from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from platform_delivery.models import *
from platform_delivery.serializers import *
from platform_delivery.send_email import send_email


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(['post'], detail=False)
    def login(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'email': user.email,
            'name': user.name
        })

        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    
    @action(['get'], detail=False)
    def rating_by_client(self, request, *args, **kwargs):
        
        client_id = self.request.query_params.get("client", None)        
        return Response(
            data=self.serializer_class(Rating.objects.filter(client=client_id).order_by('id'), many=True).data, 
            status=status.HTTP_200_OK
        )
    
    @action(['get'], detail=False)
    def rating_by_product(self, request, *args, **kwargs):
        return Response(
            data= RatingByProductSerializer(Rating.objects.distinct('product').all(), many=True).data,
            status=status.HTTP_200_OK
        )

        
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
    def list(self, request, *args, **kwargs):
        
        client_id = self.request.query_params.get("client", None)
        self.queryset = self.queryset.filter(client=client_id)    

        return super(AddressViewSet, self).list(request, *args, **kwargs)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    
    @action(['get'], detail=False)
    def favorites_by_client(self, request, *args, **kwargs):
        
        client_id = self.request.query_params.get("client", None)
        
        products = Product.objects.filter(id__in=list(Favorite.objects.filter(client=client_id).values_list("product", flat=True)))
        
        return Response(
            data=ProductSerializer(products, many=True).data, 
            status=status.HTTP_200_OK
        )
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(['get'], detail=False)
    def home_products(self, request, *args, **kwargs):
        
        news = ProductSerializer(Product.objects.filter(new=True), many=True).data
        most_sold = ProductSerializer(Product.objects.filter(most_sold=True), many=True).data

        data = {
            'news': news, 
            'most_sold': most_sold
        }
        return Response(data=data, status=status.HTTP_200_OK)


class BagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer
    
    @action(['get'], detail=False)
    def bag_by_client(self, request, *args, **kwargs):
        
        client_id = self.request.query_params.get("client", None)
    
        return Response(
            data=self.serializer_class(Bag.objects.filter(client=client_id), many=True).data, 
            status=status.HTTP_200_OK
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def list(self, request, *args, **kwargs):
        self.serializer_class = OrderListSerializer
        return super(OrderViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):    
        list_ids_items = []
        
        for item in request.data["items"]:                       
            
            obj = {"product": 0, "amount": 0, "value": 0} 
            obj["product"] = item["product"]
            obj["amount"] = item["amount"]
            obj["characteristic"] = item["characteristic"]
            obj["value"] = item["value"]
                
            serializer_item = ItemSerializer(data=obj)
            serializer_item.is_valid(raise_exception=True)
            serializer_item.save()
            list_ids_items.append(serializer_item.data["id"])
                
            if not Characteristic.objects.filter(id=item["characteristic"], product=item["product"]).exists():
                return Response("Produto sem estoque.", status=status.HTTP_400_BAD_REQUEST)
            
            qtd = Characteristic.objects.get(id=item["characteristic"]).quantity - item["amount"]
            
            if qtd < 0:
                return Response("Esta compra não pode ser efetuada, o estoque não contém mais este produto.", status=status.HTTP_400_BAD_REQUEST)
                
            Characteristic.objects.filter(id=item["characteristic"]).update(quantity=qtd)   
            
        request.data["items"] = list_ids_items
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.triggering_email_request_requests(serializer)
        self.clean_bag(serializer.data["client"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def clean_bag(self, client):
        if Bag.objects.filter(client=client).exists():
            Bag.objects.filter(client=client).delete() 
        
    def triggering_email_request_requests(self, serializer):
        send_email("Solicitação de pedido", "Solicitação de pedido - Talismã", "felipekjs36@gmail.com")
        
    @action(['get'], detail=False)
    def orders_by_client(self, request, *args, **kwargs):
        
        client_id = self.request.query_params.get("client", None)
        
        orders = Order.objects.filter(client=client_id)
        
        return Response(
            data=OrderSerializer(orders, many=True).data, 
            status=status.HTTP_200_OK
        )