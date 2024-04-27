from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from datetime import datetime
import json
import math
import ast
from .models import AirportList
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import HTTPError
from datetime import timedelta
from datetime import datetime, timedelta
import pdfkit
import razorpay
from django.shortcuts import render
from signup.models import Userdetails
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
import hashlib
import random
import datetime
from django.utils.timezone import make_aware
import json
from requests.exceptions import HTTPError
from django.http import JsonResponse
import requests
from django.conf import settings
from email.mime.text import MIMEText
import smtplib
# Login and signups
from django.shortcuts import render
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.http import HttpResponse
import smtplib
from django.contrib.auth import logout
import pdfkit


def homepage(request):
    return render(request, 'flight/flighthomepage.html')
def flightpdf(request):
    return render(request, 'flight/flightpdf.html')



def search_destinations_flight(request):
    query = request.GET.get('query', '')
    results = AirportList.objects.filter(
        Q(CITYNAME__icontains=query) | Q(COUNTRYNAME__icontains=query) | Q(AIRPORTNAME__icontains=query) | Q(AIRPORTCODE__icontains=query)
    )[:10]

    data = [
        {
            'label': result.AIRPORTNAME + '( ' + result.CITYNAME + ','+ result.COUNTRYNAME +','+ result.AIRPORTCODE +')',
            'value': result.AIRPORTNAME+ '( ' + result.CITYNAME + ','+ result.COUNTRYNAME +','+ result.AIRPORTCODE +')',
            'cityCode': result.CITYCODE,
            'AirportCode': result.AIRPORTCODE,
            'CityName' : result.CITYNAME
        }
        for result in results
    ]

    return JsonResponse({'data': data})




def one_trip(request):
    if request.method == 'GET':
        FromAirportCode = request.GET.get('fromAirportCode', '')
        ToAirportCode = request.GET.get('toAirportCode', '')
        from_onetrip = request.GET.get('from-one-trip', '')
        to_onetrip = request.GET.get('to-one-trip', '')  # Corrected variable name
        fromcityname = request.GET.get('fromcityname', '')
        tocityname = request.GET.get('tocityname','')
        Departure_date_onetrip = request.GET.get('check-in', '')
        print(Departure_date_onetrip)
        onee_trip = request.GET.get('classes', '')
        no_of_adults = request.GET.get('Adults', '')
        no_of_chaild = request.GET.get('Childs', '')
        no_of_infant = request.GET.get('Infants', '')
        DirectFlight = request.GET.get('resultdir','')
        print("classsssssssssssssssssssssssssssssssssssssssss",onee_trip)
        guest_details = f"{no_of_adults} adults,{no_of_chaild} Children,{no_of_infant} infants"
        print(guest_details)
        member_details = []
        PER_COUNT = {
            "adult": no_of_adults,
            "child": no_of_chaild, 
            "infant": no_of_infant,
        }
       
        member_details.append(PER_COUNT)
        print(member_details)
        room_json_array_string = json.dumps(member_details)

        # guest_details = f"{no_of_adults} Adults,{no_of_chaild} Childs,{no_of_infant} Infant"
        
        date_object = datetime.strptime(Departure_date_onetrip, '%d %B %Y')

# Convert datetime object to desired format
        formatted_date = date_object.strftime('%Y-%m-%dT%H:%M:%S')
        # input_date = datetime.strptime(Departure_date_onetrip, '%Y-%m-%d')
        # Departuredateonetrip = input_date.strftime('%Y-%m-%dT%H:%M:%S')
        # print("output :",Departuredateonetrip)

        print(fromcityname,tocityname,formatted_date )

        DirectFlight_bool = DirectFlight.lower() == "true"
        print(DirectFlight_bool)
        print(type(DirectFlight_bool))

        
        # request.session['start_place'] = from_onetrip  # Corrected variable name
        # request.session['end_place'] = to_onetrip
        request.session['member_details'] = room_json_array_string
        # request.session['adults'] = no_of_adults
        # request.session['childs'] = no_of_chaild
        # request.session['infant'] = no_of_infant

        url = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate'  # Removed extra space

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'ClientId': "ApiIntegrationNew",
            'UserName': "Vacation",
            'Password': "Feast@123456",
            'EndUserIp': "192.168.11.120",
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            if response.status_code == 200:
                api_data = response.json()

            if response_data.get('TokenId', None):  # Corrected key name
                token = response_data['TokenId']
                print("Authentication successful. Token:", token)

                # search for flight
                api_url = 'http://api.tektravels.com'
                api_key = 'Feast@123456'
                EndUserIp = "192.168.11.120"
                one_trip_class=f"{onee_trip}"
                
                numadult = f"{no_of_adults}"
                numchaild = f"{no_of_chaild}"
                numinfant = f"{no_of_infant}"
                DirectFlight = DirectFlight_bool
                OneStopFlight = False
                PreferredAirlines = None
                JourneyType = "1"
                sources = None
                
                
                Segments = [
                    {
                        'Origin': f"{FromAirportCode}",
                        'Destination': f"{ToAirportCode}",
                        'FlightCabinClass': f"{one_trip_class}",
                        'PreferredDepartureTime':  formatted_date,
                        'PreferredArrivalTime':  formatted_date,
                    }
                ]
                
                token_id = f"{token}"
                print(DirectFlight)
                print(type(DirectFlight))

                



                flight_info = get_flight_results( api_key,EndUserIp,token_id, numadult,numchaild, numinfant, DirectFlight,OneStopFlight,JourneyType,PreferredAirlines,Segments,sources)
                # print(".........................................................",flight_info)
                # return render(request, 'flight/oneway.html', {'flight_info': flight_info})

                FLight_list = json.dumps(flight_info)
                print(FLight_list)
                if flight_info  is not None:
                    flight_price = flight_info
                    
                    if isinstance(flight_price,list) :
                        all_prices = []
                        for flight in flight_price:
                            all_prices.append(flight.get('OffredFare'))
                        
                        valid_prices = [price for price in all_prices if price is not None]
                        # print(all_prices)

                        if not valid_prices :
                            min_price = 0
                            max_price = 1
                            error_message = 'No flight available'
                            return render(request, 'flight/oneway.html', {'error_message':error_message,'min_price': min_price, 'max_price': max_price,'date_object':date_object})
                        else:
                            # valid_prices = [price for price in flight_prices if price is not None]
                            min_price = min(valid_prices)
                            max_price = max(valid_prices)
                            print(min_price,max_price)

                            error_message = None
                            return render(request, 'flight/oneway.html', {'flight_info': flight_info, 'flight_class': one_trip_class,'FLight_list':FLight_list,
                                                'fromAircode': FromAirportCode, 'toAircode': ToAirportCode,'token_id': token_id,
                                                'fromcityname': fromcityname, 'tocityname':tocityname,'max_price':max_price,'min_price':min_price,'Departure_date':Departure_date_onetrip,'NoOfAdults':numadult,'NoOfChild':numchaild,'NoOfInfant':numinfant,'date_object':date_object})                   
                    else:
                        error_message = "Flight information is not in the expected format"
                        return render(request, 'flight/error.html', {'error_message': error_message})
                else:
                   error_message = "Error occurred during the flight search request"
                   return render(request, 'flight/error.html', {'error_message': error_message})
            else:
                print("Authentication failed:", response_data)
                return HttpResponse("Authentication failed:", response_data)
        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
    return HttpResponse("Error processing the form.")
    


