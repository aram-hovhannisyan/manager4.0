import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()

from tables.models import ItemsModel

def create_items():
    customers = ['all']
    suppliers = ['Կիրովական', 'Արտադրամաս', 'Այլ․ապրանք']

    for i in range(1, 21):
        item = ItemsModel.objects.create(
            customer=customers[0],
            supplier=suppliers[0]                 for j in range(4):
                    item = ItemsModel.objects.create(
                        customer=customer.username,
                        supplier=suppliers[i % 2].username,
                        productName=f'Joined Item {i}{j}-{customer}',
                        productPrice=j * 10
                    ),
            productName=f'item{i}',
            productPrice=i * 10
        )
        item.save()
    for j in range(1, 11):
        item = ItemsModel.objects.create(
            customer=customers[0],
            supplier=suppliers[2],
            productName=f'Ապրանք{j}',
            productPrice=j * 30
        )
    print('Items created successfully!')

# Call the create_items() function
create_items()
