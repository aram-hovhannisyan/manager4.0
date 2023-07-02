import datetime

today = datetime.date.today()
print(today)
for i in range(6):
    table_date = today + datetime.timedelta(days=i)
    print(table_date)