def get_flight_results(api_key,EndUserIp,token_id, numadult,numchaild, numinfant, DirectFlight,OneStopFlight,JourneyType,PreferredAirlines,Segments,sources):
    
    
    url ='http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Search'
    
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'EndUserIp': EndUserIp,
        'TokenId': token_id,
        'AdultCount': numadult,
        'ChildCount': numchaild,
        'InfantCount': numinfant,
        'DirectFlight': DirectFlight,
        'OneStopFlight': OneStopFlight,
        'JourneyType': JourneyType,
        'PreferredAirlines': PreferredAirlines,
        'Segments': Segments,
        'Sources': sources
    }
    print(data)

    try:
        response = requests.post(url, json=data, headers=headers,params = {'apiKey': api_key})
        response.raise_for_status()

        print("status code:", response.status_code)

        response_data = response.json()

        if 'Response' in response_data:
       
            results = response_data['Response']
       
            flight_info = []
            trace_id = results.get('TraceId', '')
            print("TraceId:", trace_id)
           
            array_count_1 = []
            array_count_2 = []
            for result_list in response_data["Response"]["Results"]:
                for result in result_list:
                    segments = result.get("Segments", [])[0]
                    if len(segments) == 1:
                        array_count_1.append({"list1" : result})
                    elif len(segments) == 2:
                        array_count_2.append({"list2" : result})

        
            for flight in array_count_1:
                segments = flight['list1']['Segments']
                fare_classification = flight['list1'].get('FareClassification', {})
                fare_breakdown = flight['list1'].get('FareBreakdown',[])
                
                for segment in segments:
                    for sub_segment in segment:
                        list_of_nonstopFlight = {
                            "AirlineType": fare_classification.get("Type"),
                            "AirlineCode": sub_segment.get("Airline", {}).get("AirlineCode"),
                            "AirlineName": sub_segment.get("Airline", {}).get("AirlineName"),
                            "AirlineNumber": sub_segment.get("Airline", {}).get("FlightNumber"),
                            "OrginAirportCode": sub_segment.get("Origin", {}).get('Airport', {}).get('AirportCode'),
                            "OrginAirportName": sub_segment.get("Origin", {}).get('Airport', {}).get('AirportName'),
                            "OrginAirportCityName": sub_segment.get("Origin", {}).get('Airport', {}).get('CityName'),
                            "OrginAirportCoutryName": sub_segment.get("Origin", {}).get('Airport', {}).get('CountryName'),
                            "OrginAirportTerminal": sub_segment.get("Origin", {}).get('Airport', {}).get('Terminal'),
                            "OrginAirportDeptime": sub_segment.get("Origin", {}).get('DepTime'),
                            "DestinationAirportCode": sub_segment.get("Destination", {}).get('Airport', {}).get('AirportCode'),
                            "DestinationAirportName": sub_segment.get("Destination", {}).get('Airport', {}).get('AirportName'),
                            "DestinationCityName": sub_segment.get("Destination", {}).get('Airport', {}).get('CityName'),
                            "DestinationCountryName": sub_segment.get("Destination", {}).get('Airport', {}).get('CountryName'),
                            "DestinationTerminal": sub_segment.get("Destination", {}).get('Airport', {}).get('Terminal'),
                            "DestinationDeptime": sub_segment.get("Destination", {}).get('ArrTime'),
                            "setsAvailable": sub_segment.get('NoOfSeatAvailable'),
                            "checkinbag": sub_segment.get('Baggage'),
                            "combainbag": sub_segment.get('CabinBaggage'),

                            "OffredFare": flight['list1']['Fare'].get('OfferedFare'),
                            "PublishedFare": flight['list1']['Fare'].get('PublishedFare'),
                            "discount1": flight['list1']['Fare'].get('CommissionEarned'),
                            "discount2": flight['list1']['Fare'].get('PLBEarned','0'),
                            "AdditionalTxnFeePub": flight['list1']['Fare'].get('AdditionalTxnFeePub','0'),
                            "OtherCharges": flight['list1']['Fare'].get('OtherCharges','0'),
                            "ServiceFee": flight['list1']['Fare'].get('ServiceFee','0'),
                            "AirlineTransFee": flight['list1']['Fare'].get('AirlineTransFee','0'),
                            "IncentiveEarned": flight['list1']['Fare'].get('IncentiveEarned','0'),
                            

                            "ResultIndex": flight['list1'].get('ResultIndex'),
                            "TraceId": trace_id,
                            
                        }
                        suffixes = ['A', 'B', 'C']
                        for suffixes, fare_info in zip(suffixes,fare_breakdown):
                            list_of_nonstopFlight[f"{suffixes}PassengerCount"] = fare_info.get('PassengerCount', '')
                            list_of_nonstopFlight[f"{suffixes}PassengerType"] = fare_info.get('PassengerType', '')
                            list_of_nonstopFlight[f"{suffixes}BaseFare"] = fare_info.get('BaseFare', '')
                            list_of_nonstopFlight[f"{suffixes}Tax"] = fare_info.get('Tax', '')

                        flight_info.append(list_of_nonstopFlight)

                    
                        flight_class = sub_segment.get('CabinClass')
                        # print(flight_class)
                        flight_class_mapping = {
                            2: "Economy",
                            3: "PremiumEconomy",
                            4: "Business",
                            5: "PremiumBusiness",
                            6: "First"
                        }
                        list_of_nonstopFlight["FlightClass"] = flight_class_mapping.get(flight_class, "Unknown")


                        #stops
                        list_of_nonstopFlight["Stopconformation"] = "Non-stop"

                        #refund or not refund
                        refund_ = flight['list1'].get('IsRefundable')
                        if refund_:
                            list_of_nonstopFlight["nonrefund"] = 'Refundable'
                        else:
                            list_of_nonstopFlight["nonrefund"] = 'Not Refundable'

                        #departure deptime convert to hour ans minute
                        date_time_departure = sub_segment.get("Origin", {}).get('DepTime')
                        departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
                        departurehoure = str(departure_time.hour).zfill(2)
                        departureminute = str(departure_time.minute).zfill(2)
                        list_of_nonstopFlight["departurehoure"]= departurehoure
                        list_of_nonstopFlight["departureminute"]=departureminute
                        departure_H_M = f"{departurehoure}:{departureminute}"
                        list_of_nonstopFlight["departure_H_M"] = departure_H_M

                        # -------------------------
                        # input_date_time = '2024-01-31T09:00:00'
                        datetime_obj = datetime.fromisoformat(date_time_departure)
                        formatted_date = datetime_obj.strftime("%a, %d %b")
                        list_of_nonstopFlight["start_date"] = formatted_date

                        # #arrival arrtime convert to hour and minute
                        date_time_arrival = sub_segment.get("Destination", {}).get('ArrTime')
                        arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
                        arrivalhoure =  str(arrival_time.hour).zfill(2)
                        arrivalminute =  str(arrival_time.minute).zfill(2)
                        list_of_nonstopFlight["arrivalhoure"]=arrivalhoure
                        list_of_nonstopFlight["arrivalminute"] =arrivalminute
                        arrival_H_M = f"{arrivalhoure}:{arrivalminute}"
                        list_of_nonstopFlight["arrival_H_M"] = arrival_H_M

                        # # total hours of traval
                        flight_time = arrival_time - departure_time
                        total_hour = flight_time.seconds // 3600
                        total_minute = (flight_time.seconds % 3600) // 60
                        list_of_nonstopFlight["totalhour"]=total_hour
                        list_of_nonstopFlight["totalminute"]=total_minute
                        total_H_M = f"{total_hour}h {total_minute}m"
                        list_of_nonstopFlight["total_H_M"] = total_H_M
                        # list_of_nonstopFlight["totalminute"] = total_minute
                # print("fareamount details",fare_brake_down)
              
                    
            for flight in array_count_2:
                segments = flight['list2']['Segments']
                fare_classification_two = flight['list2'].get('FareClassification', {})
                fare_breakdown_two = flight['list2'].get('FareBreakdown',[])
                if segments:
                    first_segment = segments[0][0]
                    second_segment = segments[0][1]
                    

                    list_of_onestopFlight = {
                        "AirlineType" : fare_classification_two.get("Type"),
                        "FirstAirlineCode" : first_segment.get('Airline',{}).get('AirlineCode'),
                        "FirstAirlineName" : first_segment.get("Airline", {}).get("AirlineName"),
                        "AirlineNumber" : first_segment.get("Airline", {}).get("FlightNumber"),
                        "FristOrginAirportCode":  first_segment.get("Origin", {}).get('Airport',{}).get('AirportCode'),
                        "FristOrginAirportName" :  first_segment.get("Origin", {}).get('Airport',{}).get('AirportName'),
                        "FristOrginAirportCityName" :  first_segment.get("Origin", {}).get('Airport',{}).get('CityName'),
                        "FristOrginAirportCoutryName" :  first_segment.get("Origin", {}).get('Airport',{}).get('CountryName'),
                        "FristOrginAirportTerminal" :  first_segment.get("Origin", {}).get('Airport',{}).get('Terminal'),
                        "FristOrginAirportDeptime" : first_segment.get("Origin", {}).get('DepTime'),
                        "FristDestinationAirportCode" : first_segment.get("Destination", {}).get('Airport',{}).get('AirportCode'),
                        "FristDestinationAirportName" : first_segment.get("Destination", {}).get('Airport',{}).get('AirportName'),
                        "FristDestinationCityName" : first_segment.get("Destination", {}).get('Airport',{}).get('CityName'),
                        "FristDestinationCountryName" : first_segment.get("Destination", {}).get('Airport',{}).get('CountryName'),
                        "FristDestinationTerminal" : first_segment.get("Destination", {}).get('Airport',{}).get('Terminal'),
                        "FristDestinationDeptime" : first_segment.get("Destination", {}).get('ArrTime'),
                        "SecondAirlineCode" : second_segment.get('Airline',{}).get('AirlineCode'),
                        "SecondAirlineName" :second_segment.get('Airline',{}).get('AirlineName'),
                        "SAirlineNumber" : second_segment.get("Airline", {}).get("FlightNumber"),
                        "SecondOrginAirportCode":  second_segment.get("Origin", {}).get('Airport',{}).get('AirportCode'),
                        "SecondOrginAirportName" :  second_segment.get("Origin", {}).get('Airport',{}).get('AirportName'),
                        "SecondOrginAirportCityName" :  second_segment.get("Origin", {}).get('Airport',{}).get('CityName'),
                        "SecondOrginAirportCoutryName" :  second_segment.get("Origin", {}).get('Airport',{}).get('CountryName'),
                        "SecondOrginAirportTerminal" :  second_segment.get("Origin", {}).get('Airport',{}).get('Terminal'),
                        "SecondOrginAirportDeptime" : second_segment.get("Origin", {}).get('DepTime'),
                        "SecondDestinationAirportCode" : second_segment.get("Destination", {}).get('Airport',{}).get('AirportCode'),
                        "SecondDestinationAirportName" : second_segment.get("Destination", {}).get('Airport',{}).get('AirportName'),
                        "SecondDestinationCityName" : second_segment.get("Destination", {}).get('Airport',{}).get('CityName'),
                        "SecondDestinationCountryName" : second_segment.get("Destination", {}).get('Airport',{}).get('CountryName'),
                        "SecondDestinationTerminal" : second_segment.get("Destination", {}).get('Airport',{}).get('Terminal'),
                        "SecondDestinationDeptime" : second_segment.get("Destination", {}).get('ArrTime'),
                        "FristsetsAvailable" : first_segment.get('NoOfSeatAvailable'),
                        "SecondsetsAvailable" : second_segment.get('NoOfSeatAvailable'),
                        "Fristcheckinbag" : first_segment.get('Baggage'),
                        "Fristcombainbag" : first_segment.get('CabinBaggage'),
                        "Secondcheckinbag" : second_segment.get('Baggage'),
                        "Secondcombainbag" : second_segment.get('CabinBaggage'),

                        "OffredFare" : flight['list2']['Fare'].get('OfferedFare'),
                        "PublishedFare": flight['list2']['Fare'].get('PublishedFare'),
                        "discount1": flight['list2']['Fare'].get('CommissionEarned'),
                        "discount2": flight['list2']['Fare'].get('PLBEarned'),
                        "AdditionalTxnFeePub": flight['list2']['Fare'].get('AdditionalTxnFeePub','0'),
                        "OtherCharges": flight['list2']['Fare'].get('OtherCharges','0'),
                        "ServiceFee": flight['list2']['Fare'].get('ServiceFee','0'),
                        "AirlineTransFee": flight['list2']['Fare'].get('AirlineTransFee','0'),
                        "IncentiveEarned": flight['list2']['Fare'].get('IncentiveEarned','0'),

                        "ResultIndex" : flight['list2'].get('ResultIndex'),
                       
                        "TraceId" :trace_id,
                        }
                    suffixes = ['A', 'B', 'C']
                    for suffixes, fare_info in zip(suffixes,fare_breakdown_two):
                        list_of_onestopFlight[f"{suffixes}PassengerCount"] = fare_info.get('PassengerCount', '')
                        list_of_onestopFlight[f"{suffixes}PassengerType"] = fare_info.get('PassengerType', '')
                        list_of_onestopFlight[f"{suffixes}BaseFare"] = fare_info.get('BaseFare', '')
                        list_of_onestopFlight[f"{suffixes}Tax"] = fare_info.get('Tax', '')
                    
                    flight_info.append(list_of_onestopFlight)
                    

                    list_of_onestopFlight["Stopconformation"] = "1-stop(s)"


                    # flight classes code
                    flightclass1 = first_segment.get('CabinClass')
                    flightclass2 = second_segment.get('CabinClass')
                    # print(flightclass1)
                    flight_class_mapping = {
                        2: "Economy",
                        3: "PremiumEconomy",
                        4: "Business",
                        5: "PremiumBusiness",
                        6: "First"
                    }
                    list_of_onestopFlight["FlightClass"] = flight_class_mapping.get(flightclass1, "Unknown")
                    list_of_onestopFlight["SecondFlightClass"] = flight_class_mapping.get(flightclass2, "Unknown")


                    #refund or not refund
                    refund_ = flight['list2'].get('IsRefundable')
                    if refund_:
                        list_of_onestopFlight["onerefund"] = 'Refundable'
                    else:
                        list_of_onestopFlight["onerefund"] = 'Not Refundable'

                    #departure deptime convert to hour ans minute
                    date_time_departure = first_segment.get("Origin", {}).get('DepTime')
                    departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
                    Firstdeparturehoure = str(departure_time.hour).zfill(2)
                    Firstdepartureminute = str(departure_time.minute).zfill(2)
                    list_of_onestopFlight["Firstdeparturehoure"]= Firstdeparturehoure
                    list_of_onestopFlight["Firstdepartureminute"]=Firstdepartureminute
                    Firstdeparture_H_M = f"{Firstdeparturehoure}:{Firstdepartureminute}"
                    list_of_onestopFlight["Firstdepartur_H_M"] = Firstdeparture_H_M 
                    # -----------------------
                    datetime_obj = datetime.fromisoformat(date_time_departure)
                    formatted_date = datetime_obj.strftime("%a, %d %b")
                    list_of_onestopFlight["Firstdstart_date"] = formatted_date

                    # #arrival arrtime convert to hour and minute
                    date_time_arrival = first_segment.get("Destination", {}).get('ArrTime')
                    arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
                    Firstarrivalhoure =  str(arrival_time.hour).zfill(2)
                    Firstarrivalminute =  str(arrival_time.minute).zfill(2)
                    list_of_onestopFlight["Firstarrivalhoure"]= Firstarrivalhoure
                    list_of_onestopFlight["Firstarrivalminute"]=Firstarrivalminute

                    Firstarrival_H_M = f"{Firstarrivalhoure}:{Firstarrivalminute}"
                    list_of_onestopFlight["Firstarrival_H_M"] = Firstarrival_H_M

                    # # total hours of traval
                    flight_time = arrival_time - departure_time
                    total_hour = flight_time.seconds // 3600
                    total_minute = (flight_time.seconds % 3600) // 60
                    list_of_onestopFlight["Firsttotalhour"]= total_hour
                    list_of_onestopFlight["Firsttotalminute"]=total_minute
                    total_H_M = f"{total_hour}h {total_minute}m"
                    list_of_onestopFlight["Firsttotal_H_M"] = total_H_M
    # -------------------------------------------------------------------------------------------------------------
                    #departure deptime convert to hour ans minute
                    date_time_departures = second_segment.get("Origin", {}).get('DepTime')
                    departure_times = datetime.strptime(date_time_departures, "%Y-%m-%dT%H:%M:%S")
                    Sconddeparturehoure = str(departure_times.hour).zfill(2)
                    Sconddepartureminute = str(departure_times.minute).zfill(2)
                    Sconddeparture_H_M = f"{Sconddeparturehoure}:{Sconddepartureminute}"
                    list_of_onestopFlight["Sconddeparture_H_M"] = Sconddeparture_H_M

                    # #arrival arrtime convert to hour and minute
                    date_time_arrivals = second_segment.get("Destination", {}).get('ArrTime')
                    arrival_times = datetime.strptime(date_time_arrivals, "%Y-%m-%dT%H:%M:%S")
                    Scondarrivalhoure =  str(arrival_times.hour).zfill(2)
                    Scondarrivalminute =  str(arrival_times.minute).zfill(2)
                    Scondarrival_H_M = f"{Scondarrivalhoure}:{Scondarrivalminute}"
                    list_of_onestopFlight["Scondarrival_H_M"] = Scondarrival_H_M

                    # # total hours of traval
                    flight_times = arrival_times - departure_times
                    total_hours = flight_times.seconds // 3600
                    total_minutes = (flight_times.seconds % 3600) // 60
                    total_H_Ms = f"{total_hours}h {total_minutes}m"
                    list_of_onestopFlight["Scondtotal_H_M"] = total_H_Ms

                    final_flight_times = arrival_times - departure_time
                    # total_seconds = final_flight_times.total_seconds()
                    # final_total_hours = int(total_seconds // 3600)
                    final_total_hours = final_flight_times.seconds // 3600
                    final_total_minutes = (final_flight_times.seconds % 3600) // 60
                    total_H_Ms = f"{final_total_hours}h {final_total_minutes}m"
                    list_of_onestopFlight["FinalTotal_H_M"] = total_H_Ms


            # print(array_count_2)
            # print(flight_info)
            return flight_info
        else:
            # Handle the case where 'Response' key is not found
            error_message = "No 'Response' key found in response data."
            return None, None, error_message

    except ValueError as ve:
        print(f"Error decoding JSON: {ve}")
    # Handle JSON decoding error, return an appropriate HTTP response or render an error page.
    except KeyError as ke:
        if str(ke) == "'Results'":
            # Handle the case where 'Results' key is not found
            error_message = "No 'Results' key found in response data."
            return None, None, error_message
        else:
            print(f"KeyError: {ke}")
            # Handle other KeyError if necessary
    
