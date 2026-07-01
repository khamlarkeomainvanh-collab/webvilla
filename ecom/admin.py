from django.contrib import admin
from .models import Customer, Product, Orders, Feedback, Expense
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'category', 'description', 'amount']
    list_filter  = ['category', 'date']
admin.site.register(Expense, ExpenseAdmin)
