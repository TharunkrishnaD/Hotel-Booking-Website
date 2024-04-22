from django.urls import path
from . import views

urlpatterns= [
   path('',views.home,name="home"),
   path('hotel/', views.hotel, name='hotel'),
   path('hotelreview/',views.hotelreview,name="hotelreview"),
   path('roomdetails/<str:hotelCode>/<str:traceId>/<str:resultIndex>/<str:tokenId>/',views.roomdetails,name="roomdetails"),
   path('search_destinations/', views.search_destinations, name='search_destinations'),
   path('hotellist', views.process_form, name='process_form'),
   path('get_room_details/', views.get_room_details, name='get_room_details'),
   path('your_view/', views.your_view, name='your_view'),
   # path('review', views.review, name='review'),
]