from django.urls import path, include
from .views import (
    # home, 
    save_table_data
)
urlpatterns=[
    # path('', home, name='home'),
    path('', include('account.urls')),
    path('account/', include('account.urls'), name='account'),
    path('save-table-data/', save_table_data, name='saveTableData')
]