def Fare_rule_details(request):
    
        # Extracting flight details
        token_id = request.POST.get('tokenId', None)
        trace_id = request.POST.get('traceId', None)
        result_index = request.POST.get('resultIndex', None)
        
# Storing session data for both flight and room
        # request.session['trace_id'] = trace_id
        # request.session['token_id'] = token_id
        # request.session['result_index'] = result_index
        print("fare details names",trace_id,result_index,token_id)
  

        # Flight API URLs and data
        flight_api_url = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/FareRule'
        flight_data = {
            "EndUserIp": "192.168.11.120",
            "TokenId": token_id,
            "TraceId": trace_id,
            "ResultIndex": result_index,
        }

       
        try:
            # Fetching flight details
            flight_response = requests.post(flight_api_url, json=flight_data)
            flight_response.raise_for_status()
 
            flight_details = flight_response.json()
            print(flight_details)
            #  response_data2 = response2.json()
            flight_rooms_html = []

            fare_rule_detail = flight_details["Response"]["FareRules"][0]
            # print(fare_rule_detail)
            faredeatils= fare_rule_detail.get('FareRuleDetail')
            combination_html = []
            flight_rule = f"""
                    
                    <div>{faredeatils}
                       
                    </div>

            """
            combination_html.append(flight_rule)

            combination_html_joined =''.join(combination_html)
        

           

           
            return JsonResponse({'fare_details_html': combination_html_joined})

            # combined_response = {
            #     'faredeatils': fare_rule_detail.get('FareRuleDetail')
            # }
            # flight_rooms_html.append(combined_response)
            # print(flight_rooms_html)
            # return JsonResponse(combined_response)

        except requests.exceptions.RequestException as ex:
            return JsonResponse({'error': str(ex)}, status=500)

    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def flightreview (request):
    if request.method == 'POST':
        # EndUserIp = request.POST.get('EndUserIp', None)
        trace_id = request.POST.get('traceId', None)
        result_index = request.POST.get('resultIndex', None)
        token_id = request.POST.get('tokenId', None)
        flight_stop = request.POST.get('flightstops',None)
        flight_class = request.POST.get('flightclass',None)
        flight_date = request.POST.get('flightdate',None)
        flight_H_M = request.POST.get('flighttodal_h_m',None)
        start_point = request.POST.get('flightstartpoint',None)
        end_point = request.POST.get('flightendpoint',None)
        Airline_code = request.POST.get('Airlinecode',None)
        # user_information_json = request.POST.get('user_information', None)
        # user_information = json.loads(user_information_json)
        # print(user_information)
        request.session['token_id'] = token_id
        request.session['trace_id'] = trace_id
        request.session['result_index'] = result_index  
        print(trace_id,result_index,token_id, flight_stop,flight_class,flight_date,Airline_code)
        
        single_flight_del = {
            "flight_stop":flight_stop,
            "flight_class" :flight_class,
            "start_point":start_point,
            "end_point":end_point,
            "flight_date":flight_date,
            "flight_H_M":flight_H_M,
        }
        totalflightlist = json.dumps(single_flight_del)
        guest_details = request.session.get('member_details', [])
        print("preview page:", guest_details)
        # new_contect=json.dumps(guest_details)

        

    # def FARE_QUOTE(trace_id,EndUserIp,token_id,result_index):
        api_url_1 = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/FareQuote'


        headers1 = {
            'Content-Type': 'application/json',
        }

        data1 = {
        "EndUserIp":"192.168.11.120",
        "TokenId": f"{token_id}",
        "TraceId": f"{trace_id}",
        "ResultIndex": f"{result_index}"
        }
        
        try:
            response1 = requests.post(api_url_1, json=data1, headers=headers1)
            response1.raise_for_status()
            print("status code:", response1.status_code)

            # traveler_details = json.loads(request.body)
            # print(traveler_details)


            response_data1 = response1.json()
            print(response_data1)

            flight_name =[]
            
            flight_details = []
            # request.session['flight_details'] = flight_details

            results = response_data1["Response"]["Results"]
            fare_breakdown = response_data1["Response"]["Results"]["FareBreakdown"]

            fare ={
                "Currency": results.get('Fare',{}).get('Currency'),
                "BaseFare" : results.get('Fare',{}).get('BaseFare'),
                "Tax" : results.get('Fare',{}).get('Tax'),
                "YQTax" : results.get('Fare',{}).get('YQTax'),
                "AdditionalTxnFeePub" : results.get('Fare',{}).get('AdditionalTxnFeePub'),
                "AdditionalTxnFeeOfrd" : results.get('Fare',{}).get('AdditionalTxnFeeOfrd'), 
                "OtherCharges": results.get('Fare',{}).get('OtherCharges'),
                "Discount" : results.get('Fare',{}).get('Discount'),
                "PublishedFare" : results.get('Fare',{}).get('PublishedFare'),
                "OfferedFare" : results.get('Fare',{}).get('OfferedFare'),
                "TdsOnCommission" : results.get('Fare',{}).get('TdsOnCommission'),
                "TdsOnPLB" : results.get('Fare',{}).get('TdsOnPLB'),  
                "TdsOnIncentive" : results.get('Fare',{}).get('TdsOnIncentive'),
                "ServiceFee" : results.get('Fare',{}).get('ServiceFee'),  
            }
            print(fare)
            request.session['fare_details'] = fare 
            # adult= []
            # chaild = []
            # infant = []
            # for fare in fare_breakdown:
            #     if fare["PassengerType"] == 1:
            #         new={
            #             "PassengerType":fare.get('PassengerType'),"Currency" : fare.get('Currency'),
            #             "BaseFare" : fare.get('BaseFare'),
            #             "Tax" : fare.get('Tax'),
            #             "YQTax" : fare.get('YQTax'),
            #             "AdditionalTxnFeePub" : fare.get('AdditionalTxnFeePub'),
            #             "AdditionalTxnFeeOfrd" : fare.get('AdditionalTxnFeeOfrd'),
            #             "PublishedFare": results.get('Fare',{}).get('PublishedFare'),
            #             "OffredFare" : results.get('Fare',{}).get('OfferedFare'),
            #             "TdsOnCommission" : results.get('Fare',{}).get('TdsOnCommission'),
            #             "TdsOnPLB" : results.get('Fare',{}).get('TdsOnPLB'),
            #             "TdsOnIncentive" : results.get('Fare',{}).get('TdsOnIncentive'),
            #             "ServiceFee" : results.get('Fare',{}).get('ServiceFee'),
                      
            #         }
            #         adult.append(new)
            #     elif fare["PassengerType"] == 2:
            #         new={"PassengerType":fare.get('PassengerType'),
            #             "Currency" : fare.get('Currency'),
            #             "BaseFare" : fare.get('BaseFare'),
            #             "Tax" : fare.get('Tax'),
            #             "YQTax" : fare.get('YQTax'),
            #             "AdditionalTxnFeePub" : fare.get('AdditionalTxnFeePub'),
            #             "AdditionalTxnFeeOfrd" : fare.get('AdditionalTxnFeeOfrd'),
            #             "PublishedFare": results.get('Fare',{}).get('PublishedFare'),
            #             "OffredFare" : results.get('Fare',{}).get('OfferedFare'),
            #             "TdsOnCommission" : results.get('Fare',{}).get('TdsOnCommission'),
            #             "TdsOnPLB" : results.get('Fare',{}).get('TdsOnPLB'),
            #             "TdsOnIncentive" : results.get('Fare',{}).get('TdsOnIncentive'),
            #             "ServiceFee" : results.get('Fare',{}).get('ServiceFee'),
            #         }
            #         chaild.append(new)
            #     elif fare["PassengerType"] == 3:
            #         new={
            #             "PassengerType":fare.get('PassengerType'),"Currency" : fare.get('Currency'),
            #             "BaseFare" : fare.get('BaseFare'),
            #             "Tax" : fare.get('Tax'),
            #             "YQTax" : fare.get('YQTax'),
            #             "AdditionalTxnFeePub" : fare.get('AdditionalTxnFeePub'),
            #             "AdditionalTxnFeeOfrd" : fare.get('AdditionalTxnFeeOfrd'),
            #             "PublishedFare": results.get('Fare',{}).get('PublishedFare'),
            #             "OffredFare" : results.get('Fare',{}).get('OfferedFare'),
            #             "TdsOnCommission" : results.get('Fare',{}).get('TdsOnCommission'),
            #             "TdsOnPLB" : results.get('Fare',{}).get('TdsOnPLB'),
            #             "TdsOnIncentive" : results.get('Fare',{}).get('TdsOnIncentive'),
            #             "ServiceFee" : results.get('Fare',{}).get('ServiceFee'),
            #         }
            #         infant.append(new)

            # print("Adult Fare:", adult)
            # print("Child Fare:", chaild)
            # print("Infant Fare:", infant)
        

            # print("thet is the .....................",results)
            segment_1 = response_data1["Response"]["Results"]["Segments"][0][0]
            # print("thet is the .....................",segments)
            # global error_message
            F_C_name ={
            "F_OrgCityName": segment_1.get("Origin", {}).get('Airport',{}).get('CityName'),
            "F_DesCityName" : segment_1.get("Destination", {}).get('Airport',{}).get('CityName'),
            "AirlineCode": segment_1.get("Airline", {}).get("AirlineCode"),
            "AirlineName" : segment_1.get("Airline", {}).get("AirlineName"),
            "AirlineNumber" : segment_1.get("Airline", {}).get("FlightNumber"),
            }
            flight_name.append(F_C_name) 


            error_message = response_data1['Response']['Error']['ErrorMessage']
            
            Flight_details = {
                "ResultIndex": results.get("ResultIndex"),
                "AirlineCode": segment_1.get("Airline", {}).get("AirlineCode"),
                "AirlineName" : segment_1.get("Airline", {}).get("AirlineName"),
                "AirlineNumber" : segment_1.get("Airline", {}).get("FlightNumber"),
                "OrginAirportCode":  segment_1.get("Origin", {}).get('Airport',{}).get('AirportCode'),
                "OrginAirportName" :  segment_1.get("Origin", {}).get('Airport',{}).get('AirportName'),
                "OrginAirportCityName" :  segment_1.get("Origin", {}).get('Airport',{}).get('CityName'),
                "OrginAirportCoutryName" :  segment_1.get("Origin", {}).get('Airport',{}).get('CountryName'),
                "OrginAirportTerminal" :  segment_1.get("Origin", {}).get('Airport',{}).get('Terminal'),
                "OrginAirportDeptime" : segment_1.get("Origin", {}).get('DepTime'),
                "DestinationAirportCode" : segment_1.get("Destination", {}).get('Airport',{}).get('AirportCode'),
                "DestinationAirportName" : segment_1.get("Destination", {}).get('Airport',{}).get('AirportName'),
                "DestinationCityName" :segment_1.get("Destination", {}).get('Airport',{}).get('CityName'),
                "DestinationCountryName" : segment_1.get("Destination", {}).get('Airport',{}).get('CountryName'),
                "DestinationTerminal" : segment_1.get("Destination", {}).get('Airport',{}).get('Terminal'),
                "DestinationDeptime" : segment_1.get("Destination", {}).get('ArrTime'),
                # "FsetsAvailable" : segments[0].get('NoOfSeatAvailable'),
                "checkinbag" : segment_1.get('Baggage'),
                "combainbag" : segment_1.get('CabinBaggage'),
                

                "OffredFare" : results.get('Fare',{}).get('OfferedFare'),
                "PublishedFare": results.get('Fare',{}).get('PublishedFare'),
                "discount1": results.get('Fare',{}).get('CommissionEarned'),
                "discount2": results.get('Fare',{}).get('PLBEarned'),
                "AdditionalTxnFeePub": results.get('Fare',{}).get('AdditionalTxnFeePub','0'),
                "OtherCharges": results.get('Fare',{}).get('OtherCharges','0'),
                "ServiceFee": results.get('Fare',{}).get('ServiceFee','0'),
                "AirlineTransFee":results.get('Fare',{}).get('AirlineTransFee','0'),
                "IncentiveEarned": results.get('Fare',{}).get('IncentiveEarned','0'),
            }
            OffredFare = results.get('Fare',{}).get('OfferedFare')
            Currency = results.get('Fare', {}).get('Currency')
            if Currency == "INR":
                Flight_details["MYtax"] = '590'
                Flight_details['mypulishfare']=OffredFare+590
            else:
                Flight_details["MYtax"] = '1150'
                Flight_details['mypulishfare']=OffredFare+1150 

            refund = results.get('IsRefundable')
            if refund:
                Flight_details['Refund'] = 'Refundable'
            else:
                Flight_details['Refund'] = 'Not Refundable'
             
            LCCtype = results.get('IsLCC')
            if LCCtype :
                Flight_details['LCCTYPE'] = 'LCC'
            else:
                Flight_details['LCCTYPE'] = 'NON LCC' 

            passportfulldetails =  results.get('IsPassportFullDetailRequiredAtBook')
            if passportfulldetails :
                Flight_details['passfulldetail'] = 'True'
            else:
                Flight_details['passfulldetail'] = 'False'

            passportticketdetails =  results.get('IsPassportRequiredAtTicket')
            if passportticketdetails :
                Flight_details['passtickketdetail'] = 'True'
            else:
                Flight_details['passtickketdetail'] = 'False'

            passportbookingdetails =  results.get('IsPassportRequiredAtBook')
            if passportbookingdetails :
                Flight_details['passbookingdetail'] = 'True'
            else:
                Flight_details['passbookingdetail'] = 'False'

            date_time_departure = segment_1.get("Origin", {}).get('DepTime')
            departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
            Firstdeparturehoure = str(departure_time.hour).zfill(2)
            Firstdepartureminute = str(departure_time.minute).zfill(2)
            Firstdeparture_H_M = f"{Firstdeparturehoure}:{Firstdepartureminute}"
            Flight_details["departur_H_M"] = Firstdeparture_H_M
            # -----------------------
            datetime_obj = datetime.fromisoformat(date_time_departure)
            formatted_date = datetime_obj.strftime("%a, %d %b")
            Flight_details["departur_date"] = formatted_date

            # #arrival arrtime convert to hour and minute
            date_time_arrival = segment_1.get("Destination", {}).get('ArrTime')
            arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
            Firstarrivalhoure =  str(arrival_time.hour).zfill(2)
            Firstarrivalminute =  str(arrival_time.minute).zfill(2)
            Firstarrival_H_M = f"{Firstarrivalhoure}:{Firstarrivalminute}"
            Flight_details["arrival_H_M"] = Firstarrival_H_M

            datetime_obj = datetime.fromisoformat(date_time_arrival)
            fformatted_date = datetime_obj.strftime("%a, %d %b")
            Flight_details["arrival_date"] = fformatted_date

            # # total hours of traval
            flight_time = arrival_time - departure_time
            total_hour = flight_time.seconds // 3600
            total_minute = (flight_time.seconds % 3600) // 60
            total_H_M = f"{total_hour}h {total_minute}m"
            Flight_details["total_H_M"] = total_H_M
            
            flight_details.append(Flight_details)

            if len(response_data1["Response"]["Results"]["Segments"][0]) > 1:
                segment_2 = response_data1["Response"]["Results"]["Segments"][0][1]
                S_C_name={
                "S_OrgCityName" : segment_2.get("Origin", {}).get('Airport',{}).get('CityName'),
                "S_DesCityName" :  segment_2.get("Destination", {}).get('Airport',{}).get('CityName'),
                "AirlineCode" : segment_2.get('Airline',{}).get('AirlineCode'),
                "AirlineName" : segment_2.get('Airline',{}).get('AirlineName'),
                "AirlineNumber" :segment_2.get("Airline", {}).get("FlightNumber"),
        
                }
                flight_name.append(S_C_name)
                flight_details_two = {
                # SsetsAvailable = segments[1].get('NoOfSeatAvailable')
                "AirlineCode" : segment_2.get('Airline',{}).get('AirlineCode'),
                "AirlineName" : segment_2.get('Airline',{}).get('AirlineName'),
                "AirlineNumber" :segment_2.get("Airline", {}).get("FlightNumber"),
                "OrginAirportCode" : segment_2.get("Origin", {}).get('Airport',{}).get('AirportCode'),
                "OrginAirportName":  segment_2.get("Origin", {}).get('Airport',{}).get('AirportName'),
                "OrginAirportCityName" :  segment_2.get("Origin", {}).get('Airport',{}).get('CityName'),
                "OrginAirportCoutryName" :  segment_2.get("Origin", {}).get('Airport',{}).get('CountryName'),
                "OrginAirportTerminal" :  segment_2.get("Origin", {}).get('Airport',{}).get('Terminal'),
                "OrginAirportDeptime" : segment_2.get("Origin", {}).get('DepTime'),
                "DestinationAirportCode" : segment_2.get("Destination", {}).get('Airport',{}).get('AirportCode'),
                "DestinationAirportName" : segment_2.get("Destination", {}).get('Airport',{}).get('AirportName'),
                "DestinationCityName" : segment_2.get("Destination", {}).get('Airport',{}).get('CityName'),
                "DestinationCountryName" : segment_2.get("Destination", {}).get('Airport',{}).get('CountryName'),
                "DestinationTerminal" : segment_2.get("Destination", {}).get('Airport',{}).get('Terminal'),
                "DestinationDeptime" : segment_2.get("Destination", {}).get('ArrTime'),
                "checkinbag" :segment_2.get('Baggage'),
                "combainbag" : segment_2.get('CabinBaggage'),
                }
                date_time_departure = segment_2.get("Origin", {}).get('DepTime')
                departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
                Firstdeparturehoure = str(departure_time.hour).zfill(2)
                Firstdepartureminute = str(departure_time.minute).zfill(2)
                Firstdeparture_H_M = f"{Firstdeparturehoure}:{Firstdepartureminute}"
                flight_details_two["departur_H_M"] = Firstdeparture_H_M
                # -----------------------
                datetime_obj = datetime.fromisoformat(date_time_departure)
                formatted_date = datetime_obj.strftime("%a, %d %b")
                flight_details_two["departur_date"] = formatted_date

                # #arrival arrtime convert to hour and minute
                date_time_arrival = segment_2.get("Destination", {}).get('ArrTime')
                arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
                Firstarrivalhoure =  str(arrival_time.hour).zfill(2)
                Firstarrivalminute =  str(arrival_time.minute).zfill(2)
                Firstarrival_H_M = f"{Firstarrivalhoure}:{Firstarrivalminute}"
                flight_details_two["arrival_H_M"] = Firstarrival_H_M

                datetime_obj = datetime.fromisoformat(date_time_departure)
                formatted_dates = datetime_obj.strftime("%a, %d %b")
                flight_details_two["arrival_date"] = formatted_dates

                # # total hours of traval
                flight_time = arrival_time - departure_time
                total_hour = flight_time.seconds // 3600
                total_minute = (flight_time.seconds % 3600) // 60
                total_H_M = f"{total_hour}h {total_minute}m"
                flight_details_two["total_H_M"] = total_H_M
                
                
                flight_details.append(flight_details_two)


                
                        
            print(flight_details)
            request.session['saffeflightdetails'] = flight_details
            dumbflighdetails = json.dumps(flight_details)
            print(flight_name)

            api_url_2 = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/SSR'
             
            headers2 = {
            'Content-Type': 'application/json',
            }

            data2 = {
            "EndUserIp":"192.168.11.120",
            "TokenId": f"{token_id}",
            "TraceId": f"{trace_id}",
            "ResultIndex": f"{result_index}"
            }
            
            try:
                response2 = requests.post(api_url_2, json=data2, headers=headers2)
                response2.raise_for_status()
                print("status code:", response2.status_code)

                response_data2 = response2.json()
                print("seats container",response_data2)
               
                flight_food = []
                baggage_details = []
                first_F_price = []
                first_seats_values = []
                second_F_price = []
                second_seats_values = []
                seatnumber = []
               
                if response_data2:
                    if "Response" in response_data2:
                        if "Meal" in response_data2["Response"]:
                            meals = response_data2["Response"]["Meal"]
                            for meal in meals:
                                meal_details = {
                                    "MealPrice": meal.get('Price', 0),
                                    "MealName": meal.get('Description', None),
                                    "Code": meal.get('Code',None)
                                }
                                flight_food.append(meal_details)

                        if "Baggage" in response_data2["Response"]:
                            baggage_list = response_data2["Response"]["Baggage"]
                            for baggage_items in baggage_list:
                                for baggage_item in baggage_items:
                                    baggage_detail = {
                                        "Weight": baggage_item.get("Weight", '0'),
                                        "Code": baggage_item.get("Code",'') ,
                                        "Currency" : baggage_item.get("Currency",''),
                                        "Text" : baggage_item.get("Text",''),
                                        "Price" : baggage_item.get("Price",0)
                                    }
                                    baggage_details.append(baggage_detail)


                        if "MealDynamic" in response_data2["Response"]:
                            meal_dynamic_data = response_data2["Response"]["MealDynamic"]
                            for meal_details_list in meal_dynamic_data:
                                for meal_detail in meal_details_list:
                                    meal_details = {
                                        "MealPrice": meal_detail.get('Price', 0),
                                        "MealName": meal_detail.get('AirlineDescription', ''),
                                        "Code": meal_detail.get("Code",'') ,
                                    }
                                    
                                    flight_food.append(meal_details)
                        
                        if "SeatDynamic" in response_data2["Response"]:
                            first_seat = response_data2['Response']['SeatDynamic'][0]['SegmentSeat'][0]
                            
                            price_in =[]
                            seatno_in = []
                            for i in range(1, len(first_seat['RowSeats'])):
                                row_seats = first_seat['RowSeats'][i]
                                seats_values = []
                                F_flight_price = []
                                F_flight_seatno=[]
                             
                                for seat in row_seats['Seats']:

                                    F_flight_price.append(seat['Price'])
                                    F_flight_seatno.append(seat['SeatNo'])
                                    
                                    se = {"Code": seat.get('Code'),
                                        "Price":seat.get('Price'),
                                        "FlightNumber":seat.get('FlightNumber'),
                                        "AvailablityType":seat.get('AvailablityType'),
                                        "seatRowNo" : seat.get('RowNo'),
                                        "SeatNo" : seat.get('SeatNo'),
                                        "Currency":seat.get('Currency'),
                                        "Text":seat.get('Text'),
                                        "AvailablityType":seat.get('AvailablityType'),
                                        "SeatType" :seat.get('SeatType'),
                                        "SeatTypevalue": "A" if seat.get('SeatType') in [2, 11,10,12,13,14,15,23,31,32,33,46,47] else None

                                    }
                                    seats_values.append(se)
                                   
                                print("price---------------",F_flight_price)
                                print("seat--------num :: ",len(F_flight_seatno))
                                seatno_in.append(F_flight_seatno)
                                price_in.append(F_flight_price)
                                first_seats_values.append(seats_values)
                            

                            # flight price based update
                            unique_values = set()
                            unique_seatnum = set()
                            for seatno in seatno_in:
                                for values in seatno:
                                   unique_seatnum.add(values)
                            sort_seatno = sorted(unique_seatnum)
                            seatnumber.append(sort_seatno)
                            print(sort_seatno) 
                            for sublist in price_in:
                                for value in sublist:
                                    unique_values.add(value)
                            print(unique_values)
                            sorted_values_list = sorted(unique_values)
                            new_values = [{"price": value} for value in sorted_values_list]
                            first_F_price.append(new_values)
                            
                            print("Unique Modified Values:", new_values)
                            

                            
                            print("one--------------------------------",first_seats_values)


                            if len(response_data2['Response']['SeatDynamic'][0]['SegmentSeat']) > 1:
                                second_sea = response_data2['Response']['SeatDynamic'][0]['SegmentSeat'][1]
                                # second_seats_values = []
                                price_in_S =[]
                                seatno_in_S = []
                                for i in range(1, len(second_sea['RowSeats'])):
                                    row_seats_two = second_sea['RowSeats'][i]
                                    seats_values_two = []
                                    S_flight_price = []
                                    S_flight_seatno=[]
                                    for seat_two in row_seats_two['Seats']:
                                        S_flight_price.append(seat_two['Price'])
                                        S_flight_seatno.append(seat_two['SeatNo'])
                                        seeat = {
                                        "Code": seat_two.get('Code'),
                                        "Price":seat_two.get('Price'),
                                        "FlightNumber":seat_two.get('FlightNumber'),
                                        "AvailablityType":seat_two.get('AvailablityType'),
                                        "seatRowNo" : seat_two.get('RowNo'),
                                        "SeatNo" : seat_two.get('SeatNo'),
                                        "Currency":seat_two.get('Currency'),
                                        "Text":seat_two.get('Text'),
                                        "AvailablityType":seat_two.get('AvailablityType'),
                                        "SeatType" :seat_two.get('SeatType'),
                                        "SeatTypevalue": "A" if seat_two.get('SeatType') in [2, 11,10,12,13,14,15,23,31,32,33,46,47] else None
                                        }
                                        seats_values_two.append(seeat)
                                    seatno_in_S.append(S_flight_seatno)
                                    price_in_S.append(S_flight_price)
                                    second_seats_values.append(seats_values_two)
                                    
                                unique_values = set()
                                unique_seatnum_s = set()
                                for seatno in seatno_in_S:
                                    for values in seatno:
                                        unique_seatnum_s.add(values)
                                sort_seat_sec_no = sorted(unique_seatnum_s)
                                seatnumber.append(sort_seat_sec_no)
                                print("second s3at no",sort_seat_sec_no) 
                                for sublist in price_in_S:
                                    for value in sublist:
                                        unique_values.add(value)
                                print("second",unique_values)
                                sorted_values_list = sorted(unique_values)
                                new_values = [{"price": value} for value in sorted_values_list]
                                second_F_price.append(new_values)
                                
                                print("second Unique Modified Values:", new_values)
                                print("second--------------------------------",second_seats_values)
                     
                    # print(fir_flight_seat)
                    # print(len(first_seats_values))
                firflight_seat = json.dumps(first_seats_values)
                fir_flight_price = json.dumps(first_F_price)
                second_flight_seat = json.dumps(second_seats_values)
                second_flight_price = json.dumps(second_F_price)
                seatNumber = json.dumps(seatnumber)
                # print("seat number",seatNumber)   
                # print("new price list :",first_F_price)
                # print("second price list:",second_F_price)    
                baggage_len = len(baggage_details)
                meal_len = len(flight_food)
                
                print("flight_food" ,flight_food)
                # print("baggage_details", baggage_details,baggage_len) 
                        
                return render(request, 'flight/flightreview.html',{'flight_details':flight_details,"dumbflighdetails":dumbflighdetails,'totalflightlist':totalflightlist,'single_flight_del':single_flight_del,'flightname':flight_name,
                    "guest_cout":guest_details,'Airline_code':Airline_code,'baggage_details':baggage_details,'foods':flight_food,'lentght_baggage':baggage_len,'meal_len':meal_len,
                    'fir_flight_seat':firflight_seat,'fir_flight_price':fir_flight_price,'second_flight_seat':second_flight_seat,'second_flight_price':second_flight_price,'seatNumber':seatNumber})

            except requests.exceptions.RequestException as ex:
                return JsonResponse({'error': f"Error: {ex}"})

        except requests.exceptions.RequestException as e:
            # Handle request-related errors
            error_message = f"Error making API request: {e}"
            return render(request, 'flight/error.html', {'error_message': error_message})
    return HttpResponse("Error processing the form.")


