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
    # Salary,
    # WeekTables,
    JoinedTables,
    SingleTable,
    Paymant,
    Week_debt,
    Global_Debt,
    Old_debt,
    BigTableRows
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
# admin.site.register(Salary)
# admin.site.register(WeekTables)
admin.site.register(JoinedTables)
admin.site.register(SingleTable)
admin.site.register(Paymant)
admin.site.register(Global_Debt)
admin.site.register(Week_debt)
admin.site.register(Old_debt)
admin.site.register(BigTableRows)