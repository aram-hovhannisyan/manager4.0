import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

customers = ["148", "189", "54", "170", "104", "Էրանոս", "Լիճք", "Մ․ավագ",
            "Մ․1ին", "Զոլ․1ին", "Զոլ․2րդ", "Ծովինար"]
customersPasswords = [
    '148password1234', "189password5678",
    "54password1478", "170password2369",
    "104password2589", "eranospassword3258", 
    "lijqpassword6547", "mavagpassword4569",
    "m1inpassword9654", "zol1inpassword7428",
    "zol2rdpassword9426", "tovinarpassword1463"
                    ]
admins = ['Վակուլ']

# superusers = ['aram']

suppliers = ['Կիրովական', 'Արտադամաս']


def create_users(customers, customersPasswords):

    aram_admin = User.objects.create_superuser(username = 'aram', password= 'aramhovhannisyan')
    aram_admin.save()

    # Create an admin user
    admin_user = User.objects.create_user(username='Վակուլ', password='vakulpassword1236')
    admin_user.is_admin = True
    admin_user.save()

    # Create a customer user

    for customer, password in zip(customers, customersPasswords):
        customer_user = User.objects.create_user(username=customer, password=password)
        customer_user.is_customer = True
        customer_user.save()

    # Create an employee user
    employee_user = User.objects.create_user(username='Վարդգես', password='vardgespassword1234')
    employee_user.is_employee = True
    employee_user.save()

    # Create a supplier user
    supplier_user = User.objects.create_user(username='Արտադրամաս', password='artadramas1258')
    supplier_user.is_supplier = True
    supplier_user.save()

    supplier_user = User.objects.create_user(username='Կիրովական', password='kirovakanpassword4569')
    supplier_user.is_supplier = True
    supplier_user.save()

    supplier_user = User.objects.create_user(username='Այլ.ապրանք', password='aylapranqpassword1793')
    supplier_user.is_supplier = True
    supplier_user.save()
    
create_users(customers, customersPasswords)
