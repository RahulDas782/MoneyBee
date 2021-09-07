from django.contrib import admin
from django.urls import path
from payments import views
 
urlpatterns = [
    path('', views.homepage, name='index'),
    path('createRoom', views.createRoom, name='createRoom'),
    path('joinRoom', views.joinRoom, name='joinRoom'),
    path('confirm', views.confirm, name='confirm'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin/', admin.site.urls),
]