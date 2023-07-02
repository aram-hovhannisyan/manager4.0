import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()
from account.models import User
from django.apps import apps

def clear_database():
    # Get all installed models
    all_models = apps.get_models()

    # Exclude User model
    excluded_models = [User]

    # Iterate over models and delete records
    for model in all_models:
        if model not in excluded_models:
            model.objects.all().delete()

    print('Database cleared successfully!')

clear_database()
