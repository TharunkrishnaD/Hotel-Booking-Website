from django.urls import path
from flight import views

urlpatterns= [
   path('',views.homepage,name="flighthome"),
   path('search_destinations_flight/', views.search_destinations_flight, name='search_destinations_flight'),
   path('one_trip/', views.one_trip, name="one_trip"),
   path('round_trip/',views.round_trip, name="round_trip"),
   path('multitrip/',views.multitrip, name="multitrip"),
   path('flightreview/',views.flightreview, name="flightreview"),
   path('Fare_rule_details/',views.Fare_rule_details,name="Fare_rule_details"),
   path('one_trip_reviewpage/',views.one_trip_reviewpage,name="one_trip_reviewpage"),
   path('onetrip_book/',views.onetrip_book,name="onetrip_book"),
   path('flightpdf/',views.flightpdf, name="flightpdf"),
 


   
   
]