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
    def uniqueProductNames():
        unique_names = ItemsModel.objects.values('productName', 'supplier').distinct()
        return unique_names

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

class UserTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tableName = models.CharField(max_length=50)
    dateOfCreating = models.DateField(auto_now=True, null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

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

    def __str__(self) -> str:
        return f'{self.product_name}-{self.product_count}'

class BigTable(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE,related_name='supplier', null = True)
    table = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)

    def __str__(self) -> str:
        return f'{self.supplier}'
    


class Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name='supplier0') 
    debt = models.IntegerField()
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)
    seen = models.BooleanField(default=False, null=True)
    is_return = models.BooleanField(default=False, null=True)
    date = models.DateField(auto_now=True,null=True)

    def sumOfEveryUser(user):
        allDebts = Debt.objects.filter(customer = user)
        sum = 0
        for i in allDebts:                
            if i.seen:
                sum += i.debt
        return sum

    def payed(user):
        allDebts = Debt.objects.filter(customer = user)
        payed = 0
        for i in allDebts:
            if i.seen and not i.supplier:
                payed += i.debt
        return payed

    def have_not_seen(user):
        allDebts = Debt.objects.filter(customer = user)
        notSeen = False
        for i in allDebts:
            if not i.seen:
                notSeen = True
        return notSeen

    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self) -> str:
        return f'{self.customer} - {self.debt}'
    
class Salary(models.Model):
    salary = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.customer}-{self.salary}-{self.date}"

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
    # customer_Table = models.ForeignKey(UserTable, on_delete=models.CASCADE)

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

