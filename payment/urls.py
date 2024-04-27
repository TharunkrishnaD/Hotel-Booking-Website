
from django.urls import path
from . import views


urlpatterns = [
    path('payment/', views.home, name='home'),
    path('payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('paymentflight/', views.paymentflight, name='paymentflight'),
    path('paymentflight/Flightpaymenthandler/', views.Flightpaymenthandler, name='Flightpaymenthandler'),
    # path('payment/success',views.success,name='success')
]