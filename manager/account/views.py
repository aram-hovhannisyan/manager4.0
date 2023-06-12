from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ItemAddForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

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
    Salary
)
from account.models import (
    User
)

import json

from django.core.paginator import Paginator

from django.http import HttpResponseRedirect

from account.mydecorators import *

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
    suppliers = User.objects.filter(is_supplier = True)
    # print(tableRows)
    # for i in items: 
    #     print(i.customer)
    return render(request, 'customer.html', {
        'Items': items,
        'Tables': tablesUsers,
        'TableRows': tableRows,
        'Suppliers': suppliers
        })

@customer_required
def tablesByUser(request):
    tablesbyUser = UserTable.objects.filter(user = request.user)
    tableRows = TableItem.objects.all()
    
    paginator = Paginator(tablesbyUser, 5) # show 10 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    debt = Debt.objects.filter(customer = request.user)

    suppliers = User.objects.filter(is_supplier = True)

    total = int(Debt.sumOfEveryUser(request.user))
    payed = int(Debt.payed(request.user))


    return render(request, 'tablesbyUser.html', {
        'tables':page_obj,
        'Rows':tableRows,
        'debt_row': debt,
        'Suppliers': suppliers,
        'total': total,
        'payed':payed
        })

# ========================== Customer End  ===================

# ////////////////////////// Employee Start //////////////////

@employee_required
def employee(request):

    # tablesUsers = UserTable.objects.all()
    # items = ItemsModel.objects.all()
    tableRows = TableItem.objects.all()
    bigTables = BigTable.objects.all()
    suppliers = User.objects.filter(is_supplier = True)

    uniq = ItemsModel.uniqueProductNames()
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
    for i in allCustomers:
        if Debt.have_not_seen(i):
            debts.append([i, int(Debt.sumOfEveryUser(i)), False])
        else:
            debts.append([i, int(Debt.sumOfEveryUser(i)), True])

    return render(request, 'work.html',{
        'allCustomers':allCustomers,
        'debts': debts,
        'allSuppliers': allSuppliers,
                                                })

@employee_required
def customerTables(request, user_id):
    customer = User.objects.get(id = user_id)
    tablesUsers = UserTable.objects.filter(user_id = user_id)
    tableRows = TableItem.objects.all()
    
    paginator = Paginator(tablesUsers, 5) # show 10 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'customerTables.html', {
        'tables':page_obj,
        'Rows':tableRows,
        'customer':customer
        })

@employee_required
def customerDebt(request, user_id):
    customer = User.objects.get(id = user_id)
        
    suppliers = User.objects.filter(is_supplier = True)

    customersDept = Debt.objects.filter(customer_id = user_id)

    total = int(Debt.sumOfEveryUser(customer))
    payed = int(Debt.payed(customer))
    return render(request, 'customersDebt.html', {
        'customer':customer,
        'debt_row': customersDept,
        'Suppliers': suppliers,
        'total': total,
        'payed':payed
    } )

def toggle_seen(request, debt_id):
    # Get the Debt object based on the debt_id
    try:
        debt = Debt.objects.get(id=debt_id)
    except Debt.DoesNotExist:
        return JsonResponse({'error': 'Debt not found'}, status=404)
    customer = debt.customer
    # Toggle the 'seen' field
    debt.seen = not debt.seen
    debt.save()
    total = int(Debt.sumOfEveryUser(customer))
    payed = int(Debt.payed(customer))
    # Return the updated 'seen' value and debt amount in the response
    return JsonResponse({'seen': debt.seen, 'debt': debt.debt,'payed':payed, 'total':total })

def myOrders(request, supplier_id):
    theSupplier = User.objects.get(id = supplier_id)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = theSupplier)
    columnsOFtable = Ordered_Products_Column.objects.filter(supplierof_table = theSupplier)
    uniq = ItemsModel.uniqueProductNames()
    customers = User.objects.filter(is_customer = True)
    tableRows = TableItem.objects.all()

    return render(request, 'myOrders.html', {
        'supplier': theSupplier,
        'Tables': orderedProducts_Tables,
        'Columns_of_Table': columnsOFtable,
        'Products': uniq,
        'Customers': customers,
        'TableRows': tableRows,
    })

def sendSalary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Process the form data
            customer = User.objects.get(username = form.cleaned_data['customer'])
            date = form.cleaned_data['date']
            salary = form.cleaned_data['salary']
            # Perform further actions (e.g., send salary to the selected customer)
            # ...

            Salary.objects.create(
                salary = salary,
                customer = customer,
                date = date
            ).save()
            return redirect('customers')  # Render a success page
    else:
        form = SalaryForm()
    
    return redirect('customers')

def salaries(request):
    sal = Salary.objects.all()
    cust = User.objects.filter(is_customer = True)
    return render(request, 'customersSalaries.html', {
        'Sal': sal,
        'Customers': cust
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
    return render(request, 'allcustomersforAdmin.html',{'allCustomers':allCustomers})

@admin_required
def customersProducts(request, user_id):
    customer = User.objects.get(id = user_id)
    Products = ItemsModel.objects.all()
    return render(request, 'customerProducts.html', {'customer': customer, 'products':Products})

@admin_required
def productsForAll(request):
    Products = ItemsModel.objects.filter(customer = 'all')
    return render(request, 'productsforAll.html', {'products': Products})

# ========================== Admin End      ==================

# ///////////////////////// Supplier Start  //////////////////

@supplier_required
def supplier(request):
    # products = ItemsModel.objects.filter(supplier = request.user.username)
    orderedProducts_Tables = Ordered_Products_Table.objects.filter(supplierof_Table = request.user)
    columnsOFtable = Ordered_Products_Column.objects.filter(supplierof_table = request.user)
    uniq = ItemsModel.uniqueProductNames()
    customers = User.objects.filter(is_customer = True)
    tableRows = TableItem.objects.all()

    paginator = Paginator(orderedProducts_Tables, 3) # show 10 tables per page
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