from django.shortcuts import redirect
from django.urls import reverse
from .models import Flightclientdetails
@csrf_exempt
def one_trip_reviewpage(request):
    hidden_email = "hari"  # request.session.get('hidden_email','') 
    hidden_phone_number = "9360461524"   # request.session.get('hidden_phone_number','') 
    hidden_username = "gokul"   # request.session.get('hidden_username','')
    published_amount=request.POST.get('publishedprice')
    flight_details=request.POST.get('flightdetails')
    print(type(published_amount),flight_details)
    form = Flightclientdetails(user_name=hidden_username,email=hidden_email,phone_number=hidden_phone_number,contact_details = {"customer_phonenumber":request.POST.get('phoneNumber'),"customer_email":request.POST.get('gmail')} ,user_information={"users_info":request.POST.get('user_information'),"flight_info":request.POST.get('flightdetails')},
            published_amount=request.POST.get('publishedprice'),payment_flag=request.POST.get('payment_flag'),payment_id=request.POST.get('payment_id'),payed_amount=request.POST.get('payed_amount'))
    # print(form)
    
    form.save()
    inserted_row_id = form.id
    request.session['inserted_row_id'] = inserted_row_id


    fulldeatils =request.POST.get('user_information','')
    flightdetails = request.POST.get('flightdetails','')
    fullflightdetails=request.POST.get('fullflightdetails','')
    print("userinformation",fulldeatils)
    datass = json.loads(flightdetails)
    FFList = json.loads(fullflightdetails)
    userinformation = json.loads(fulldeatils)

    request.session['preview_data'] = {
        'user_name': request.POST.get('user_name'),
        'email': request.POST.get('gmail'),
        'phone_number': request.POST.get('phoneNumber'),
        'user_information': request.POST.get('fulldeatils'),
        'flight_information': request.POST.get('flightdetails'),
        'published_amount': request.POST.get('publishedprice'),
        'payment_flag': request.POST.get('payment_flag'),
        'payment_id': request.POST.get('payment_id'),
        'payed_amount': request.POST.get('payed_amount'),
    }

    Phonenum = request.POST.get('phoneNumber')
    Gmail = request.POST.get('gmail')
    user_information= request.POST.get('user_information','')
    flight_details = request.session.get('flight_details')
    # publishedamount = request.session.get('published_amount')
    # print("room info :",flight_details)
    
    # print(user_information)
    
    request.session['flight_details'] = datass
    request.session['fullflight_details'] = FFList
    request.session['userinformation'] = userinformation
    request.session['published_amount'] = published_amount
    request.session['user_information'] = user_information
    request.session['personaldetails'] ={
       'user_information': request.POST.get('user_information')
    }
    # print(form)
    return redirect(reverse('paymentflight'))  

