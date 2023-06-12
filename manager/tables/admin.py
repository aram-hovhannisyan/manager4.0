from django.contrib import admin
from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt,
    SuppliersProducts,
    Ordered_Products_Column,
    Ordered_Products_Table,
    Salary
)
# Register your models here.
admin.site.register(ItemsModel)
admin.site.register(TableItem)
admin.site.register(UserTable)
admin.site.register(BigTable)
admin.site.register(Debt)
admin.site.register(SuppliersProducts)
admin.site.register(Ordered_Products_Table)
admin.site.register(Ordered_Products_Column)
admin.site.register(Salary)
