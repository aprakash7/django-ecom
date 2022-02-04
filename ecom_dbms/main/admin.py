from django.contrib import admin
from .models import *

class dateandtime(admin.ModelAdmin):
    readonly_fields= ('date',)

admin.site.register(Product, dateandtime)
admin.site.register(Order, dateandtime)
admin.site.register(OrderItem, dateandtime)
admin.site.register(Address)
admin.site.register(Customer)