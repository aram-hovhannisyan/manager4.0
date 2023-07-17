from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ItemAddForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
from django.contrib.auth.decorators import login_required
from tables.models import (
    ItemsModel,
    UserTable,
    TableItem,
    BigTable,
    Debt,
    Ordered_Products_Column,
    Ordered_Products_Table,
    # Salary,
    JoinedTables,
    Paymant,
    Week_debt,
    Global_Debt,
    Old_debt,
    BigTableRows
)
from account.models import (
    User
)
from datetime import datetime
import json

from django.core.paginator import Paginator

import datetime as d


from django.http import HttpResponseRedirect
from django.db import models
from django.db.models import Sum
from account.mydecorators import (
    admin_required,
    customer_required,
    employee_required,
    supplier_required
)

from .forms import SalaryForm

def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            elif user is not None and user.is_supplier:
                login(request, user)
                return redirect('supplier')
        else:
            return redirect('login_view')
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

# ========================== Customer Start ===================

@customer_required
def customer(request):
    tablesUsers = UserTable.objects.all()
    items = ItemsModel.productsfor_Customer(request.user)

    tableRows = TableItem.objects.all()
    joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"])
    suppliers = User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) 

    return render(request, 'customer.html', {
        'Items': items,
        'Tables': tablesUsers,
        'TableRows': tableRows,
        'Suppliers': suppliers,
        "joinedSuppliers": joinedTables
        })


