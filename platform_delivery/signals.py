# from django.db.models.signals import post_save
# from django.core.signals import request_finished
# from django.dispatch import receiver
# from platform_delivery.models import *


# @receiver(post_save, sender=Order)
# def Order(sender, instance, created, **kwargs):    
    
#     if not created:
#         if instance.status == 'CANCELED':
#             for item in instance.items.all():
#                 if Characteristic.objects.filter(id=item.characteristic.id, product=item.product.id).exists():
#                     qtd = Characteristic.objects.get(id=item.characteristic.id).quantity + item.amount
#                     Characteristic.objects.filter(id=item.characteristic.id).update(quantity=qtd)
                
        