import os
import django
import datetime
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()
from tables.models import ItemsModel, JoinedTables, SingleTable, TableItem, Week_debt, BigTableRows
from account.models import User
from tables.models import UserTable, Debt, Old_debt, Global_Debt, BigTable, Paymant

def create_join_items():
    customers = ['all']
    suppliers = ['Կիրովական', 'Արտադրամաս']

    for i in range(1, 31):
        ItemsModel.objects.create(
            customer=customers[0],
            supplier=suppliers[0] if i <= 15 else suppliers[1],
            productName=f'item{i}',
            productPrice=i * 20
        )

    print('Join Items created successfully!')

def create_single_items():
    customers = ['all']
    suppliers = ['Այլ.ապրանք']

    for i in range(1, 16):
        ItemsModel.objects.create(
            customer=customers[0],
            supplier=suppliers[0],
            productName=f'Apranq{i}',
            productPrice=i * 20
        )

    print('Single Items created successfully!')

def create_singletables(today):
    customers = User.objects.filter(is_customer=True)
    suppliers = []
    joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"])
    for i in User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"]):
        suppliers.append(i)
    for j in User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')):
        suppliers.append(j)
    items = ItemsModel.objects.all()

    for customer in customers:
        total = 0
        try:
            Old_debt.objects.get(
                date=today,
                customer=customer
            )
        except:
            try:
                latest_global = Global_Debt.objects.filter(customer=customer).latest('timeOfCreating')
                Old_debt.objects.create(
                    customer=customer,
                    date=today,
                    debt=latest_global.debt
                )
            except:
                Old_debt.objects.create(
                    customer=customer,
                    date=today,
                    debt=0
                )

        single_table = SingleTable.objects.create(
            tableName=f'Single Table {customer}',
            dateOfCreating=today,
            customer=customer
        )
        user_table = UserTable.objects.create(
            user=customer,
            tableName=f'Single Table-{customer}',
            singleTable=single_table,
            dateOfCreating=today,
        )
        try:
            bigtable = BigTable.objects.get(supplier=suppliers[2], user=customer)
            bigtable.table = user_table
            bigtable.save()
        except BigTable.DoesNotExist:
            bigtable = BigTable.objects.create(
                supplier=suppliers[2],
                table=user_table,
                user=customer
            )

        for item in items:
            if item.supplier == suppliers[2].username:
                table_item = TableItem.objects.create(
                    table=user_table,
                    product_name=item.productName,
                    product_count=20,
                    product_price=item.productPrice,
                    total_price=item.productPrice * 20,
                    customer=customer,
                    supplier = suppliers[2]
                )
                big_tab, created = BigTableRows.objects.get_or_create(
                    user=customer,
                    supplier=suppliers[2],
                    product_name=table_item.product_name,
                    defaults={
                        'product_count': table_item.product_count,
                        'total_price': table_item.total_price,
                        'table': user_table
                    }
                )
                if not created:
                    big_tab.product_count = table_item.product_count
                    big_tab.total_price = table_item.total_price
                    big_tab.table = user_table
                    big_tab.save()

                total += item.productPrice * 20

        debt = Debt.objects.create(
            customer=customer,
            single=True,
            debt=total,
            date=today
        )
        try:
            latest_global_debt = Global_Debt.objects.filter(customer=customer).latest('timeOfCreating')
            newGlobalDebt = Global_Debt.objects.create(
                customer=customer,
                date=today,
                debt=latest_global_debt.debt + total
            )
        except:
            newGlobalDebt = Global_Debt.objects.create(
                customer=customer,
                date=today,
                debt=total
            )
        total = 0

    print('single pages were created')


def create_tables(today, create):
    if create:
        create_join_items()
        create_single_items()

    create_singletables(today)
    items = ItemsModel.objects.all()
    customers = User.objects.filter(is_customer=True)

    # today = datetime.date.today() + datetime.timedelta(days=7) #start day
    total = 0

    suppliers = []
    joinedTables = User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"])
    for i in User.objects.filter(is_supplier=True, username__in=["Կիրովական", "Արտադրամաս"]):
        suppliers.append(i)
    for j in User.objects.filter(is_supplier=True).exclude(username__in=joinedTables.values('username')) :
        suppliers.append(j)

    print("Start joined table creating")

    for customer in customers:
        print(customer.username)
        for i in range(5):
            table_date = today + datetime.timedelta(days=i)    
            joined_table = JoinedTables.objects.create(
                tableName=f'JoinedTable-{customer.username}-{i}',
                dateOfCreating = table_date,
                customer = customer
                )
            # print(table_date, today)
            for k in range(2):
                user_table = UserTable.objects.create(
                    user=customer,
                    tableName=f'Joined Table-{customer}-{i}{k}',
                    joinedTable=joined_table,
                    dateOfCreating = table_date,
                )
                try:
                    bigtable = BigTable.objects.get(supplier=suppliers[i % 2], user=customer)
                    bigtable.table = user_table
                    bigtable.save()
                except BigTable.DoesNotExist:
                    bigtable = BigTable.objects.create(
                        supplier=suppliers[i % 2],
                        table=user_table,
                        user=customer
                        )
                for item in items:
                    if item.supplier == suppliers[i % 2].username:
                        table_item = TableItem.objects.create(
                            table= user_table,
                            product_name = item.productName,
                            product_count = 40,
                            product_price = item.productPrice,
                            total_price = item.productPrice * 20,
                            customer = customer,
                            supplier = suppliers[i % 2]
                        )
                        table_item.save()
                        big_tab, created = BigTableRows.objects.get_or_create(
                            user=customer,
                            supplier=suppliers[i % 2],
                            product_name=table_item.product_name,
                            defaults={
                                'product_count': table_item.product_count,
                                'total_price': table_item.total_price,
                                'table': user_table
                            }
                        )
                        if not created:
                            big_tab.product_count = table_item.product_count
                            big_tab.total_price = table_item.total_price
                            big_tab.table = user_table
                            big_tab.save()
                        total += item.productPrice * 20
            debt = Debt.objects.create(
                customer = customer,
                joined = True,
                debt = total,
                date = table_date
            )
            try:
                latest_global_debt = Global_Debt.objects.filter(customer=customer).latest('timeOfCreating')
                newGlobalDebt = Global_Debt.objects.create(
                    customer = customer,
                    date = table_date,
                    debt = latest_global_debt.debt + total
                )
            except:
                newGlobalDebt = Global_Debt.objects.create(
                    customer = customer,
                    date = table_date,
                    debt = total
                )
            total = 0

        debt = Paymant.objects.create(
                customer=customer,
                money= 15000,
                returned = 3000,
                salary = 2000,
                date = today
                )
        latest_global_debt = Global_Debt.objects.filter(customer = customer).latest('timeOfCreating')
        debt_sum = latest_global_debt.debt - debt.money - debt.returned - debt.salary
        old_debt = Old_debt.objects.get(
            customer = customer,
              date = today).debt
        # print(old_debt)
        # print('Hellow')
        weekDebt = Week_debt.objects.create(
            customer = customer,
            date = today,
            debt = debt_sum - old_debt
        )
        gloabalDebt = Global_Debt.objects.create(
            customer = customer,
            debt = debt_sum,
            date = today
        )

    print('Tables created successfully!')

create_tables(today = datetime.date.today(), create=False)
create_tables(today = datetime.date.today() + datetime.timedelta(days=7), create=False)
create_tables(today = datetime.date.today() + datetime.timedelta(days=14), create=False)
create_tables(today = datetime.date.today() + datetime.timedelta(days=21), create=False)