def onetrip_book(request):
    
    razorpay_client = razorpay.Client(auth=("rzp_test_5bpcghNaRd7Qqg", "AyBHtno3opb2r4D1pVgqpPG5"))
    payment_id = request.session.get('payment_id', '')
    print("book",payment_id)
    razor_paydetails = razorpay_client.payment.fetch(payment_id)
    print("book",razor_paydetails)
    inserted_row_id = request.session.get('inserted_row_id', None)
    Flightclientdetails.objects.filter(id=inserted_row_id).update(
    payment_information = razor_paydetails
    )
    amount = razor_paydetails['amount']
    print(amount)
    if amount == amount:
        client_ip = request.session.get('client_ip','')

        # id
        token_id = request.session.get('token_id')
        trace_id = request.session.get('trace_id')
        result_index = request.session.get('result_index')

        value = request.session.get('total_price', None)
        check_value = amount / 100
        print("book",check_value)
        faredetails = request.session.get('fare_details')
        print("faredetails",faredetails)

        LCCfare = {
            'BaseFare': faredetails['BaseFare'],
            'Tax': faredetails['Tax'],
            'YQTax': faredetails['YQTax'],
            'AdditionalTxnFeePub': faredetails['AdditionalTxnFeePub'],
            'AdditionalTxnFeeOfrd' : faredetails['AdditionalTxnFeeOfrd'], 
            "OtherCharges": faredetails['OtherCharges']
        }

        
        # flight class lcc or nonlcc class find function
        saffeflightdetails=request.session.get('saffeflightdetails')
        findlcc = saffeflightdetails[0].get('LCCTYPE')
        print("class of lcc and non lcc",findlcc)

        
        clientdetails =request.session.get('user_information')
        print('userinformation',clientdetails)
        data_dict = json.loads(clientdetails)
        LCCdetails = json.loads(clientdetails)
        # flight gmail , and phone number 
        Finaldata =request.session.get('preview_data')
        Fgmail=Finaldata.get('email')
        FphoneNumber=Finaldata.get('phone_number')

        all_individuals = []
        LCC_all_individuals = []
        # Define a function to map gender values
        def map_gender(gender):
            if gender.lower() == "mr" or gender.lower() == "miss":
                return 1  # Male
            elif gender.lower() == "mrs" or gender.lower() == "mstr":
                return 2  # Female
            else:
                return 0  # Unknown

        # Access the dictionary elements
        # non lcc flight list
        for category, individuals in data_dict.items():
            for person in individuals:
                original_date_str = person["dob"]
                original_date = datetime.strptime(original_date_str, "%Y-%m-%d")
                converted_date_str = original_date.strftime("%Y-%m-%dT00:00:00")
                
                new_person = {
                    "Title": person["gender"],
                    "FirstName": person["firstName"],
                    "LastName": person.get("lastName", ""),
                    "PaxType": 1 if category == "adults" else (2 if category == "children" else 3),
                    "DateOfBirth": converted_date_str,
                    "Gender": map_gender(person["gender"]),
                    "PassportNo": person["passportNumber"],
                    "PassportExpiry":person["exDate"],
                    "AddressLine1": "no1,chennai",  # Add your address line here
                    "AddressLine2": "",
                    "Fare": faredetails,
                    "City": "chennai",
                    "CountryCode": "IN",
                    "CellCountryCode" : "+91",
                    "ContactNo": FphoneNumber,
                    "Nationality": "IN",
                    "Email": Fgmail,
                    "IsLeadPax": True,
                    "FFAirlineCode": None,
                    "FFNumber": "",
                    "GSTCompanyAddress": "",
                    "GSTCompanyContactNumber": "",
                    "GSTCompanyName": "",
                    "GSTNumber": "",
                    "GSTCompanyEmail": ""
                }
                all_individuals.append(new_person)
        print(all_individuals)

        # LCC flight list its stored that values
        for category, individuals in LCCdetails.items():
            for person in individuals:
                original_date_str = person["dob"]
                original_date = datetime.strptime(original_date_str, "%Y-%m-%d")
                converted_date_str = original_date.strftime("%Y-%m-%dT00:00:00")
                
                new_person = {
                    "Title": person["gender"],
                    "FirstName": person["firstName"],
                    "LastName": person.get("lastName", ""),
                    "PaxType": 1 if category == "adults" else (2 if category == "children" else 3),
                    "DateOfBirth": converted_date_str,
                    "Gender": map_gender(person["gender"]),
                    "PassportNo": person["passportNumber"],
                    "PassportExpiry":person["exDate"],
                    "AddressLine1": "no1,chennai",  # Add your address line here
                    "AddressLine2": "",
                    "Fare": faredetails,
                    "City": "chennai",
                    "CountryCode": "IN",
                    "CountryName": "India",
                    "Nationality": "IN",
                    "ContactNo": FphoneNumber,
                    "Email": Fgmail,
                    "IsLeadPax": True,
                    "FFAirlineCode": None,
                    "FFNumber": "",
                    "Baggage":[{
                            "AirlineCode": "6E",
                            "FlightNumber": "23",
                            "WayType": 2,
                            "Code": "No Baggage",
                            "Description": 2,
                            "Weight": 0,
                            "Currency": "INR",
                            "Price": 0,
                            "Origin": "DEL",
                            "Destination": "DXB"
                        }],
                    "MealDynamic": [{
                        "AirlineCode": "6E",
                        "FlightNumber": "23",
                        "WayType": 2,
                        "Code": "No Meal",
                        "Description": 2,
                        "AirlineDescription": "",
                        "Quantity": 0,
                        "Currency": "INR",
                        "Price": 0,
                        "Origin": "DEL",
                        "Destination": "DXB"
                        }],
                    "SeatDynamic": [{
                        "AirlineCode": "6E",
                        "FlightNumber": "2978",
                        "CraftType": "A320-180",
                        "Origin": "DEL",
                        "Destination": "DXB",
                        "AvailablityType": 1,
                        "Description": 2,
                        "Code": "2A",
                        "RowNo": "2",
                        "SeatNo": "A",
                        "SeatType": 1,
                        "SeatWayType": 2,
                        "Compartment": 1,
                        "Deck": 1,
                        "Currency": "INR",
                        "Price": 300                                                                                                                                                                                                      
                            
                        }],
                    "GSTCompanyAddress": "",
                    "GSTCompanyContactNumber": "",
                    "GSTCompanyName": "",
                    "GSTNumber": "",
                    "GSTCompanyEmail": ""
                }
                LCC_all_individuals.append(new_person)
        print(LCC_all_individuals)
        
        if findlcc == 'NON LCC':
            url = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Book'
            
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "ResultIndex": f"{result_index}",
                "Passengers": all_individuals,
                "EndUserIp": "192.168.11.120",
                "TokenId":  f"{token_id}",
                "TraceId": f"{trace_id}"
            }

            try :
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()

                response_data = response.json()
                print(response_data)

                trace_id = response_data['Response']['TraceId']
                pnr = response_data['Response']['Response']['PNR']
                booking_id = response_data['Response']['Response']['BookingId']
                IsTimeChanged = response_data['Response']['Response']['IsTimeChanged']
                IsPriceChanged = response_data['Response']['Response']['IsPriceChanged']
                origin = response_data['Response']['Response']['FlightItinerary']['Origin']
                destination = response_data['Response']['Response']['FlightItinerary']['Destination']

            except requests.exceptions.RequestException as ex:
                print(f"Error: {ex}")

            if IsPriceChanged != True: 
                url2 = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Ticket'

                headers2 = {
                    'Content-Type': 'application/json',
                }
                
                data2={
                    "EndUserIp": "192.168.11.120",
                    "TokenId":f"{token_id}" ,
                    "TraceId": f"{trace_id}",
                    "PNR": f"{pnr}",
                    "BookingId": f'{booking_id}'
                }

            else:
               return render(request,"flight/oneway.html") 
            
        elif findlcc == 'LCC':
            url3 = 'http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Ticket'
            
            headers3 = {
                'Content-Type': 'application/json',
            }

            data3 ={
                    "PreferredCurrency": None,
                    "ResultIndex": f"{result_index}",
                    "AgentReferenceNo": "sonam1234567890",
                    "Passengers": [{
                        "Title": "Mr",
                        "FirstName": "OIRNEGRPN",
                        "LastName": "tbo",
                        "PaxType": 1,
                        "DateOfBirth": "1987-12-06T00:00:00",
                        "Gender": 1,
                        "PassportNo": None,
                        "PassportExpiry": None,
                        "AddressLine1": "123, Test",
                        "AddressLine2": "",
                        "Fare": LCCfare,
                        "City": "Gurgaon",
                        "CountryCode": "IN",
                        "CountryName": "India",      
                        "Nationality": "IN",
                        "ContactNo": FphoneNumber,
                        "Email": "harsh@tbtq.in",
                        "IsLeadPax": True,
                        "FFAirlineCode": "6E",
                        "FFNumber": "123",
                    "Baggage":[{
                            "AirlineCode": "6E",
                            "FlightNumber": "23",
                            "WayType": 2,
                            "Code": "No Baggage",
                            "Description": 2,
                            "Weight": 0,
                            "Currency": "INR",
                            "Price": 0,
                            "Origin": "DEL",
                            "Destination": "DXB"
                        }],
                    "MealDynamic": [{
                        "AirlineCode": "6E",
                        "FlightNumber": "23",
                        "WayType": 2,
                        "Code": "No Meal",
                        "Description": 2,
                        "AirlineDescription": "",
                        "Quantity": 0,
                        "Currency": "INR",
                        "Price": 0,
                        "Origin": "DEL",
                        "Destination": "DXB"
                        }],
                    "SeatDynamic": [{
                        "AirlineCode": "6E",
                        "FlightNumber": "2978",
                        "CraftType": "A320-180",
                        "Origin": "DEL",
                        "Destination": "DXB",
                        "AvailablityType": 1,
                        "Description": 2,
                        "Code": "2A",
                        "RowNo": "2",
                        "SeatNo": "A",
                        "SeatType": 1,
                        "SeatWayType": 2,
                        "Compartment": 1,
                        "Deck": 1,
                        "Currency": "INR",
                        "Price": 300                                                                                                                                                                                                      
                            
                        }],
                    "GSTCompanyAddress": "",
                    "GSTCompanyContactNumber": "",
                    "GSTCompanyName": "",
                    "GSTNumber": "",
                    "GSTCompanyEmail": ""
                } ],
                "EndUserIp": "192.168.11.120",
                "TokenId": f"{token_id}",
                "TraceId": f"{trace_id}"
            }
            try :
                response3 = requests.post(url3, json=data3, headers=headers3)
                response3.raise_for_status()

                response_data3 = response3.json()
                print(response_data3)



                
                return render(request,"flight/error.html")
            except requests.exceptions.RequestException as ex:
                print(f"Error: {ex}")
        



        







        


    





        
       

