from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings
# Create your models here.

from account.models import User
from django.db.models import Q


class ItemsModel(models.Model):
    customer = models.CharField(max_length=50, null = True)
    supplier = models.CharField(max_length=50, null = True)
    productName = models.CharField(max_length=50)
    productPrice = models.IntegerField()

    @staticmethod
    def uniqueProductNames(supplier):
        if supplier:
           return ItemsModel.objects.filter(supplier = supplier).values('productName', 'supplier').distinct()
        return ItemsModel.objects.values('productName', 'supplier').distinct()


    @staticmethod
    def productsfor_Customer(customer):
        custprod = ItemsModel.objects.filter(customer=customer.username)
        allprod = ItemsModel.objects.filter(customer="all")
        custprod_distinct = custprod.values('productName').distinct()
        
        allprod = allprod.exclude(productName__in=custprod_distinct)
        
        queryset = custprod.union(allprod)
        return queryset

    def __str__(self) -> str:
        return f'{self.productName}'



class JoinedTables(models.Model):
    tableName = models.CharField(max_length=250, null= True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ["-timeOfCreating"]
    
class SingleTable(models.Model):
    tableName = models.CharField(max_length=250, null= True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ["-timeOfCreating"]

class UserTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tableName = models.CharField(max_length=50)
    dateOfCreating = models.DateField(null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)
    joinedTable = models.ForeignKey(JoinedTables, on_delete=models.CASCADE, null=True)
    singleTable = models.ForeignKey(SingleTable, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-timeOfCreating"]
    
    def __str__(self):
        return self.tableName

class TableItem(models.Model):
    table = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(null=True, default=0)
    product_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True,default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='supplier3')

    def __str__(self) -> str:
        return f'{self.product_name}-{self.product_count}'

class BigTable(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier', null = True)
    table = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)

    def __str__(self) -> str:
        return f'{self.supplier}'
    
class BigTableRows(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier1', null = True)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(null=True, default=0)
    total_price = models.IntegerField(null=True,default=0)
    # bigTable = models.ForeignKey(BigTable, on_delete=models.CASCADE)
    table = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.product_name}-{self.product_count} - {self.user}'

# class Rows_of_ordered_culumns(models.Model):
#     supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier1', null = True)
#     product_name = models.CharField(max_length=50)



class Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    joined = models.BooleanField(default=False)
    single = models.BooleanField(default=False)
    debt = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)
    # seen = models.BooleanField(default=False, null=True)
    date = models.DateField(null=True)

    def sumOfEveryUser(user):
        allDebts = Debt.objects.filter(customer = user)
        sum = 0
        for i in allDebts:                
            sum += i.debt
        return sum

    def payed(user):
        allDebts = Debt.objects.filter(customer = user)
        payed = 0
        for i in allDebts:
            if i.seen and not i.supplier:
                payed += i.debt
        return payed

    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self) -> str:
        return f'{self.customer} - {self.debt}'

class Global_Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    debt = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()

    def __str__(self) -> str:
        return f'{self.customer} -- {self.date} -- {self.debt}'  
    
class Week_debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()
    debt = models.IntegerField()

class Old_debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    timeOfCreating = models.DateTimeField(auto_now=True)
    date = models.DateField()
    debt = models.IntegerField()

# class Salary(models.Model):
#     salary = models.IntegerField()
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()

#     def __str__(self) -> str:
#         return f"{self.customer}-{self.salary}-{self.date}"


class SuppliersProducts(models.Model):

    suplier = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.suplier} {self.productName}'

class Ordered_Products_Table(models.Model):
    nameof_Table = models.CharField(max_length=150)
    supplierof_Table = models.ForeignKey(User, on_delete=models.CASCADE)
    dateof_Creating = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-dateof_Creating"]

    def __str__(self) -> str:
        return f"{self.supplierof_Table}-{self.dateof_Creating.date()}"

class Ordered_Products_Column(models.Model):
    supplierof_table = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent_Table = models.ForeignKey(Ordered_Products_Table, on_delete=models.CASCADE)
    table = models.ForeignKey(UserTable, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.parent_Table}"

# class WeekTables(models.Model):
#     weekStart = models.DateField(auto_now=True)
#     weekEnd = models.BooleanField(default=False)
#     weekTable = models.CharField(default="Table", max_length=255)
#     customerWeek = models.ForeignKey(User, null = True, on_delete=models.CASCADE) 

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Only update weekTable when creating a new instance
#             weekTable = "Table" + str(self.getId())
#             self.weekTable = weekTable
#         super().save(*args, **kwargs)

#     @staticmethod
#     def getId():
#         latest_week = WeekTables.objects.order_by('-id').first()
#         if latest_week:
#             return latest_week.id + 1
#         return 1

#     def __str__(self):
#         return f"{self.weekTable} -- {self.weekStart} -- {self.id}"


class Paymant(models.Model):
    money = models.IntegerField()
    returned = models.IntegerField()
    salary = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ["-timeOfCreating"]
