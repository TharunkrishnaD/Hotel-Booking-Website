from django.urls import path
from . import views


urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('send_otp/',views.send_otp,name='send_otp'),
    # path('login_view/',views.login_view,name='login_view'),
    path('signup_view/',views.signup_view,name='signup_view'),
    path('success/',views.success,name='success'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    path('download-pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('check_cancel/',views.check_cancel,name='check_cancel'),
    path('cancel_status/',views.cancel_status,name='cancel_status'),
    path('hotelhistory/',views.hotelhistory,name='hotelhistory'),
    path('hotelcancelled/',views.hotelcancelled,name='hotelcancelled'),
    path('upcominghotel/',views.upcominghotel,name='upcominghotel'),
    path('flightportal/',views.flightportal,name='flightportal'),
    path('portalhome/',views.portalhome,name='portalhome'),
    path('send_pdf_link/', views.send_pdf_link, name='send_pdf_link'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    # path('thanks/',views.signup,name='thanks')
]