def round_trip(request):
    if request.method == 'GET':
        From_AirportCode = request.GET.get('from_airport_code', '')
        To_AirportCode = request.GET.get('to_airport_code', '')
        from_roundtrip = request.GET.get('from-round-trip', '')
        to_roundtrip = request.GET.get('to-round-trip', '')  # Corrected variable name
        from_cityname= request.GET.get('cityname-from','')
        to_cityname= request.GET.get('cityname-to','')
        Departure_date_roundtrip = request.GET.get('start-date-roundtrip', '')
        return_data_roundtrip = request.GET.get('return-date-roundtrip','')
        round_class= request.GET.get('classes','')
        noof_adults = request.GET.get('Adults1', '')
        noof_chaild = request.GET.get('Child1', '')
        noof_infant = request.GET.get('Infant1', '')
        # guest_details = f"{no_of_adults} Adults,{no_of_chaild} Childs,{no_of_infant} Infant"

        # departure date method chhange "2024-02-20T00:00:00"
        input_date_departure = datetime.strptime( Departure_date_roundtrip , '%Y-%m-%d')
        Departuredateroundtrip = input_date_departure.strftime('%Y-%m-%dT%H:%M:%S')
        print("output :",Departuredateroundtrip)

        # return date date method chhange "2024-02-20T00:00:00"
        input_date_return = datetime.strptime( return_data_roundtrip , '%Y-%m-%d')
        returndateroundtrip = input_date_return .strftime('%Y-%m-%dT%H:%M:%S')
        print("output :",returndateroundtrip)
        print(noof_adults,noof_chaild,noof_infant,Departuredateroundtrip,returndateroundtrip,From_AirportCode,To_AirportCode)

        request.session['start_place'] =  from_roundtrip  # Corrected variable name
        request.session['end_place'] =to_roundtrip
        # request.session['guest_details'] = guestdetails
        request.session['adults'] = noof_adults
        request.session['childs'] = noof_chaild
        request.session['infant'] = noof_infant

        url = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate'  # Removed extra space

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'ClientId': "ApiIntegrationNew",
            'UserName': "Vacation",
            'Password': "Feast@123456",
            'EndUserIp': "192.168.11.120",
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            response_data = response.json()

            if response_data.get('TokenId', None):  # Corrected key name
                token = response_data['TokenId']
                print("Authentication successful. Token:", token)

                # search for flight
                api_url = 'http://api.tektravels.com'
                api_key = 'Feast@123456'
                EndUserIp = "192.168.11.120"
                
                num_adult = f"{noof_adults}"
                num_chaild = f"{noof_chaild}"
                num_infant = f"{noof_infant}"
                DirectFlight = False
                OneStopFlight = False
                PreferredAirlines = None
                JourneyType = "2"
                sources = None
                
                Segments = [
                    {
                        'Origin': f"{From_AirportCode}",
                        'Destination': f"{To_AirportCode}",
                        'FlightCabinClass': "1",
                        'PreferredDepartureTime':  f"{Departuredateroundtrip}",
                        'PreferredArrivalTime':  f"{Departuredateroundtrip}",
                    },
                    {
                        'Origin': f"{To_AirportCode}",
                        'Destination': f"{From_AirportCode}",
                        'FlightCabinClass': "1",
                        'PreferredDepartureTime':  f"{returndateroundtrip}",
                        'PreferredArrivalTime':  f"{returndateroundtrip}",
                        
                    }
                ]
                
                token_id = f"{token}"
               

                flight_info = roundflight_result (api_key,EndUserIp,token_id,num_adult,num_chaild,num_infant,DirectFlight,OneStopFlight,JourneyType,PreferredAirlines,Segments,sources)

                if flight_info:
                        flight_prices = [flight['OfferedFare'] for flight in flight_info]

                        if not flight_prices or all(price is None for price in flight_prices):
                            min_price = 0
                            max_price = 1
                            error_message = 'No flight available'
                            return render(request, 'flight/roundtrip.html',{'error_message':error_message,'min_price': min_price, 'max_price': max_price})
                        else:
                            valid_prices = [price for price in flight_prices if price is not None]
                            min_price = min(valid_prices)
                            max_price = max(valid_prices)
                            error_message = None
                            return render(request,'flight/roundtrip.html',{'round_flight_info':flight_info ,'fight_class': round_class,'fromAircode':From_AirportCode ,'toAircode':To_AirportCode,
                                                                             'fromcityname':from_cityname,'tocityname':to_cityname,'max_price':max_price,'min_price':min_price })
                else:
                    error_message = "Error occurred during the flight search request"
            else:
                print("Authentication failed:", response_data)
        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
    return HttpResponse("Error processing the form.")

