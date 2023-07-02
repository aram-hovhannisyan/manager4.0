from django.shortcuts import render, get_object_or_404
from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    JoinedTables,
    SingleTable,
    Paymant,
    Global_Debt,
    Week_debt,
    Old_debt,
    BigTableRows
)
from account.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from django.shortcuts import redirect

from account.forms import PaymantForm

# Create your views here.


def home(request):
    User = request.user
    Items = ItemsModel.objects.all()

    return render(request, 'tables/home.html', {'Items': Items, 'user': User})


@login_required
@csrf_exempt
def save_table_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        table_name = json.loads(request.body)['table_name']
        total = json.loads(request.body)['total-sum']
        date = json.loads(request.body)['date']
        joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"])

        if len(table_name) == 1:
            try:
                Old_debt.objects.get(
                    date = date,
                    customer = request.user
                )
            except:
                try:
                    latest_global = Global_Debt.objects.filter(customer=request.user).latest('timeOfCreating')
                    Old_debt.objects.create(
                        customer = request.user,
                        date = date,
                        debt = latest_global.debt
                    )
                except:
                    Old_debt.objects.create(
                        customer = request.user,
                        date = date,
                        debt = 0
                    )
        try:
            SingleTable.objects.get(dateOfCreating = date, customer = request.user)
        except:
            try:
                Old_debt.objects.get(
                    date = date,
                    customer = request.user
                )
            except:
                try:
                    latest_global = Global_Debt.objects.filter(customer=request.user).latest('timeOfCreating')
                    oldDebt = Old_debt.objects.create(
                        customer = request.user,
                        date = date,
                        debt = latest_global.debt
                    )
                except:
                    oldDebt = Old_debt.objects.create(
                        customer = request.user,
                        date = date,
                        debt = 0
                    )
        try:
            latest_global_debt = Global_Debt.objects.filter(customer=request.user).latest('timeOfCreating')
            # print(latest_global_debt.debt, 'lastest debt')
            newGlobalDebt = Global_Debt.objects.create(
                customer = request.user,
                date = date,
                debt = latest_global_debt.debt + total
            )
        except:
            newGlobalDebt = Global_Debt.objects.create(
                customer = request.user,
                date = date,
                debt = total
            )

        if len(table_name) == 1:
            singleTabUsr = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) 
            mainTable = SingleTable.objects.create(
                tableName = table_name,
                customer = request.user,
                dateOfCreating = date
                )
            for join, tabNam in zip(singleTabUsr, table_name):
                table = UserTable.objects.create(
                    user = request.user,
                    tableName = tabNam,
                    singleTable = mainTable,
                    dateOfCreating = date
                )
                for row in data:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user
                    )
                    table_item.save()

                    big_tab, created = BigTableRows.objects.get_or_create(
                        user=request.user,
                        supplier=join,
                        product_name=table_item.product_name,
                        defaults={
                            'product_count': table_item.product_count,
                            'total_price': table_item.total_price,
                            'table': table
                        }
                    )
                    if not created:
                        big_tab.product_count = table_item.product_count
                        big_tab.total_price = table_item.total_price
                        big_tab.table = table
                        big_tab.save()

                try:
                    bigtable = BigTable.objects.get(supplier=join, user=request.user)
                    bigtable.table = table
                    bigtable.save()
                except BigTable.DoesNotExist:
                    bigtable = BigTable.objects.create(
                        supplier=join,
                        table=table,
                        user=request.user
                        )
            debt = Debt.objects.create(
                customer = request.user,
                single = True,
                debt = total,
                date = date
            )  
            return JsonResponse({'message': 'Table data saved successfully'})

        mainTable = JoinedTables.objects.create(
            tableName = table_name, 
            customer = request.user,
            dateOfCreating = date
            )
        for join, tabNam in zip(joinedTables, table_name):
            table = UserTable.objects.create(
                user = request.user,
                tableName = tabNam,
                joinedTable = mainTable,
                dateOfCreating = date
            )
            table.save()
            for row in data:
                if row['supplier'] == join.username:
                    if row['productCount'] == '':
                        row['productCount'] = 0
                    table_item = TableItem.objects.create(
                        table=table,
                        product_name=row['productName'],
                        product_count=row["productCount"],
                        product_price=row['productPrice'],
                        total_price=row['totalPrice'],
                        customer = request.user
                    )
                    table_item.save()

                    big_tab, created = BigTableRows.objects.get_or_create(
                        user=request.user,
                        supplier=join,
                        product_name=table_item.product_name,
                        defaults={
                            'product_count': table_item.product_count,
                            'total_price': table_item.total_price,
                            'table': table
                        }
                    )
                    if not created:
                        big_tab.product_count = table_item.product_count
                        big_tab.total_price = table_item.total_price
                        big_tab.table = table
                        big_tab.save()

            try:
                bigtable = BigTable.objects.get(supplier=join, user=request.user)
                bigtable.table = table
                bigtable.save()
            except BigTable.DoesNotExist:
                bigtable = BigTable.objects.create(
                    supplier=join,
                    table=table,
                    user=request.user
                    )
                



        debt = Debt.objects.create(
            customer = request.user,
            joined = True,
            debt = total,
            date = date
        )   

        return JsonResponse({'message': 'Table data saved successfully'})

