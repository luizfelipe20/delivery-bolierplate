import re
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import JSONField

CHARACTERISTIC_TYPE = [
    ('SIZE', 'Tamanho'),
    ('COLOR', 'Cor'),
]

PAYMENT_WAY = [
    ('CARD', 'Cartão de crédito'),
    ('BOLETO', 'Boleto'),
    ('TRANSFER', 'Transferência bancária'),
]

ORDER_STATUS = [
    ('RECEIVED', 'Pedido recebido'),
    ('PAID', 'Pagamento aprovado'),
    ('NF', "Nota fiscal emitida"),
    ('TRANSPORT', "Em transporte"),
    ('DELIVERED', "Entregue"),
    ('CANCELED', "Cancelado")
]


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
          raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user

        
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=255,
        unique=True,
        help_text=_('Required. 15 characters or fewer. Letters, \
                    numbers and @/./+/-/_ characters'),
        validators=[
                    validators.RegexValidator(
                                            re.compile('^[\w.@+-]+$'),
                                            _('Enter a valid username.'),
                                            _('invalid')
                    )
        ]
    )
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    name = models.CharField(_('nome'), max_length=200, blank=True, null=True)
    cpf = models.CharField(_('cpf'), max_length=200, blank=True, null=True)
    phone = models.CharField(_('telefone'), max_length=200, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. \
                    Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False,
        help_text=_('Designates whether this user has confirmed his account.'))
    phone = models.CharField(_('telefone'), max_length=30, blank=True, null=True)
    ddd = models.CharField(_('ddd'), max_length=2, blank=True, null=True)
    login_facebook = models.BooleanField(null=True, blank=True)
    categories_music = JSONField(null=True, blank=True)
     
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Address(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=25, verbose_name="CEP")
    neighborhood = models.CharField(max_length=255, verbose_name="Bairro")
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=10, verbose_name="Número")
    complement = models.CharField(max_length=255, verbose_name="Complemento", null=True, blank=True)
    reference = models.CharField(max_length=255, verbose_name="Ponto de referência", null=True, blank=True)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return "{}".format(self.street)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return "{}".format(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    name = models.CharField(max_length=100, verbose_name="Nome")
    value = models.FloatField(verbose_name="Preço")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    availability = models.BooleanField(verbose_name="Disponibilidade", default=False)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return "{}".format(self.name)


class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, verbose_name="Tipo", choices=CHARACTERISTIC_TYPE)
    title = models.CharField(max_length=20, verbose_name="Descrição", blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantidade", default=0)

    class Meta:
        verbose_name = "Característica"
        verbose_name_plural = "Características"

    def __str__(self):
        return "{} - {} - {}".format(self.product.name, self.type, self.id)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Image")

    class Meta:
        verbose_name = "Imagem do produto"
        verbose_name_plural = "Imagens do produto"

    def __str__(self):
        return "{}".format(self.product.name)


class Bag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="produto", blank=True, null=True)
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantidade", default=0)
    value = models.FloatField(blank=True, null=True, verbose_name="valor")

    class Meta:
        verbose_name = "Sacola"
        verbose_name_plural = "Sacolas"

    def __str__(self):
        return "{}".format(self.client.name)


class Banner(models.Model):
    image = models.ImageField(verbose_name="Image")
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return "Banner"


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="produto")
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name="quantidade")
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, blank=True, null=True, verbose_name="característica do produto")
    value = models.FloatField(blank=True, null=True, verbose_name="valor")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
    
    def __str__(self):
        return "{}".format(self.product.name)
    
    
class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="cliente")
    items = models.ManyToManyField(Item, verbose_name="itens do pedido")
    number = models.CharField(max_length=20, verbose_name="Número do pedido")
    payment_way = models.CharField(max_length=10, verbose_name="Forma de pagamento", choices=PAYMENT_WAY)
    status = models.CharField(verbose_name="Status", max_length=10, choices=ORDER_STATUS, default='RECEIVED')
    total_value = models.FloatField(verbose_name="Valor bruto", default=0)
    discount_value = models.FloatField(verbose_name="Valor do desconto", default=0)
    value = models.FloatField(verbose_name="Valor total", default=0)
    date = models.DateTimeField(verbose_name="Data da compra", default=datetime.now)
    tracking_code = models.CharField(verbose_name="Código de rastreio", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return "{}".format(self.client.name)


class Rating(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_rating")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.FloatField(verbose_name="estrelas", default=0)
    comment = models.TextField(verbose_name="comentário", null=True, blank=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return "{}".format(self.client.name)


class Favorite(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="cliente")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="produto")

    class Meta:
        verbose_name = "Favoritado"
        verbose_name_plural = "Favoritados"

    def __str__(self):
        return "{}".format(self.client.name)