def roundflight_result(api_key,EndUserIp,token_id,num_adult,num_chaild,num_infant,DirectFlight,OneStopFlight,JourneyType,PreferredAirlines,Segments,sources):

    url ='http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Search'
    
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'EndUserIp': EndUserIp,
        'TokenId': token_id,
        'AdultCount': num_adult,
        'ChildCount': num_chaild,
        'InfantCount': num_infant,
        'DirectFlight': DirectFlight,
        'OneStopFlight': OneStopFlight,
        'JourneyType': JourneyType,
        'PreferredAirlines': PreferredAirlines,
        'Segments': Segments,
        'Sources': sources
    }
    # print(data)

    try:
        response = requests.post(url, json=data, headers=headers,params={'apiKey': api_key})
        response.raise_for_status()

        print("status code:", response.status_code)

        response_data = response.json()
        # print(response_data)
        flight_info = []

    # Assuming response_data is the JSON structure you provided
        results = response_data["Response"]["Results"]

        for result in results:
            for segments in result:
                for segment in segments.get("Segments", []):
                    for flight_segment in segment:
                        airline_details = flight_segment.get("Airline", {})

                        airline_info = {
                            "AirlineCode": airline_details.get("AirlineCode"),
                            "AirlineName": airline_details.get("AirlineName"),
                            "FlightNumber": airline_details.get("FlightNumber"),
                            "FareClass":  airline_details.get("FareClass"),
                            "DepartureAirport": flight_segment.get("Origin", {}).get("Airport", {}).get("AirportCode"),
                            "DepartureAirportName": flight_segment.get("Origin", {}).get("Airport", {}).get("AirportName"),
                            "departurecityname":flight_segment.get("Origin", {}).get("Airport", {}).get("CityName"),
                            "departurecontryname":flight_segment.get("Origin", {}).get("Airport", {}).get("CountryName"),
                            "departureTerminal":flight_segment.get("Origin", {}).get("Airport", {}).get("Terminal"),
                            "DepartureTime": flight_segment.get("Origin", {}).get("DepTime"),
                            "ArrivalAirport": flight_segment.get("Destination", {}).get("Airport",{}).get("AirportCode"),
                            "ArrivalAirportName": flight_segment.get("Destination", {}).get("Airport", {}).get("AirportName"),
                            "arrivalcityname":flight_segment.get("Destination", {}).get("Airport", {}).get("CityName"),
                            "arrivalcontryname":flight_segment.get("Destination", {}).get("Airport", {}).get("CountryName"),
                            "arrivalTerminal":flight_segment.get("Destination", {}).get("Airport", {}).get("Terminal"),
                            "ArrivalTime": flight_segment.get("Destination", {}).get("ArrTime"),
                            "OfferedFare": segments.get("Fare", {}).get("OfferedFare"),
                            "checkinbag":flight_segment.get("Baggage"),
                            "combainbag":flight_segment.get("CabinBaggage"),
                            "setsAvailable": flight_segment.get("NoOfSeatAvailable"),
                            "TotalFare": flight_segment.get("Fare", {}).get("OfferedFare"),
                            
                        }

                         #refund or not refund
                        refund_val = segments.get("IsRefundable")
                        if refund_val:
                            airline_info["refund"] = 'Refundable'
                        else:
                            airline_info["refund"] = 'Not Refundable'

                        #departure deptime convert to hour ans minute
                        date_time_departure = airline_info.get("DepartureTime", "")
                        departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
                        airline_info["departurehoure"] = str(departure_time.hour).zfill(2)
                        airline_info["departureminute"] = str(departure_time.minute).zfill(2)

                        #arrival arrtime convert to hour and minute
                        date_time_arrival = airline_info.get("ArrivalTime", "")
                        arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
                        airline_info["arrivalhoure"] =  str(arrival_time.hour).zfill(2)
                        airline_info["arrivalminute"] =  str(arrival_time.minute).zfill(2)

                        # total hours of traval
                        flight_time = arrival_time - departure_time
                        total_hour = flight_time.seconds // 3600
                        total_minute = (flight_time.seconds % 3600) // 60
                        airline_info["totalhour"] = total_hour
                        airline_info["totalminute"] = total_minute
                        
                        flight_info.append(airline_info)

        print(flight_info)
        return flight_info
    except requests.exceptions.RequestException as ex:
        print(f"Error: {ex}")
        return None







