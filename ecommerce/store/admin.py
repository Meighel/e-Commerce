from django.contrib import admin
from store.models import User, Order, CartItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
admin.site.register(Order)
admin.site.register(CartItem)