@customer_required
def tablesByUser(request):
    page_number = request.GET.get('page')
    # Joined Tables

    joinedTables = JoinedTables.objects.filter(
        customer=request.user,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_copy = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        ).__reversed__()  # Reversed join_page_obj
    reversed_join_page_for_debt = joinPaginator.get_page(
            joinPaginator.num_pages - join_page_obj.number + 1
        )  # Reversed join_page_obj


    reversed_table_page_obj = []
    for join in reversed_join_page_copy:
        try:
            joins = UserTable.objects.filter(
                user = request.user,
                joinedTable = join,
            )
            for jo in joins:
                reversed_table_page_obj.append(jo)
        except:
            continue
    JoinRows = []
    for tab in reversed_table_page_obj:
        try:
            row =  TableItem.objects.filter(
                customer = request.user,
                table = tab
            )
            for r in row:
                JoinRows.append(r)
        except:
            continue
    
    # Joined Tables

    single_debt_array = []
    debt_array = []
    for i in reversed_join_page_for_debt:
        try:
            joinedDebt = Debt.objects.get(
                customer = request.user,
                joined = True,
                date = i.dateOfCreating
            )
            theDebt = [str(i.dateOfCreating),joinedDebt.debt,""]
            try:
                singleDebt = Debt.objects.get(
                    customer = request.user,
                    single=True, 
                    date=i.dateOfCreating
                    )
                if singleDebt.date not in single_debt_array:
                    single_debt_array.append(singleDebt.date)
                theDebt[2] = singleDebt.debt
            except:
                pass
            debt_array.append(theDebt)
        except:
            continue

    SingleTables = []
    for date in single_debt_array:
        try:
            singleTab = UserTable.objects.get(
                user= request.user,
                singleTable__isnull = False,
                dateOfCreating = date
            )
            SingleTables.append(singleTab)
        except:
            continue

    SingleRows = []
    for table in SingleTables:
        try:
            row = TableItem.objects.filter(
                customer = request.user,
                table = table,
            )
            for r in row:
                SingleRows.append(r)
        except:
            continue

    # Single Tables 

    try:
        weekPaymant = Paymant.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        weekPaymant = Paymant.objects.none()
    
    try:
        week_debt = Week_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        week_debt = Week_debt.objects.none()
    
    try:
        old_debt = Old_debt.objects.get(
            customer = request.user,
            date = single_debt_array[0]
        )
    except:
        old_debt = Old_debt.objects.none()

    try:
        globalDebt = Global_Debt.objects.filter(customer = request.user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()

    try: 
        defaultDate = single_debt_array[0].strftime("%Y-%m-%d")
    except:
        defaultDate = datetime.now().strftime("%Y-%m-%d")

    return render(request, 'tablesbyUser.html', {
        'table': join_page_obj,
        'defaultDate': defaultDate,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        # 'Rows': tableRows,
        "SingleRows": SingleRows ,
        "JoinRows": JoinRows ,

        # 'singleTables': reversed_single_page_obj,
        'singleTables': SingleTables,
        'joinedDebt': debt_array,
        # 'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt
    })

# ========================== Customer End  ===================

# ////////////////////////// Employee Start //////////////////

@employee_required
def employee(request):

    # tablesUsers = UserTable.objects.all()
    # items = ItemsModel.objects.all()
    # tableRows = TableItem.objects.all()
    tableRows = BigTableRows.objects.all()
    bigTables = BigTable.objects.all()
    suppliers = User.objects.filter(is_supplier = True)

    uniq = ItemsModel.uniqueProductNames(None)
    # for row in tableRows:
    #     print(row.product_name ,row.total_price)
    return render(request, 'employee.html', {
        # 'Items': items,
        # 'Tables': tablesUsers,
        'Products': uniq,
        'TableRows': tableRows,
        'BigTables': bigTables,
        'Suppliers': suppliers
    })

@employee_required
def allCustomers(request):

    debts = []
    allCustomers = User.objects.filter(is_customer = True)
    allSuppliers = User.objects.filter(is_supplier = True)
    # for i in 
    globDebts = []
    for cust in allCustomers:
        try:
            latest_global = Global_Debt.objects.filter(customer=cust).latest('timeOfCreating')
            globDebts.append([cust, latest_global.debt])
        except:
             globDebts.append([cust, 0])
    for i in allCustomers:
        debts.append([i, int(Debt.sumOfEveryUser(i))])

    return render(request, 'work.html',{
        'allCustomers':allCustomers,
        'debts': globDebts,
        'allSuppliers': allSuppliers,
    })

@employee_required
def customerTables(request, user_id):
    user = User.objects.get(id = user_id)
    tableRows = TableItem.objects.filter(customer=user)  # shat a dandaxacnelu heto
    page_number = request.GET.get('page')

    tablesbyUser = UserTable.objects.filter(
        user=user, 
        singleTable__isnull=True
        ).order_by('timeOfCreating')  # Reverse the order by 'timeOfCreating'
    tablePaginator = Paginator(tablesbyUser, 10)  # show 10 tables per page
    table_page_obj = tablePaginator.get_page(page_number)
    reversed_table_page_obj = tablePaginator.get_page(
        tablePaginator.num_pages - table_page_obj.number + 1
        )  # Reversed table_page_obj

    singleTables = UserTable.objects.filter(
        user= user,
        singleTable__isnull = False
    ).order_by('timeOfCreating')
    singlePaginator = Paginator(singleTables, 1) #show 1 tables per page
    single_page_obj = singlePaginator.get_page(page_number)
    reversed_single_page_obj = singlePaginator.get_page(
        singlePaginator.num_pages - single_page_obj.number + 1
    )
    joinedTables = JoinedTables.objects.filter(
        customer=user,
        ).order_by('timeOfCreating')  # Reverse the order by '-id'
    joinPaginator = Paginator(joinedTables, 5)  # show 5 joinedTables per page
    join_page_obj = joinPaginator.get_page(page_number)
    reversed_join_page_obj = joinPaginator.get_page(
        joinPaginator.num_pages - join_page_obj.number + 1
        )  # Reversed join_page_obj
    reversed_join_page_obj =  reversed_join_page_obj.__reversed__()
    joineddebt = Debt.objects.filter(
        customer = user,
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    singleddebt = Debt.objects.filter(
        customer = user,
        single = True
        ).order_by('timeOfCreating')
    singledebtPaginator = Paginator(singleddebt, 1) #show 5 debts per page of the singled tables
    singledebt_page_obj = singledebtPaginator.get_page(page_number)
    reversed_single_debt_obj = singledebtPaginator.get_page(
        singledebtPaginator.num_pages - singledebt_page_obj.number + 1
    )
    try:
        weekPaymant = Paymant.objects.get(
            customer = user,
            date = reversed_single_debt_obj[0].date
        )
    except:
        weekPaymant = Paymant.objects.none()
    try:
        week_debt = Week_debt.objects.get(
            customer = user,
            date = reversed_single_debt_obj[0].date
        )
    except:
        week_debt = Week_debt.objects.none()
    
    try:
        old_debt = Old_debt.objects.get(
            customer = user,
            date = reversed_single_debt_obj[0].date
        )
    except:
        old_debt = Old_debt.objects.none()
    try:
        globalDebt = Global_Debt.objects.filter(customer = user).latest('timeOfCreating')
    except:
        globalDebt = Global_Debt.objects.none()
        
    return render(request, 'customerTables.html', {
        'table': join_page_obj,
        'tables': reversed_table_page_obj,
        'joins': reversed_join_page_obj,
        'Rows': tableRows,
        'singleTables': reversed_single_page_obj,
        'joinedDebt': reversed_joined_debt_obj,
        'singleDebt': reversed_single_debt_obj,
        'weekPaymant': weekPaymant,
        'weekDebt': week_debt,
        'oldDebt': old_debt,
        'globalDebt': globalDebt,
        'customer': user
    })

def myOrders(request, supplier_id):
    theSupplier = User.objects.get(id = supplier_id)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = theSupplier)
    columnsOFtable = Ordered_Products_Column.objects.filter(supplierof_table = theSupplier)
    uniq = ItemsModel.uniqueProductNames(theSupplier)
    customers = User.objects.filter(is_customer = True)
    tableRows = TableItem.objects.filter(supplier_id = supplier_id)
    # print(tableRows.count(), theSupplier)

    return render(request, 'myOrders.html', {
        'supplier': theSupplier,
        'Tables': orderedProducts_Tables,
        'Columns_of_Table': columnsOFtable,
        'Products': uniq,
        'Customers': customers,
        'TableRows': tableRows,
    })

@employee_required
def totalPage(request):
    page_number = request.GET.get('page')  
    joineddebt = Debt.objects.filter(
        customer = User.objects.get(username = 148),
        joined = True
        ).order_by('timeOfCreating')
    joineddebtPaginator = Paginator(joineddebt, 5) #show 5 debts per page of the joined tables
    joineddebt_page_obj = joineddebtPaginator.get_page(page_number)
    reversed_joined_debt_obj = joineddebtPaginator.get_page(
        joineddebtPaginator.num_pages - joineddebt_page_obj.number + 1
    )
    single_debt_array = []
    single_debt_dict = {}
    for i in reversed_joined_debt_obj:
        try: 
            singleDebt = Debt.objects.filter(
                single=True, 
                date=i.date
                )
            if singleDebt[0].date not in single_debt_array:
                single_debt_array.append(singleDebt[0].date)
                single_debt_dict[str(i.date)] = singleDebt.aggregate(sum = Sum('debt'))['sum']
        except:
            continue
    debt_array = []
    for debt in reversed_joined_debt_obj:
        joinTable_debt = Debt.objects.filter(
            joined = True,
            date = debt.date
        )
        try:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], single_debt_dict[str(debt.date)]])
        except:
            debt_array.append([str(debt.date),joinTable_debt.aggregate(sum = Sum('debt'))['sum'], ''])


    # PAYMANT
    try:
        total_payments_money = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(money=models.Sum('money'))['money']
        total_payments_returned = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(returned=models.Sum('returned'))['returned']
        total_payments_salary = Paymant.objects.filter(
            date = single_debt_array[0],
        ).aggregate(salary=models.Sum('salary'))['salary']
    except:
        total_payments_money = 0
        total_payments_returned = 0
        total_payments_salary = 0

    # PAYMANT

    customers = User.objects.filter(is_customer=True)
    total_global_debt = 0
    try:
        old_debt = Old_debt.objects.filter(date = single_debt_array[0]).aggregate(sum = Sum('debt'))['sum']
        new_debt = Week_debt.objects.filter(date = single_debt_array[0]).aggregate(sum = Sum('debt'))['sum']
    except:
        old_debt = 0
        new_debt = 0
        pass
    for customer in customers:
        debt = Global_Debt.objects.filter(customer=customer).order_by('-timeOfCreating').first()
        if debt:
            total_global_debt += debt.debt

    return render(request, 'totalPage.html',{
        'joinedDebt': debt_array,
        'table': joineddebt_page_obj,
        # 'singleDebt': single_debt_by_date,
        'Returned': total_payments_returned,
        'Salary': total_payments_salary,
        'Money': total_payments_money,
        'GlobalDebt': total_global_debt,
        'OldDebt': old_debt,
        'NewDebt': new_debt,
    })

