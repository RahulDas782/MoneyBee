# MoneyBee
This is a project made by me and my 4 friends. <a href="https://github.com/CodingCorpse/money-B">Project Link</a>

## Idea
In today's era, Money Management is one of the key features that everyone should be aware of. Often, while we are traveling, going to restaurants with friends we decide to "pool" in the money, an equivalent of splitting when the Payment arrives. Our solution to this problem exploits the fact that no such Bill-Sharing application exists. We use a Shared Database System integrated with RazorPay API, wherein, users can join specific rooms, created by an "admin" or a "master" and then they can pay a specific amount against the corresponding Room ID, once all the payments have been received they are sent to the desired Merchant. Our solution has faster run-time, supports UPI Payments, and has a hassle-free, user-friendly interface. Our architecture includes usage of MySQL, for storing all transaction details, along with the room and the users that have been added in the room till now, we decided to use a database particularly due to the support TCL( Transaction Control Language ).

## Installation and Run
- Firstly install python 3.0 [Download Python 3.0](https://www.python.org/downloads/)
- Then install below dependencies
```
pip install django
pip install django-heroku
pip install psycopg2
pip install razorpay
```
- Type `python manage.py runserver` in terminal. It will start a localhost on your machine.
- Follow the localhost link and open with your browser.
- Eureka moment :-)
