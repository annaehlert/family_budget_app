Family Budget App - it is app for management of family budget. <br />
In this app you can create as many budgets as you can and share it with as many users as you can.<br />
Main elements of an app:
user, family and budgets creation, <br />
modifying of the budget, adding family members, <br />
adding incomes and expenses to chosen budget.
Technologies: <br />
Python 3.7.9, Django Rest Framework

To start the app you need to run below endpoint: <br />
1. download below repo.
2. create virtualenv on your computer. 
3. Download requirements.txt (with command pip install -r requirements.txt). 
4. Then you need to run below commands:
python manage.py makemigrations
python manage.py migrate
5. After all these steps you can run:
python manage.py runserver
and start to work.
If you want to use Django admin:
6. python manage.py createsuperuser
7. Enter your desired username, email and password.
8. After command 
python manage.py runserver and going to "admin/" endpoint you will be able
to login and work on data in database.