from datetime import datetime
import requests
from django.shortcuts import render
from django.http import HttpResponse

def multitrip(request):
    if request.method == 'GET':
        # From_AirportCode = request.GET.get('from_airport_code', '')
        # To_AirportCode = request.GET.get('to_airport_code', '')
        # from_roundtrip = request.GET.get('from-round-trip', '')
        # to_roundtrip = request.GET.get('to-round-trip', '')
        # Departure_date_multitrip = request.GET.get('start-date-roundtrip', '')
        # return_data_multitrip = request.GET.get('return-date-roundtrip', '')
        # no_of_adults = request.GET.get('Adults', '')
        # no_of_chaild = request.GET.get('Child', '')
        # no_of_infant = request.GET.get('Infant', '')
        # guest_details = f"{no_of_adults} Adults,{no_of_chaild} Childs,{no_of_infant} Infant"

        # Uncomment and use date formatting if needed
        # input_date_departure = datetime.strptime(Departure_date_multitrip, '%Y-%m-%d')
        # Departuredatemultitrip = input_date_departure.strftime('%Y-%m-%dT%H:%M:%S')

        # input_date_return = datetime.strptime(return_data_multitrip, '%Y-%m-%d')
        # returndatamultitrip = input_date_return.strftime('%Y-%m-%dT%H:%M:%S')

        # request.session['start_place'] = from_roundtrip
        # request.session['end_place'] = to_roundtrip
        # request.session['guest_details'] = guest_details
        # request.session['adults'] = no_of_adults
        # request.session['childs'] = no_of_chaild
        # request.session['infant'] = no_of_infant

        url = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate'

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'ClientId': "ApiIntegrationNew",
            'UserName': "Vacation",
            'Password': "Feast@123456",
            'EndUserIp': "192.168.11.120",
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            response_data = response.json()

            if response_data.get('TokenId', None):
                token = response_data['TokenId']
                print("Authentication successful. Token:", token)

                # Search for flight
                api_url = 'http://api.tektravels.com'
                api_key = 'Feast@123456'
                EndUserIp = "192.168.11.120"
                
                numadults = 2
                numchailds = 2
                numinfants = 1
                DirectFlight = False
                OneStopFlight = False
                PreferredAirlines = None
                JourneyType = "2"
                sources = None
                
                Segments = [
                    {
                        'Origin': "DEL",
                        'Destination': "BOM",
                        'FlightCabinClass': "1",
                        'PreferredDepartureTime':  "2024-02-20T00:00:00",
                        'PreferredArrivalTime':  "2024-02-20T00:00:00",
                    },
                    {
                        'Origin': "BOM",
                        'Destination': "DEL",
                        'FlightCabinClass': "1",
                        'PreferredDepartureTime':  "2024-02-25T00:00:00",
                        'PreferredArrivalTime':  "2024-02-25T00:00:00",
                        
                    },
                    {
                        'Origin': "DEL",
                        'Destination': "BOM",
                        'FlightCabinClass': "1",
                        'PreferredDepartureTime':  "2024-02-28T00:00:00",
                        'PreferredArrivalTime':  "2024-02-28T00:00:00",
                        
                    }
                ]
                
                token_id = f"{token}"

                flightinfo = multi_flight_result(api_key, EndUserIp, token_id, numadults, numchailds, numinfants, DirectFlight, OneStopFlight, JourneyType, PreferredAirlines, Segments, sources)
                return render(request, 'multidemo.html', {'flightinfo': flightinfo})
            else:
                print("Authentication failed:", response_data)
        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
    return HttpResponse("Error processing the form.")

def multi_flight_result(api_key, EndUserIp, token_id, numadults, numchailds, numinfants, DirectFlight, OneStopFlight, JourneyType, PreferredAirlines, Segments, sources):
    url ='http://api.tektravels.com/BookingEngineService_Air/AirService.svc/rest/Search'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'EndUserIp': EndUserIp,
        'TokenId': token_id,
        'AdultCount': numadults,
        'ChildCount': numchailds,
        'InfantCount': numinfants,
        'DirectFlight': DirectFlight,
        'OneStopFlight': OneStopFlight,
        'JourneyType': JourneyType,
        'PreferredAirlines': PreferredAirlines,
        'Segments': Segments,
        'Sources': sources
    }
    print(data)

    try:
      
        response = requests.post(url, json=data, headers=headers, params={'apiKey': api_key})
        response.raise_for_status()

        print("status code:", response.status_code)

        response_data = response.json()
        print(response_data)
        flightinfo = []

        # Assuming response_data is the JSON structure you provided
        resultss = response_data["Response"]["Results"]
        for result in resultss:
            for segments in result:
                for segment in segments.get("Segments", []):
                    for flight_segment in segment:
                        airlinedetails = flight_segment.get("Airline", {})
                        airlineinfo = {
                            "AirlineCode": airlinedetails.get("AirlineCode"),
                            "AirlineName": airlinedetails.get("AirlineName"),
                            "FlightNumber": airlinedetails.get("FlightNumber"),
                            "FareClass":  airlinedetails.get("FareClass"),
                            "DepartureAirport": flight_segment.get("Origin", {}).get("Airport", {}).get("AirportCode"),
                            "DepartureAirportName": flight_segment.get("Origin", {}).get("Airport", {}).get("AirportName"),
                            "departurecityname": flight_segment.get("Origin", {}).get("Airport", {}).get("CityName"),
                            "departurecontryname": flight_segment.get("Origin", {}).get("Airport", {}).get("CountryName"),
                            "departureTerminal": flight_segment.get("Origin", {}).get("Airport", {}).get("Terminal"),
                            "DepartureTime": flight_segment.get("Origin", {}).get("DepTime"),
                            "ArrivalAirport": flight_segment.get("Destination", {}).get("Airport",{}).get("AirportCode"),
                            "ArrivalAirportName": flight_segment.get("Destination", {}).get("Airport", {}).get("AirportName"),
                            "arrivalcityname": flight_segment.get("Destination", {}).get("Airport", {}).get("CityName"),
                            "arrivalcontryname": flight_segment.get("Destination", {}).get("Airport", {}).get("CountryName"),
                            "arrivalTerminal": flight_segment.get("Destination", {}).get("Airport", {}).get("Terminal"),
                            "ArrivalTime": flight_segment.get("Destination", {}).get("ArrTime"),
                            "OfferedFare": segments.get("Fare", {}).get("OfferedFare"),
                            "checkinbag":flight_segment.get("Baggage"),
                            "combainbag":flight_segment.get("CabinBaggage"),
                        }

                        # Departure deptime convert to hour and minute
                        date_time_departure = airlineinfo.get("DepartureTime", "")
                        departure_time = datetime.strptime(date_time_departure, "%Y-%m-%dT%H:%M:%S")
                        airlineinfo["departurehoure"] = str(departure_time.hour).zfill(2)
                        airlineinfo["departureminute"] = str(departure_time.minute).zfill(2)

                        # Arrival arrtime convert to hour and minute
                        date_time_arrival = airlineinfo.get("ArrivalTime", "")
                        arrival_time = datetime.strptime(date_time_arrival, "%Y-%m-%dT%H:%M:%S")
                        airlineinfo["arrivalhoure"] =  str(arrival_time.hour).zfill(2)
                        airlineinfo["arrivalminute"] =  str(arrival_time.minute).zfill(2)

                        # Total hours of travel
                        flight_time = arrival_time - departure_time
                        total_hour = flight_time.seconds // 3600
                        total_minute = (flight_time.seconds % 3600) // 60
                        airlineinfo["totalhour"] = total_hour
                        airlineinfo["totalminute"] = total_minute

                        flightinfo.append(airlineinfo)

        print(flightinfo)
        return flightinfo
    except requests.exceptions.RequestException as ex:
        print(f"Error: {ex}")
        return None