# \\\\\\\\\\\\\\\\\\\\\\\\\\ Employee End   \\\\\\\\\\\\\\\\\\

# ========================== Admin Start    ==================

@admin_required
def admin(request):
    users = User.objects.filter(is_customer=True)
    suppliers = User.objects.filter(is_supplier=True)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        customers = data['customers']
        supplier = data['supplier']
        productName = data['productName']
        productPrice = data['productPrice']

        for customer in customers:
            item = ItemsModel(
                customer=customer,
                supplier=supplier,
                productName=productName,
                productPrice=productPrice
            )
            item.save()

        return redirect('adminpage')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm()

    items = ItemsModel.objects.all()
    return render(request, 'admin.html', {'Items': items, 'Users': users, 'Suppliers': suppliers, 'Form': form})


@admin_required
def delete_item(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()       
    # return redirect('adminpage')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_all(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('productsforall')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_item_byuser(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def edit_item(request, item_id):
    customers = User.objects.filter(is_customer=True)
    item = get_object_or_404(ItemsModel, id=item_id)
    suppliers = User.objects.filter(is_supplier = True)
    if request.method == 'POST':
        form = ItemAddForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('adminpage')
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm(instance=item)
    return render(request, 'edit_item.html', {'form': form,'item':item, 'Users': customers, 'Suppliers': suppliers})

@admin_required
def allCustomersforAdmin(request):
    allCustomers = User.objects.filter(is_customer = True)
    return render(request, 'allCustomersforAdmin.html',{'allCustomers':allCustomers})

@admin_required
def customersProducts(request, user_id):
    customer = User.objects.get(id = user_id)
    Products = ItemsModel.objects.all()
    return render(request, 'customerProducts.html', {'customer': customer, 'products':Products})

@admin_required
def productsForAll(request):
    Products = ItemsModel.objects.filter(customer = 'all')
    return render(request, 'productsForAll.html', {'products': Products})

# ========================== Admin End      ==================

# ///////////////////////// Supplier Start  //////////////////

@supplier_required
def supplier(request):
    # products = ItemsModel.objects.filter(supplier = request.user.username)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = request.user)
    columnsOFtable = Ordered_Products_Column.objects.filter(supplierof_table = request.user)
    uniq = ItemsModel.uniqueProductNames(request.user)
    customers = User.objects.filter(is_customer = True)
    tableRows = TableItem.objects.filter(supplier = request.user)
    # print(tableRows.count())
    paginator = Paginator(orderedProducts_Tables, 3) # show 3 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'supplier.html', {
        'Tables': page_obj,
        'Columns_of_Table': columnsOFtable,
        'Products': uniq,
        'Customers': customers,
        'TableRows': tableRows,
    })

@supplier_required
def orderedProducts(request):
    return render(request, 'ordered_Product.html', {})
# \\\\\\\\\\\\\\\\\\\\\\\\ Supplier End     \\\\\\\\\\\\\\\\\\  