def Paymant_View(request):
    if request.method == 'POST':
        form = PaymantForm(request.POST)
        if form.is_valid():
            debt = Paymant.objects.create(
                customer=request.user,
                money= int(request.POST.get('money')),
                returned = int(request.POST.get('returned')),
                salary = int(request.POST.get('salary')),
                date = request.POST.get('date')
                )
            latest_global_debt = Global_Debt.objects.filter(customer = request.user).latest('timeOfCreating')
            debt_sum = latest_global_debt.debt - debt.money - debt.returned - debt.salary
            weekDebt = Week_debt.objects.create(
                customer = request.user,
                date = request.POST.get('date'),
                debt = debt_sum
            )
            gloabalDebt = Global_Debt.objects.create(
                customer = request.user,
                debt = debt_sum,
                date = request.POST.get('date')
            )

            print(request.POST.get('date'), 'dateeee Payyy')
            debt.save()
            return redirect('tablesbyuser')
        return redirect('tablesbyuser')
    return redirect('tablesbyuser')

def sendOrder(request):
    if request.method == "POST": 
        data = json.loads(request.body)
        suplier_id = data['supplier_id']
        orderedTableName = data['nameOftable']
        customers = User.objects.filter(is_customer = True)
        supplier = User.objects.get(username = data['sup_name'])
        pTable = Ordered_Products_Table.objects.create(
            nameof_Table = orderedTableName,
            supplierof_Table = supplier,
        )
        pTable.save()
        # rows_of_colmns = 
        for customer in customers:
            try:
                # print('Hello World!')
                custBigTable = BigTable.objects.get(
                    supplier_id = suplier_id,
                    user = customer
                    )
                columnof_Table = UserTable.objects.get(
                    tableName = custBigTable.table.tableName
                    )
                Ordered_Products_Column.objects.create(
                    parent_Table = pTable,
                    table = columnof_Table,
                    supplierof_table = supplier,
                ).save()
            except:
                continue
    
    return redirect('employee')


# def Return(request):
#     if request.method == 'POST':
#         form = PaymantForm(request.POST)
#         if form.is_valid():
#             debt = Debt.objects.create(
#                 customer=request.user,
#                 debt=-int(request.POST.get('debt')),
#                 is_return = True,
#                 date = request.POST.get('date')
#                 )
#             print(request.POST.get('date'), 'dateeee')
#             debt.save()
#             return redirect('customer')
#         return redirect('customer')
#     return redirect('customer')