from rest_framework import serializers
from platform_delivery.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'phone')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        depth = 1
        fields = ('id', 'category', 'name', 'subtitle', 'value', 'stars', 'description', 'details', 'productimage_set', 'characteristic_set')


class BagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bag
        fields = ['id', 'product', 'characteristic', 'quantity', 'value', 'client']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'cep', 'neighborhood', 'street', 'number', 'complement', 'reference')


class CharacteristicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = ['id', 'type', 'quantity', 'title']


class ProductImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image(self, obj):
        if obj.image is not None and hasattr(obj.image, 'url'):
            return obj.image.url
        return ''


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'client', 'product', 'stars', 'comment']

    
class RatingByProductSerializer(serializers.ModelSerializer):
    
    stars = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['id', 'client', 'product', 'stars', 'comment']

    def get_stars(self, obj):
        from django.db.models import Avg
        return Rating.objects.filter(product=obj.product.id).aggregate(Avg('stars'))["stars__avg"]

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        

class BannerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Banner
        fields = '__all__'
        

class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'product', 'characteristic', 'amount', 'value']


class ItemOrderSerializer(serializers.ModelSerializer):
    
    # product = ProductSerializer()
    class Meta:
        model = Item
        fields = ['product', 'characteristic', 'amount', 'value']


        
class OrderListSerializer(serializers.ModelSerializer):
    
    # items = ItemOrderSerializer(many=True)
    # client = ClientSerializer()
    class Meta:
        model = Order
        depth = 1
        fields = ['client', 'items', 'number', 'payment_way', 'status', 'total_value', 'discount_value', 'value', 'date', 'tracking_code']
