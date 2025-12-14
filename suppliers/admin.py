from django.contrib import admin
from .models import Suppliers
from .models import Order
from .models import Rating
from .models import Employee
from .models import SupplierWallet
from .models import OrderMessage
# Register your models here.
admin.site.register(Suppliers)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(Employee)
admin.site.register(SupplierWallet)
admin.site.register(OrderMessage)