from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
import requests
import copy
import datetime
import os
from django.shortcuts import redirect
import json
import math
from django.template import loader, Context
from html import unescape
import ast
from .models import NewCityListHotelCSV
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

def logout_view(request):
    try:
        del request.session['hidden_email']
        del request.session['hidden_phone_number']
        del request.session['hidden_username']
    except KeyError:
        pass  

    logout(request)

    return redirect(reverse('hotel'))


def home(request):
    return render(request, "home/flighthomepage.html")
def hotel(request):
    hidden_email = request.session.get('hidden_email','')
    hidden_phone_number = request.session.get('hidden_phone_number','')
    hidden_username = request.session.get('hidden_username','')
    return render(request, "home/hotelhome.html",{'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username})
def navbar(request):
    return render(request, "home/navbar.html")

def search_destinations(request):
    query = request.GET.get('query', '')
    results = NewCityListHotelCSV.objects.filter(
        Q(DESTINATION__icontains=query) | Q(COUNTRY__icontains=query )
    )[:10]

    data = [
        {
            'label': result.DESTINATION + '( ' + result.COUNTRY + ')',
            'value': result.DESTINATION + '( ' + result.COUNTRY + ')',
            'cityID': result.CITYID,
            'countryCode': result.COUNTRYCODE
        }
        for result in results
    ]

    return JsonResponse({'data': data})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If the request went through a proxy or load balancer,
        # the client's IP address might be in the X-Forwarded-For header
        ip_address = x_forwarded_for.split(',')[0]
    else:
        # Otherwise, get the client's IP address from REMOTE_ADDR
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Store the IP address in a variable
    client_ip_address = ip_address
    return client_ip_address

def login_views(request):
    error = None
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        print(email_or_phone)
        # Check if email_or_phone or password is empty
        if not email_or_phone or not password:
           error_message = 'Email/Phone and Password fields cannot be empty.'

        # Check if the user exists with the given email or phone number
        user = Userdetails.objects.filter(Q(email=email_or_phone) | Q(phone_number=email_or_phone)).first()

        if user:
            # Hash the provided password using MD5 hashing for comparison
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            # Check if the hashed password matches the one stored in the database
            if user.password == hashed_password:
                print(user.email)
                print(user.password)
                print(request.session)
                request.session['hidden_email'] = user.email
                request.session['hidden_phone_number'] = user.phone_number
                request.session['hidden_username'] = user.username
                email = user.email
                phone_number = user.phone_number
                username = user.username
                # template = get_template(template_path)
                # html = template.render(context)
                # print(context)
                return JsonResponse({'success': True, 'email': email,'phone_number':phone_number,'username':username})
                # client_details = Hotelclientdetails.objects.filter(email=user.email)
                # # Serialize the queryset to JSON
                # serialized_data = serialize('json', client_details)
                
                # # Initialize an empty dictionary to store hotel names and booking IDs
                # # Initialize an empty list to store hotel data
                # hotel_data = []

                # # Deserialize the JSON string to a list of dictionaries
                # deserialized_data = json.loads(serialized_data)
                # for entry in deserialized_data:
                #     # Extracting hotel name
                #     fields = entry['fields']
                #     user_info = fields.get('booking_information', {})
                #     datas = json.dumps(user_info)
                #     pdfs = fields.get('pdf_document', '')
                #     print(datas)
                #     hotel_name = user_info.get('hotel_name', {})
                #     booking_id = user_info.get('booking_id', '')

                #     # Store hotel name and booking ID in a dictionary
                #     entry_data = {'hotel_name': hotel_name, 'booking_id': booking_id,'datas':user_info}

                #     # Append entry data to the list
                #     hotel_data.append(entry_data)

                # print(hotel_data)
                # details_dict = json.loads(serialized_data)
                # print(details_dict)
                # template_path = "home/hotelreview.html"
                # # Authenticate user with the provided credentials
                # context = request.session.get('hotel_review')
                # return render(request,'signup/success.html',{"email":user.email,"hotel_data":hotel_data})
            else:
                # Password doesn't match, render login page with error message
                 error_message = 'Invalid email/phone number or password.'

        else:
            # User not found, render login page with error message
           error_message = 'User not found.'

    # If the request method is not POST, render the login page
    return JsonResponse({'success': False, 'error_message': error_message})
# Function to get or refresh token

def get_or_refresh_token(request):
    token_creation_time_str = request.session.get('token_creation_time')
    token_creation_time = datetime.datetime.strptime(token_creation_time_str, "%Y-%m-%d %H:%M:%S") if token_creation_time_str else None
    token = request.session.get('token')
    client_ip = get_client_ip(request)
    request.session['client_ip'] = client_ip

    
    # Define the token expiration time as exactly one day from the creation time
    token_expiration_time = token_creation_time + timedelta(days=1) if token_creation_time else None


    # Check if token exists and is less than 23 hours old
    if token is not None and token_creation_time is not None and datetime.datetime.now() < token_expiration_time:
        return token

    # If token doesn't exist or is older than 23 hours, obtain a new token
    url = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'ClientId': "ApiIntegrationNew",
        'UserName': "Vacation",
        'Password': "Feast@123456",
        'EndUserIp': client_ip,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        if response.status_code == 200:
            token = response_data.get('TokenId')
            if token:
                # Save the token and its creation time in session
                request.session['token'] = token
                request.session['token_creation_time'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                print(request)
                return token

    except requests.exceptions.RequestException as ex:
        print(f"Error: {ex}")

    return None

def process_form(request):

    if request.method == 'GET':
        token = get_or_refresh_token(request)
        print(token)
        if not token:
            return HttpResponse("Error processing the form: Failed to obtain token.")
        city_name = request.GET.get('cityname', '')
        client_ip = request.session.get('client_ip','')
        cityid = request.GET.get('city_id', '')
        countrycode = request.GET.get('country_code', '')
        check_in_str = request.GET.get('check-in', '')
        print(check_in_str)
        check_out = request.GET.get('check-out', '')
        nationality = request.GET.get('nation', '')
        personsdetails = request.GET.get('roomInfoInput','')
        hidden_email = request.session.get('hidden_email','')
        hidden_phone_number = request.session.get('hidden_phone_number','')
        hidden_username = request.session.get('hidden_username','')
        print(hidden_email)
        totalroom = request.GET.get('totalRoomInfoInput','')
        data = json.loads(personsdetails)
        print(personsdetails)
        no_of_adults = data[0]["NoOfAdults"]
        no_of_children = data[0]["NoOfChild"]
        # children_age = data[0]["ChildAge"]
        # print(second_form_url_with_params)
        data_dict = json.loads(totalroom)
        total_rooms = data_dict['TotalRooms']
        total_adults = data_dict['NoOfAdults']
        total_child = data_dict['NoOfChild']
        guest_details = f"{total_adults} Adults,{total_child} Childs,{total_rooms} Rooms"
        print(check_in_str)

        print(total_rooms)
        print(guest_details)
        format_check_in_date = datetime.datetime.strptime(check_in_str, "%d %B %Y").strftime("%d %b %Y")
        check_in_date = datetime.datetime.strptime(check_in_str, '%d %B %Y')
        formatted_check_in_date =  check_in_date.strftime('%d/%m/%Y')
        print(formatted_check_in_date)

        format_check_out_date = datetime.datetime.strptime(check_out, "%d %B %Y").strftime("%d %b %Y")
        check_out_date = datetime.datetime.strptime(check_out, '%d %B %Y')
        formatted_check_out_date = check_out_date.strftime('%d/%m/%Y')
        print(formatted_check_out_date)

        request.session['check_in_date'] = format_check_in_date
        request.session['check_out_date'] = format_check_out_date
        request.session['guestdetails'] = guest_details
        request.session['totalrooms'] = total_rooms
        request.session['adults'] = total_adults
        request.session['childs'] = total_child
        request.session['personsdetails'] = personsdetails
        request.session['nationality'] = nationality
        


    # Calculate the number of nights
        num_nights = (check_out_date - check_in_date).days
        request.session['No_of_Night'] = num_nights



        # url = 'http://api.tektravels.com/SharedServices/SharedData.svc/rest/Authenticate'

        # headers = {
        #     'Content-Type': 'application/json',
        # }

        # data = {
        #     'ClientId': "ApiIntegrationNew",
        #     'UserName': "Vacation",
        #     'Password': "Feast@123456",
        #     'EndUserIp': client_ip,
        # }

        # try:
        #     response = requests.post(url, json=data, headers=headers)
        #     response.raise_for_status()

        #     response_data = response.json()
        #     if response.status_code == 200:
        #         api_data = response.json()

            #     # Construct the file path on the C drive
            #     c_drive_path = "C:\Response"
            #     file_name = "auth.txt"
            #     notepad_file_path = os.path.join(c_drive_path, file_name)

            # # Open the file in write mode ("w") to overwrite existing content
            # with open(notepad_file_path, "w") as notepad_file:
            #     notepad_file.write(str(api_data))

        if token:
            # token = response_data['TokenId']
            print("Authentication successful. Token:", token)

            # Search for hotels
            api_url = 'http://api.tektravels.com'
            api_key = 'Feast@123456'
            check_in_date = f"{formatted_check_in_date}"
            no_of_nights = f"{num_nights}"
            country_code = f"{countrycode}"
            city_id = f"{cityid}"
            result_count = 0
            preferred_currency = "INR"
            guest_nationality = f"{nationality}"
            no_of_rooms = total_rooms
            room_guests = json.loads(personsdetails) 
            print(room_guests)
            max_rating = 5
            min_rating = 3
            review_score = 0
            is_nearby_search_allowed = False
            end_user_ip = client_ip
            token_id = f"{token}"
            print(room_guests)

            hotel_info = get_hotel_results(api_url, api_key, check_in_date, no_of_nights, country_code, city_id,
                                            result_count, preferred_currency, guest_nationality, no_of_rooms, room_guests, max_rating, min_rating,
                                            is_nearby_search_allowed, end_user_ip, token_id)
            print("hii")

            if hotel_info:

                hotel_prices = hotel_info[-3]['HotelPrices']
                # Check if hotel_prices is empty
                if not hotel_prices:
                    # If empty, assign zero as min and max values
                    min_price = 0
                    max_price = 1
                    error_message = 'No Hotels Avaliable'
                    return render(request, 'home/listofhotel.html', {'error_message':error_message,'min_price': min_price, 'max_price': max_price,'formatted_check_in_date':check_in_str ,'formatted_check_out_date':check_out,'countrycode':countrycode, 'nationality': city_name ,'personsdetails':personsdetails, 'min_price': min_price, 'max_price': max_price,'formatted_check_in_date':check_in_str ,'formatted_check_out_date':check_out,'num_nights':num_nights,'cityid':cityid,'totalroom':totalroom,'personsdetails':personsdetails,'totalroom':totalroom,'cityid':cityid,'countrycode':countrycode,'nationality':nationality, 'citytitle':city_name ,'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username,'total_adults':total_adults,'total_rooms':total_rooms})
                else:
                    # If not empty, calculate min and max prices
                    min_price = min(hotel_prices)
                    max_price = max(hotel_prices)
                    return render(request, 'home/listofhotel.html', {'hotel_info': hotel_info , 'token_id': token_id,'countrycode':countrycode,'personsdetails':personsdetails, 'min_price': min_price, 'max_price': max_price,'formatted_check_in_date':check_in_str ,'formatted_check_out_date':check_out,'num_nights':num_nights,'cityid':cityid,'totalroom':totalroom,'no_of_adults':no_of_adults,'no_of_children':no_of_children,'total_adults':total_adults,'total_rooms':total_rooms,'personsdetails':personsdetails,'totalroom':totalroom,'cityid':cityid,'countrycode':countrycode,'nationality':nationality, 'citytitle':city_name ,'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username })

            else:
                error_message = "Error occurred during the hotel search request."
        else:
            print("Authentication failed:", "Token Not Found")
    
        # Handle other exceptions if needed

    # Handle the case when the form is not submitted or authentication fails
    return HttpResponse("Error processing the form.")

def get_hotel_results(api_url, api_key, check_in_date, no_of_nights, country_code, city_id, result_count,
                      preferred_currency, guest_nationality, no_of_rooms, room_guests, max_rating, min_rating, is_nearby_search_allowed, end_user_ip, token_id):
    url = f'{api_url}/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelResult/'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'apiKey': api_key,
        'CheckInDate': check_in_date,
        'NoOfNights': no_of_nights,
        'CountryCode': country_code,
        'CityId': city_id,
        "IsTBOMapped": True,
        'ResultCount': result_count,
        'PreferredCurrency': preferred_currency,
        'GuestNationality': guest_nationality,
        'NoOfRooms': no_of_rooms,
        'RoomGuests': room_guests,
        'MaxRating': max_rating,
        'MinRating': min_rating,
        'ReviewScore': 0,
        'IsNearBySearchAllowed': is_nearby_search_allowed,
        'EndUserIp': end_user_ip,
        'TokenId': token_id,
    }
    print("step1")
    print(data)

    try:
        response = requests.post(url, json=data, headers=headers, params={'apiKey': api_key})
        response.raise_for_status()

        print("Status Code:", response.status_code)
        if response.status_code == 200:
            api_data = response.json()

            # Construct the file path on the C drive
            c_drive_path = "C:\Response"
            file_name = "api_response.txt"
            notepad_file_path = os.path.join(c_drive_path, file_name)

            # Open the file in write mode ("w") to overwrite existing content
           
        response_data = response.json()
        print(response_data)

        trace_id = response_data.get('HotelSearchResult', {}).get('TraceId', '')
        print("TraceId:", trace_id)

        hotel_results = response_data.get('HotelSearchResult', {}).get('HotelResults', [])

        hotel_info = []
        hotel_prices = []
        hotel_star = []
        hotel_property = []

        for hotel in hotel_results:
            hotel_name = hotel.get('HotelName', '')
            rating = hotel.get('StarRating', 0)
            image_url = hotel.get('HotelPicture', '')
            address = hotel.get('HotelAddress', '')
            price = hotel.get('Price', {}).get('OfferedPriceRoundedOff', 0)
            hotel_code = hotel.get('HotelCode', '')
            hotel_category = hotel.get('HotelCategory', '')
            result_index = hotel.get('ResultIndex', None)
            supplier_hotel_codes = hotel.get('SupplierHotelCodes')
            print(supplier_hotel_codes)

            if supplier_hotel_codes is not None:
                second_category_id = supplier_hotel_codes[1]['CategoryId'] if len(supplier_hotel_codes) > 1 else None
            hotel_info.append({
                'HotelName': hotel_name,
                'Rating': rating,
                'ImageURL': image_url,
                'Address': address,
                'Price': price,
                'TraceId': trace_id,
                'HotelCode': hotel_code,
                'HotelCategory': hotel_category,
                'ResultIndex': result_index,
            })

            hotel_prices.append(price)
            hotel_star.append(rating)
            hotel_property.append(hotel_category)
        hotel_info.append({'HotelPrices': hotel_prices})
        hotel_info.append({'HotelStar': hotel_star})
        hotel_info.append({'HotelCategory':hotel_property})

        return hotel_info

    except requests.exceptions.RequestException as ex:
        print(f"Error: {ex}")
        # Handle other exceptions if needed
        return None
def roomdetails(request,hotelCode,traceId,resultIndex,tokenId):
    hotel_code = hotelCode
    trace_id = traceId
    result_index = resultIndex
    token_id = tokenId

    api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelRoom'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': '123.1.1.1',  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }
    print("test2")
    print(data)

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()

        response_data = response.json().get('GetHotelRoomResult', {})

        totalrooms = request.GET.get('totalrooms', None)

        if response_data.get('ResponseStatus') == 1:
            room_details = response_data.get('HotelRoomsDetails', [])

            # Create a list to store formatted room details HTML
            formatted_rooms_html = []

            for room in room_details:
                room_html = f"""
                    <div class="hide-room1">
                        <div class="book-room">
                            <h3 style="width:200px">{room.get('RoomTypeName', '')}</h3>
                            <p>{room.get('Breakfast', '')}</p>
                        </div>
                        <div class="book-room-price">
                            <p class="price">{room.get('Price', {}).get('PublishedPriceRoundedOff', 0)}</p>
                            <p>Per Room/Night</p>
                        </div>
                        <div class="hide-elements" style="display: none;">
                            <p class="tax">{room.get('Price', {}).get('Tax', 0)}</p>
                        </div>
                        <div class="book-room-btn">
                            <button class="btn btn-primary book-btn" onclick="bookRoom()">Book Room</button>
                        </div>
                    </div>
                """

                formatted_rooms_html.append(room_html)

            # Join the formatted HTML for all rooms
            all_rooms_html = ''.join(formatted_rooms_html)

            response_content = {'html': all_rooms_html}
            return JsonResponse(response_content)

        else:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
            return JsonResponse({'error': error_message})
            return JsonResponse(response_content)

    except requests.exceptions.RequestException as ex:
        return JsonResponse({'error': f"Error: {ex}"})
        return JsonResponse(response_content)
def your_view(request):
    hotel_code = request.GET.get('hotel-code', None)
    trace_id = request.GET.get('trace-id', None)
    result_index = request.GET.get('result-index', None)
    token_id = request.GET.get('token-id', None)
    CategoryId_1 = request.GET.get('CategoryId', None)
    totalrooms = request.GET.get('total_rooms', None)
    client_ip = request.session.get('client_ip','')
    hidden_email = request.session.get('hidden_email','')
    hidden_phone_number = request.session.get('hidden_phone_number','')
    hidden_username = request.session.get('hidden_username','')
    print(totalrooms)
    request.session['hotel_code'] = hotel_code
    request.session['trace_id'] = trace_id
    request.session['result_index'] = result_index
    request.session['token_id'] = token_id
    request.session['totalrooms'] = totalrooms
    print(totalrooms)
    print(hotel_code)
    # msg = request.GET.get('par', None)

    check_in_date = request.session.get('check_in_date', '')
    check_out_date = request.session.get('check_out_date', '')
    guest_details = request.session.get('guestdetails', '')
    No_of_nights = request.session.get('No_of_Night','')

    # Second API request
    api_url2 = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelRoom'
    headers2 = {
        'Content-Type': 'application/json',
    }
    data2 = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': client_ip,  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }

    try:
        response = requests.post(api_url2, json=data2, headers=headers2)
        response.raise_for_status()

        response_data = response.json().get('GetHotelRoomResult', {})
        # print("kkk")
        # print(response_data)
        request.session['response_data'] = response_data
        print(totalrooms)
        data_json = json.dumps(data2)
        print(data_json)

        if response_data.get('ResponseStatus') == 1:
            room_details = response_data.get('HotelRoomsDetails', [])
            # print("room_details")
            # print(room_details)
            fixed_combination = None
            category_id = None
            try:
                for room_combination in response_data['RoomCombinationsArray']:
                    if room_combination['InfoSource'] == 'FixedCombination':
                        fixed_combination = room_combination['RoomCombination']
                        category_id = room_combination['CategoryId']
            except Exception as e:
                room_combinations_data = response_data.get('RoomCombinations', {})
                fixed_combination = room_combinations_data.get('RoomCombination', [])

            # print('Fixed Combination:', fixed_combination)
            # print('Category ID:', category_id)
            request.session['category_id'] = category_id
            # Create a dictionary to store room details based on RoomIndex
            room_index_mapping = {room['RoomIndex']: room for room in room_details}

            # Create a list to store formatted room details HTML
            formatted_rooms_html = []

            button_added = False

            for combination in fixed_combination:
                if 'RoomIndex' in combination:
                    combination_indices = combination['RoomIndex']
                    # Check if the combination indices match the totalrooms
                    if len(combination_indices) == int(totalrooms):
                        # Create a list to store HTML for this combination
                        combination_html = []
                        room_json_list = [] 
                        # print("sss")
                        # print(room_json_list)

                        for index in combination_indices:
                            room = room_index_mapping.get(index)
                            print(room)
                            if room:
                                room_json = json.dumps(room)
                                room_json_list.append(room_json) 
                                # print("kkk")
                                # print(room_json)
                                # data_json = json.dumps(data2)
                                room_index = room["RoomIndex"]
                                print(room_index)
                                request.session[f'payload_{index}'] = room_json
                                Hoteltype = {room.get('RoomTypeName', '')}
                                info_string = Hoteltype.pop()
                                values = info_string.split(',')
                                Roomtypename = values[0].strip()
                                Roomtypedetails = ','.join(values[1:]).strip()
                                combination_room_indices = []
                                for index in combination_indices:
                                    room = room_index_mapping.get(index)
                                    if room:
                                        room_index = room["RoomIndex"]
                                        combination_room_indices.append(room_index)
                                # print(combination_room_indices)
                                
                                room_html = f"""
                                   <div class="d-flex col-md-12" style="border-radius:10px;margin:2px;justify-content:space-between;padding:2px 6px;width:100%">
                                    <div class="room-info d-flex justify-content-between" style="width:80%">
                                        <div class="more_room_div">
                                            <p class="room-info-name">{Roomtypename}</p>
                                            <p class="room-type-name">{Roomtypedetails}</p>
                                        </div>
                                        <div class="price-info mt-3">
                                            <div class="rub-price">
                                                <p style="color: #004EAE;">INR</p>
                                                <p class="price" style="color: #004EAE;">{room.get('Price', {}).get('PublishedPriceRoundedOff', 0)}</p>
                                            </div>
                                            <div style="margin-top:-20px; margin-bottom:10px;">
                                                <p class="pn" >Per Room/Night</p>
                                            </div>
                                        </div>
                                    </div>    
                                    <div class="hide-elements" style="display: none;">
                                        <p class="tax">{room.get('Price', {}).get('Tax', 0)}</p>
                                        <input type="hidden" class="room-index" value="{{ hotel.HotelName }}">
                                        <input type="hidden" class="room-index" value="{room_json}">
                                        <input type="hidden" class="room-index" id="data-123" value='{data_json}'>
                                    </div>
                                    <div class="empty-placeholder" style="{'' if not button_added else 'height: 30px; width: 23%;'}"></div>
                                    <div class="book-room-btn mt-4" style="{'' if not button_added else 'display: none;'}">
                                            <button class="book-btn"
                                                    onclick="bookRoom()">
                                                Book Room
                                            </button>
                                        </div>
                                   </div>
                                     
                                   
                                """
                                combination_html.append(room_html)

                                # Set the flag to True after adding the button for the first time
                                button_added = True
                            else:
                                button_added = False  # Reset the flag if no room is found

                        # Join the HTML for this combination
                        combination_html_joined = ''.join(combination_html)

                        room_json_array_string = json.dumps(room_json_list)

                        # Wrap the generated HTML within hide-room1 container
                        formatted_rooms_html.append(f'''
                            <div class="hide-room1">{combination_html_joined}<div class="hide-123">
                                <input type="hidden" class="room-index" id="hide-123" value='{room_json_array_string}'>
                                <input type="hidden" class="room-index" id="data-123" value='{data_json}'>
                                <input type="hidden" class="room-index" id="categoryid" value='{category_id}'>
                            </div>
                        </div>
                        ''')
                        # print("jhjd")
                        # print(room_json_array_string)
                        
                        button_added = False

                        # formatted_rooms_html.append(.format(room_indices=json.dumps(combination_room_indices), hotel_code=hotel_code))

            # Join the formatted HTML for all combinations
            all_rooms_html = ''.join(formatted_rooms_html)
            # print(all_rooms_html)

        else:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
            return JsonResponse({'error': error_message})
    except requests.exceptions.RequestException as ex:
        return JsonResponse({'error': f"Error: {ex}"})
    
    # First API request
    api_url1 = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelInfo'
    headers1 = {
        'Content-Type': 'application/json',
    }
    data1 = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': client_ip,  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }
    if category_id is not None:
           data1['CategoryId'] = category_id

    try:
        response1 = requests.post(api_url1, json=data1, headers=headers1)
        response1.raise_for_status()

        response_data1 = response1.json().get('HotelInfoResult', {}).get('HotelDetails', {})
        # print("check")
        # print(response_data1)
        # Extract information from the first API response
        hotel_name = response_data1.get('HotelName', '')
        star_rating = response_data1.get('StarRating', '')
        description = response_data1.get('Description', '')
        attractions = response_data1.get('Attractions', [])
        hotel_facilities = response_data1.get('HotelFacilities', [])
        images = response_data1.get('Images', [])
        address = response_data1.get('Address','')
        latitude = response_data1.get('Latitude', '')
        longitude = response_data1.get('Longitude', '')

        extracted_info = {
            'check_in_date':check_in_date,
            'check_out_date':check_out_date,
            'guest_details':guest_details,
            'No_of_Night':No_of_nights,
            'hotel_name': hotel_name,
            'star_rating': star_rating,
            'description': description,
            'attractions': attractions,
            'hotel_facilities': hotel_facilities,
            'images': images,
            'address':address,
            'latitude': latitude,
            'longitude': longitude,
            # Add other information as needed...
        }
        # Combine information from both API responses
        combined_info = {
            'hotel_info': extracted_info,
            'room_details_html': all_rooms_html,
        }
        # print(combined_info)

        return render(request, 'home/viewhotels.html', {'combined_info': combined_info,'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username})


    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    

def get_room_details(request):
    hotel_code = request.POST.get('hotelCode', None)
    trace_id = request.POST.get('traceId', None)
    result_index = request.POST.get('resultIndex', None)
    token_id = request.POST.get('tokenId', None)
    client_ip = request.session.get('client_ip','')

    request.session['trace_id'] = trace_id
    request.session['token_id'] = token_id
    request.session['result_index'] = result_index
    request.session['hotel_code'] = hotel_code

    api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelRoom'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': client_ip,  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }
    print("test2")
    print(data)
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            api_data = response.json()

            # Construct the file path on the C drive
            c_drive_path = "C:\Response"
            file_name = "Room response.txt"
            notepad_file_path = os.path.join(c_drive_path, file_name)

            # Open the file in write mode ("w") to overwrite existing content
            with open(notepad_file_path, "w") as notepad_file:
                notepad_file.write(str(api_data))
        response_data = response.json().get('GetHotelRoomResult', {})
        print("categroyid")
        print(response_data)
        print("categroyid")
        request.session['response_data'] = response_data
        totalrooms = request.session.get('totalrooms', '')

        if response_data.get('ResponseStatus') == 1:
            room_details = response_data.get('HotelRoomsDetails', [])
            print("room_details")
            print(room_details)
            fixed_combination = None
            category_id = None
            try:
                for room_combination in response_data['RoomCombinationsArray']:
                    if room_combination['InfoSource'] == 'FixedCombination':
                        fixed_combination = room_combination['RoomCombination']
                        category_id = room_combination['CategoryId']
            except Exception as e:
                room_combinations_data = response_data.get('RoomCombinations', {})
                fixed_combination = room_combinations_data.get('RoomCombination', [])

            print('Fixed Combination:', fixed_combination)
            print('Category ID:', category_id)
            request.session['category_id'] = category_id

            # Create a dictionary to store room details based on RoomIndex
            room_index_mapping = {room['RoomIndex']: room for room in room_details}
            print(room_index_mapping)

            # Create a list to store formatted room details HTML
            formatted_rooms_html = []

            button_added = False


            for combination in fixed_combination:
                if 'RoomIndex' in combination:
                    combination_indices = combination['RoomIndex']
                    print(combination_indices)
                    # Check if the combination indices match the totalrooms
                    if len(combination_indices) == int(totalrooms):
                        
                        # Create a list to store HTML for this combination
                        combination_html = []
                        room_json_list = [] 
                        print("sss")
                        print(room_json_list)

                        for index in combination_indices:
                            room = room_index_mapping.get(index)
                            print(room)
                            if room:
                                room_json = json.dumps(room)
                                room_json_list.append(room_json)  
                                print("kkk")
                                print(room_json)
                                room_index = room["RoomIndex"]
                                print(room_index)
                                data_json = json.dumps(data)
                                print("gff")
                                print(data_json)
                                request.session[f'payload_{index}'] = room_json
                                Hoteltype = {room.get('RoomTypeName', '')}
                                info_string = Hoteltype.pop()
                                values = info_string.split(',')
                                Roomtypename = values[0].strip()
                                Roomtypedetails = ','.join(values[1:]).strip()
                                combination_room_indices = []
                                for index in combination_indices:
                                    room = room_index_mapping.get(index)
                                    if room:
                                        room_index = room["RoomIndex"]
                                        combination_room_indices.append(room_index)
                                print(combination_room_indices)
                                
                                room_html = f"""
                                    <div class="hide-room2">
                                        <div class="book-room">
                                            <p class="room-info-name">{Roomtypename}</p>
                                            <p class="room-info-sname">{Roomtypedetails}</p>
                                        </div>
                                        <div class="price_div d-flex justify-content-between">
                                            <div class="book-room-price">
                                                <p class="price">INR {room.get('Price', {}).get('OfferedPriceRoundedOff', 0)}</p>
                                                <p class="mb-0">Per Room/Night</p>
                                            </div>
                                            <input type="hidden" id="CancellationPolicies" value="{room.get('CancellationPolicies', [])}">
                                            <tbody id="cancellationPoliciesTableBody">
                                            <div class="hide-elements" style="display: none;">
                                                <p class="tax">{room.get('Price', {}).get('Tax', 0)}</p>
                                                <input type="hidden" class="room-index" value="{{ hotel.HotelName }}">
                                                <input type="hidden" class="room-index" value="{json.dumps(room_json_list)}">
                                            </div>
                                            <div class="book-room-btn" style="{'' if not button_added else 'display: none;'}">
                                                <button class="btn btn-primary book-btn"
                                                        onclick="bookRoom()">
                                                    Book Room
                                                </button>
                                            </div>
                                        </div>
                                        <div class="empty-placeholder" style="{'' if not button_added else 'height: 30px;'}"></div>
                                    </div>
                                """
                                combination_html.append(room_html)

                                # Set the flag to True after adding the button for the first time
                                button_added = True
                            else:
                                button_added = False  # Reset the flag if no room is found

                        # Join the HTML for this combination
                        combination_html_joined = ''.join(combination_html)

                        room_json_array_string = json.dumps(room_json_list)

                        # Wrap the generated HTML within hide-room1 container
                        formatted_rooms_html.append(f'''
                            <div class="hide-room1">{combination_html_joined}<div class="hide-123">
                                <input type="hidden" class="room-index" id="hide-123" value='{room_json_array_string}'>
                                <input type="hidden" class="room-index" id="data-123" value='{data_json}'>
                                <input type="hidden" class="room-index" id="categoryid" value='{category_id}'>
                            </div>
                        </div>
                        ''')
                        print("jhjd")
                        print(room_json_array_string)
                        
                        button_added = False

                        # formatted_rooms_html.append(.format(room_indices=json.dumps(combination_room_indices), hotel_code=hotel_code))

            # Join the formatted HTML for all combinations
            all_rooms_html = ''.join(formatted_rooms_html)

            # Store the combined HTML in the session or wherever you need
            # request.session['all_rooms_html'] = all_rooms_html
            return JsonResponse({'room_details_html': all_rooms_html})

    except requests.exceptions.RequestException as ex:
        print(f"Error: {ex}")

from django.utils import timezone

def hotelreview(request):
    if request.method == 'POST':
        room_json_list = request.POST.get('roomJsonElement')  # Retrieve roomJsonElement value
        hotel_name = request.POST.get('hotelName')  # Retrieve hotelName value
        hide_123_value = request.POST.get('hide123Value')
        category_id_1 = request.POST.get('categoryid1')  # Retrieve hide123Value value
        client_ip = request.session.get('client_ip','')
        hidden_email = request.session.get('hidden_email','')
        hidden_phone_number = request.session.get('hidden_phone_number','')
        hidden_username = request.session.get('hidden_username','')
        request.session['category_id_1'] = category_id_1
        Hoteldetails_1 = json.loads(room_json_list)
        request.session['hotel_name'] = hotel_name
        # Handle the values as needed
        # print("Room JSON List:", Hoteldetails_1)
        # print("Hotel Name:", hotel_name)
        # print("Hide 123 Value:", hide_123_value)
        # Get the current time
        current_time_1 = datetime.datetime.now()

        # Add 10 minutes to the current time
        future_time_1 = current_time_1 + timedelta(minutes=10)
        current_time = current_time_1.strftime('%Y-%m-%d %H:%M:%S')
        future_time = future_time_1.strftime('%Y-%m-%d %H:%M:%S')
        request.session['current_time'] = current_time
        request.session['future_time'] = future_time

        formatted_hotel_room_details = []

        # Iterate over each data entry
        for entry in Hoteldetails_1:
            room_details = json.loads(entry)
            
            # Check if AvailabilityType is "Confirm"
            if room_details.get("AvailabilityType") == "Confirm":
                # Format room details as desired
                smoking_preference_mapping = {
                    "NoPreference": 0,
                    "Smoking": 1,
                    "NonSmoking": 2,
                    "Either": 3
                }
                smoking_preference = room_details.get("SmokingPreference", None)
                smoking_preference_numeric = smoking_preference_mapping.get(smoking_preference, None)
                
                formatted_room = {
                    "RoomIndex": room_details.get("RoomIndex", None),
                    "RoomTypeCode": room_details.get("RoomTypeCode", None),
                    "RoomTypeName": room_details.get("RoomTypeName", None),
                    "RatePlanCode": room_details.get("RatePlanCode", None),
                    "BedTypeCode": room_details.get("BedTypeCode", None),
                    "SmokingPreference": smoking_preference_numeric,
                    "Supplements": room_details.get("Supplements", None),
                    "Price": {
                        "CurrencyCode": room_details.get("Price", {}).get("CurrencyCode", None),
                        "RoomPrice": room_details.get("Price", {}).get("RoomPrice", None),
                        "Tax": room_details.get("Price", {}).get("Tax", None),
                        "ExtraGuestCharge": room_details.get("Price", {}).get("ExtraGuestCharge", None),
                        "ChildCharge": room_details.get("Price", {}).get("ChildCharge", None),
                        "OtherCharges": room_details.get("Price", {}).get("OtherCharges", None),
                        "Discount": room_details.get("Price", {}).get("Discount", None),
                        "PublishedPrice": room_details.get("Price", {}).get("PublishedPrice", None),
                        "PublishedPriceRoundedOff": room_details.get("Price", {}).get("PublishedPriceRoundedOff", None),
                        "OfferedPrice": room_details.get("Price", {}).get("OfferedPrice", None),
                        "OfferedPriceRoundedOff": room_details.get("Price", {}).get("OfferedPriceRoundedOff", None),
                        "AgentCommission": room_details.get("Price", {}).get("AgentCommission", None),
                        "AgentMarkUp": room_details.get("Price", {}).get("AgentMarkUp", None),
                        "ServiceTax": room_details.get("Price", {}).get("ServiceTax", None),
                        "TDS": room_details.get("Price", {}).get("TDS", None)
                    }
                }
                
                formatted_hotel_room_details.append(formatted_room)

        # Display the resulting formatted hotel room details
        # print(formatted_hotel_room_details)

        request.session['formatted_hotel_room_details'] = formatted_hotel_room_details

        data = json.loads(hide_123_value)
        request.session['data_1'] = data
        # Access values separately
        result_index = data["ResultIndex"]
        hotel_code = data["HotelCode"]
        end_user_ip = data["EndUserIp"]
        token_id = data["TokenId"]
        trace_id = data["TraceId"]
        nationality = request.session.get('nationality', None)
        totalrooms = request.session.get('totalrooms', '')

        payload = {
            'ResultIndex': result_index,
            'HotelCode': hotel_code,
            'HotelName': hotel_name,
            'GuestNationality': nationality,
            'NoOfRooms': totalrooms,
            'ClientReferenceNo': 0,
            'IsVoucherBooking': 'true',
            'EndUserIp': client_ip,
            'TokenId': token_id,
            'TraceId': trace_id,
            'HotelRoomsDetails': formatted_hotel_room_details
        }

        if category_id_1 is not None:
           payload['CategoryId'] = category_id_1

        print("test3")
        print(payload)
        request.session['payload_str'] = payload

        api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/BlockRoom'
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            # Handle the API response as needed
            api_response = response.json()
            print("hii")
            print(api_response)
            print("hii")
            block_book = api_response
            request.session['block_book'] = block_book
            block_book_string = json.dumps(block_book)
            hide_123_value_str = json.dumps(hide_123_value)


            # Print or use the total_offered_price as needed 
            block_room_result = api_response.get('BlockRoomResult', {})
            # Print 'CancellationPolicies'
            
            availability_type = block_room_result.get('AvailabilityType', '')
            Is_cancellation_policy_changed = block_room_result.get('IsCancellationPolicyChanged','')
            Is_Price_Changed = block_room_result.get('IsPriceChanged','')
            print(Is_cancellation_policy_changed)
            print(Is_Price_Changed)
            print(Is_cancellation_policy_changed)
            print(Is_Price_Changed)
            if Is_cancellation_policy_changed or Is_Price_Changed:
                return redirect('hotel')
            # Continue with the rest of your code if the conditions are not met
            hotel_rooms_details = block_room_result.get('HotelRoomsDetails', [])
            LastCancellationDate = hotel_rooms_details[0]['LastCancellationDate']
            cancellation_policies_str = hotel_rooms_details[0]['CancellationPolicies']
            cancellation_policies = json.dumps(cancellation_policies_str)
            print(cancellation_policies)
            print(LastCancellationDate)
            hotel_rooms_details = block_room_result.get('HotelRoomsDetails', [])
            LastCancellationDate = hotel_rooms_details[0]['LastCancellationDate']
            cancellation_policies_str = hotel_rooms_details[0]['CancellationPolicies']
            cancellation_policies = json.dumps(cancellation_policies_str)
            print(cancellation_policies)
            print(LastCancellationDate)
            # Initialize a variable to store the total OfferedPriceRoundedOff
            total_offered_price = 0

            # Loop through each hotel room and add the OfferedPriceRoundedOff to the total
            for room_details in hotel_rooms_details:
                total_offered_price += room_details['Price']['OfferedPriceRoundedOff']
            print("Total Offered Price for all hotels:", total_offered_price)
            print("end")
            total_offered_price_main =  "{:.2f}".format(total_offered_price)

            # Print the entire 'Price' dictionary to inspect its structure
            discount_amount = 0.05 * total_offered_price

            # Calculate GST on the discounted price
            gst_amount = 0.18 * discount_amount

            # Calculate the final price after applying GST
            formatted_final_tax = math.ceil(gst_amount + discount_amount)
            final_tax = "{:.2f}".format(formatted_final_tax)

            # total price of the room
            total_price_not = formatted_final_tax + total_offered_price
            total_price = "{:.2f}".format(total_price_not)
            request.session['total_price'] = total_price_not

            check_in_date = request.session.get('check_in_date', '')
            check_out_date = request.session.get('check_out_date', '')
            adults = request.session.get('adults', '')
            childs = request.session.get('childs', '')
            No_of_nights = request.session.get('No_of_Night','')
            personsdetails =  request.session.get('personsdetails','')

            if availability_type == 'Confirm':
                # Extract required details into a dictionary
                details_dict = {
                    'hotel_name': block_room_result.get('HotelName', ''),
                    'rating': block_room_result.get('StarRating', 0),
                    'address': f"{block_room_result.get('AddressLine1', '')}, {block_room_result.get('AddressLine2', '')}",
                    'cancellation_policy': block_room_result.get('HotelPolicyDetail', ''),
                    'CancellationPolicies': cancellation_policies,
                    'check_in_date':check_in_date,
                    'check_out_date':check_out_date,
                    'adults':adults,
                    'childs':childs,
                    'totalrooms':totalrooms,
                    'No_of_Night':No_of_nights,
                    'published_price':total_offered_price_main,
                    'final_tax':final_tax,
                    'total_price':total_price
                }
                request.session['details_dict'] = details_dict
                print(details_dict)

                # Pass the details dictionary to another HTML page

                return render(request, 'home/hotelreview.html', {'details': details_dict, 'personsdetails': personsdetails , 'block_book_string':block_book_string ,'hide_123_value_str':hide_123_value_str , 'category_id':category_id_1,'current_time':current_time,'future_time':future_time,'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username})

                # hotel_review = {'details': details_dict, 'personsdetails': personsdetails , 'block_book_string':block_book_string ,'hide_123_value_str':hide_123_value_str , 'category_id':category_id_1,'current_time':current_time,'future_time':future_time}
                # request.session['hotel_review'] = hotel_review
            # # Pass the details dictionary to another HTML page
            #     template = loader.get_template('home/hotelreview.html')

            #     # Render the template with the data
            #     rendered_template = template.render({'my_data': hotel_review}, request)

                # template_path = 'home/hotelreview.html'
                # # Create a Django response object, and specify content_type as pdf
                # template = get_template(template_path)
                # html = template.render(hotel_review)
                

                # Return the rendered content as an HttpResponse
                # return HttpResponse(html)
        
        except Exception as e:
            error_message = f"Unexpected error: {e}"
            return render(request, 'home/error.html', {'error_message': error_message})

        except requests.exceptions.RequestException as e:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()

                # Handle the API response as needed
                api_response = response.json()
                # Handle request-related errors
                error_message = f"Error making API request: {e}"
                api_response = response.json()
                error_message = api_response['BlockRoomResult']['Error']['ErrorMessage']
                
                return render(request, 'home/error.html', {'error_message': error_message})

        except ValueError as e:
            # Handle JSON decoding errors
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            # Handle the API response as needed
            api_response = response.json()
            error_message = f"Error decoding API response: {e}"
            error_message = api_response['BlockRoomResult']['Error']['ErrorMessage']
            return render(request, 'home/error.html', {'error_message': error_message})

        except Exception as e:
            # Handle other unexpected errors
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            # Handle the API response as needed
            api_response = response.json()
            error_message = f"Unexpected error: {e}"
            error_message = api_response['BlockRoomResult']['Error']['ErrorMessage']
        return render(request, 'home/error.html', {'error_message': error_message})
    
    # room_json_element_str = request.GET.get('roomJsonElement', [])
    # hotel_name = request.GET.get('hotelName', None)
    # # hide123Value = request.GET.get('hide123Value', [])
    # # print("hii")
    # # print(hide123Value)
    # Hoteldetails_1 = request.session.get('response_data', {})
    # trace_id = request.session.get('trace_id', None)
    # token_id = request.session.get('token_id', None)
    # result_index = request.session.get('result_index', None)
    # check_in_date = request.session.get('check_in_date', '')
    # hotel_code = request.session.get('hotel_code', None)
    # totalrooms = request.session.get('totalrooms', None)
    # nationality = request.session.get('nationality', None)
    # print(room_json_element_str)

    # # Get the current time with seconds
    # current_time = timezone.now()

    # # Calculate 10 minutes plus from the current time
    # plus_10_minutes = current_time + timezone.timedelta(minutes=10)
    # print(plus_10_minutes)

    # print(f"totalrooms: {totalrooms}")
    # print("str1")
    # print(type(room_json_element_str))
    # # Decoding the URL encoded string and parsing it into a Python list
    # room_json_element = json.loads(room_json_element_str)
    # print(room_json_element)
    # print(type(room_json_element))
    # print('lele')
    # for element in room_json_element:
    #     print(element)
    # # if not print(room_json_element_str[0]):
    # #     room_json_element = room_json_element_str
    # #     print(room_json_element[1])
    # # else:
    # #     try:
    # #         room_json_element = room_json_element_str
    # #     except NameError:  # Handle the case when room_json_element_str is not defined
    # #         room_json_element = None  # Or any other action you want to take
    # # print(room_json_element)
    # # Assuming your data is stored in the variable hotel_rooms_details
    # Hoteldetails = Hoteldetails_1.get('HotelRoomsDetails', [])

    # matching_rooms = []

    # for room_index in room_json_element:
    #     for detail in Hoteldetails:
    #         print("Room Index:", room_index, "Detail Room Index:", detail["RoomIndex"])
    #         if room_index == detail["RoomIndex"]:
    #             print("Success: RoomIndex Match")
    #             matching_rooms.append(detail)
    #             print("start")
    #             print("success")
    #             break 

    # # Print the matching room details
    # print("123")
    # print(matching_rooms)
    # print("123")



    # print("str2")
    # check_in_date = request.session.get('check_in_date', '')
    # check_out_date = request.session.get('check_out_date', '')
    # adults = request.session.get('adults', '')
    # childs = request.session.get('childs', '')
    # totalrooms = request.session.get('totalrooms', '')
    # No_of_nights = request.session.get('No_of_Night','')
    # personsdetails =  request.session.get('personsdetails','')

    # # Create a new list to store hotel room details in the specified format
    # # 

    # # processed_indices = set()

    # # # Iterate over the room indices in room_json_element
    # # for room_index in range(len(Hoteldetails)):
    # #     try:

    # #         # Find the corresponding room details in Hoteldetails
    # #         if room_index in processed_indices:
    # #             print(f"Room with index {room_index} already processed. Skipping.")
    # #             continue

    # #         # Find the corresponding room details in Hoteldetails
    # #         matching_room_details = [room for room in Hoteldetails if all(room.get(key) == value for key, value in zip(('RoomIndex',), room_json_element))]
    # #         if matching_room_details:
    # #             # If room_details is found, format it according to the specified structure
    # #             for room_details in matching_room_details:
    # #                 if room_details:
    # #                     if any(room['RoomIndex'] == room_details['RoomIndex'] for room in formatted_hotel_room_details):
    # #                         print(f"Room with RoomIndex {room_details['RoomIndex']} already in the formatted list. Skipping.")
    #                         # continue
    # formatted_hotel_room_details = []

    # matched_indices = set()
                        
    # for room_index in room_json_element:
    #     room_index_matched = False
    #     for room_details in Hoteldetails:
    #         if room_details["RoomIndex"] in matched_indices:
    #             continue  # Skip this room details if it has already been matched
    #         print("Room Index:", room_index, "Detail Room Index:", room_details["RoomIndex"])
    #         if room_index == room_details["RoomIndex"]:
    #             smoking_preference_mapping = {
    #                 "NoPreference": 0,
    #                 "Smoking": 1,
    #                 "NonSmoking": 2,
    #                 "Either": 3
    #             }

    #             # Get the smoking preference from room_details
    #             smoking_preference = room_details.get("SmokingPreference", None)

    #             # Map the smoking preference to its numerical value
    #             smoking_preference_numeric = smoking_preference_mapping.get(smoking_preference, None)
    #             formatted_room = {
    #                 "RoomIndex": room_details.get("RoomIndex", None),
    #                 "RoomTypeCode": room_details.get("RoomTypeCode", None),
    #                 "RoomTypeName": room_details.get("RoomTypeName", None),
    #                 "RatePlanCode": room_details.get("RatePlanCode", None),
    #                 "BedTypeCode": room_details.get("BedTypeCode", None),
    #                 "SmokingPreference": smoking_preference_numeric,
    #                 "Supplements": room_details.get("Supplements", None),
    #                 "Price": {
    #                     "CurrencyCode": room_details.get("Price", {}).get("CurrencyCode", None),
    #                     "RoomPrice": room_details.get("Price", {}).get("RoomPrice", None),
    #                     "Tax": room_details.get("Price", {}).get("Tax", None),
    #                     "ExtraGuestCharge": room_details.get("Price", {}).get("ExtraGuestCharge", None),
    #                     "ChildCharge": room_details.get("Price", {}).get("ChildCharge", None),
    #                     "OtherCharges": room_details.get("Price", {}).get("OtherCharges", None),
    #                     "Discount": room_details.get("Price", {}).get("Discount", None),
    #                     "PublishedPrice": room_details.get("Price", {}).get("PublishedPrice", None),
    #                     "PublishedPriceRoundedOff": room_details.get("Price", {}).get("PublishedPriceRoundedOff", None),
    #                     "OfferedPrice": room_details.get("Price", {}).get("OfferedPrice", None),
    #                     "OfferedPriceRoundedOff": room_details.get("Price", {}).get("OfferedPriceRoundedOff", None),
    #                     "AgentCommission": room_details.get("Price", {}).get("AgentCommission", None),
    #                     "AgentMarkUp": room_details.get("Price", {}).get("AgentMarkUp", None),
    #                     "ServiceTax":  room_details.get("Price", {}).get("ServiceTax", None),
    #                     "TDS": room_details.get("Price", {}).get("TDS", None)
    #                 }
    #             }

    #             # Add the formatted room to the new list
    #             formatted_hotel_room_details.append(formatted_room)
    #             matched_indices.add(room_details["RoomIndex"])   

    #             room_index_matched = True
    #             break  # Stop searching for this room index
        
    # # Check if the room index was not matched
    # if not room_index_matched:
    #     print("Room Index:", room_index, "Detail Room Index: Not found")


    # # Display the resulting formatted hotel room details
    # print(formatted_hotel_room_details)

    # payload = {
    #     'ResultIndex': result_index,
    #     'HotelCode': hotel_code,
    #     'HotelName': hotel_name,
    #     'GuestNationality': nationality,
    #     'NoOfRooms': totalrooms,
    #     'ClientReferenceNo': 0,
    #     'IsVoucherBooking': 'true',
    #     'EndUserIp': '123.1.1.1',
    #     'TokenId': token_id,
    #     'TraceId': trace_id,
    #     'HotelRoomsDetails': formatted_hotel_room_details
    # }
    # category_id = request.session.get('category_id', None)
    # if category_id is not None:
    #     payload['CategoryId'] = category_id
    # print("start")
    # print(payload)
    # request.session['payload'] = payload
    # print("end")

    # # Now, you can use this payload in your API request
        
    # api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/BlockRoom'
    # headers = {'Content-Type': 'application/json'}
    # try:
    #     response = requests.post(api_url, json=payload, headers=headers)
    #     response.raise_for_status()

    #     # Handle the API response as needed
    #     api_response = response.json()
    #     print("hii")
    #     print(api_response)


    #     # Print or use the total_offered_price as needed 
    #     block_room_result = api_response.get('BlockRoomResult', {})
    #     availability_type = block_room_result.get('AvailabilityType', '')
    #     hotel_rooms_details = block_room_result.get('HotelRoomsDetails', [])
    #     # Initialize a variable to store the total OfferedPriceRoundedOff
    #     total_offered_price = 0

    #     # Loop through each hotel room and add the OfferedPriceRoundedOff to the total
    #     for room_details in hotel_rooms_details:
    #         total_offered_price += room_details['Price']['OfferedPriceRoundedOff']
    #     print("Total Offered Price for all hotels:", total_offered_price)
    #     print("end")
    #     total_offered_price_main =  "{:.2f}".format(total_offered_price)

    #     # Print the entire 'Price' dictionary to inspect its structure
    #     discount_amount = 0.05 * total_offered_price

    #     # Calculate GST on the discounted price
    #     gst_amount = 0.18 * discount_amount

    #     # Calculate the final price after applying GST
    #     formatted_final_tax = math.ceil(gst_amount + discount_amount)
    #     final_tax = "{:.2f}".format(formatted_final_tax)

    #     # total price of the room
    #     total_price_not = formatted_final_tax + total_offered_price
    #     total_price = "{:.2f}".format(total_price_not)
    #     request.session['total_price'] = total_price_not

    #     if availability_type == 'Confirm':
    #         # Extract required details into a dictionary
    #         details_dict = {
    #             'hotel_name': block_room_result.get('HotelName', ''),
    #             'rating': block_room_result.get('StarRating', 0),
    #             'address': f"{block_room_result.get('AddressLine1', '')}, {block_room_result.get('AddressLine2', '')}",
    #             'cancellation_policy': block_room_result.get('HotelPolicyDetail', ''),
    #             'check_in_date':check_in_date,
    #             'check_out_date':check_out_date,
    #             'adults':adults,
    #             'childs':childs,
    #             'totalrooms':totalrooms,
    #             'No_of_Night':No_of_nights,
    #             'published_price':total_offered_price_main,
    #             'final_tax':final_tax,
    #             'total_price':total_price
    #         }
    #         request.session['details_dict'] = details_dict
    #         print(details_dict)

    #     # Pass the details dictionary to another HTML page

    #     return render(request, 'home/hotelreview.html', {'details': details_dict, 'personsdetails': personsdetails})
    
    # except requests.exceptions.RequestException as e:
    #         # Handle request-related errors
    #         error_message = f"Error making API request: {e}"
    #         return render(request, 'home/error.html', {'error_message': error_message})

    # except ValueError as e:
    #     # Handle JSON decoding errors
    #     error_message = f"Error decoding API response: {e}"
    #     return render(request, 'home/error.html', {'error_message': error_message})

    # except Exception as e:
    #     # Handle other unexpected errors
    #     error_message = f"Unexpected error: {e}"
    # return render(request, 'home/error.html', {'error_message': error_message})
    

from django.shortcuts import render, redirect
# from .forms import HotelClientDetailsForm
from .models import Hotelclientdetails
@csrf_exempt
def previewpage(request):
        
        hidden_email = request.session.get('hidden_email','')
        hidden_phone_number = request.session.get('hidden_phone_number','')
        hidden_username = request.session.get('hidden_username','')
        
        form = Hotelclientdetails(user_name=hidden_username,email=hidden_email,phone_number=hidden_phone_number,contact_details = {"customer_name":request.POST.get('user_name'),"customer_phonenumber":request.POST.get('phone_number'),"customer_email":request.POST.get('email')} ,user_information={"room_info":request.POST.get('user_information'),"price_info":request.POST.get('room_information')},
                                 published_amount=request.POST.get('published_amount'),payment_flag=request.POST.get('payment_flag'),payment_id=request.POST.get('payment_id'),payed_amount=request.POST.get('payed_amount'))
        print(form)
        current_time_extra =request.POST.get('curTime')
        print(current_time_extra)
        request.session['current_time_extra'] = current_time_extra
        persons=request.POST.get('user_information')
        print("thiru")
        print(persons)
        request.session['persons'] = persons
        persons_data = json.loads(persons)
        # Separate title, adult, and child details
        combined_details = []
        client_ip = request.session.get('client_ip','')

        for room_data in persons_data:
            room_key = list(room_data.keys())[0]
            room_details = room_data[room_key]

            for adult in room_details['adults']:
                combined_details.append({
                    'title': adult['gender'],
                    'firstName': adult['firstName'],
                    'lastName': adult['lastName']
                })

            for child in room_details['children']:
                combined_details.append({
                    'title': child['gender'],
                    'firstName': child['firstName'],
                    'lastName': child['lastName'],
                    'age': child['age']
                })

        print('Combined Details:', combined_details)
        # if form.is_valid():
        form.save()
        inserted_row_id = form.id
        print(inserted_row_id)
        request.session['inserted_row_id'] = inserted_row_id
        request.session['preview_data'] = {
            'user_name': request.POST.get('user_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'user_information': request.POST.get('user_information'),
            'published_amount': request.POST.get('published_amount'),
            'payment_flag': request.POST.get('payment_flag'),
            'payment_id': request.POST.get('payment_id'),
            'payed_amount': request.POST.get('payed_amount'),
        }
        request.session['personaldetails'] = {
            'user_information': request.POST.get('user_information'),
        }
        print(form)
        
        # request.session['custom_data'] = form
        return redirect(reverse('home'))
        # print(context)
        return render(request, 'home/hotelhome.html')  

def hotelbooked(request):
    razorpay_client = razorpay.Client(auth=("rzp_test_5bpcghNaRd7Qqg", "AyBHtno3opb2r4D1pVgqpPG5"))
    payment_id = request.session.get('payment_id', '')
    razor_paydetails = razorpay_client.payment.fetch(payment_id)
    inserted_row_id = request.session.get('inserted_row_id', None)
    Hotelclientdetails.objects.filter(id=inserted_row_id).update(
    payment_information = razor_paydetails
    )
    amount = razor_paydetails['amount']
    client_ip = request.session.get('client_ip','')

    value = request.session.get('total_price', None)
    check_value = amount / 100
    if value == check_value:
        block_book = request.session.get('block_book')
        data = request.session.get('data_1')
        hide_123_val = request.POST.get('hide_123_val')
        category_id = request.POST.get('category_id')
        current_time_extra = request.POST.get('current_time')
        print(current_time_extra)

        category_id_1 = request.session.get('category_id_1')
        print(category_id_1)
        hotel_rooms_details = block_book["BlockRoomResult"]["HotelRoomsDetails"]
        print(hotel_rooms_details)

        formatted_hotel_room_details_1 = []

        # Iterate over each data entry
        for entry in hotel_rooms_details:
            room_details = entry
            
            # Check if AvailabilityType is "Confirm"
            if room_details.get("AvailabilityType") == "Confirm":
                # Format room details as desired
                smoking_preference_mapping = {
                    "NoPreference": 0,
                    "Smoking": 1,
                    "NonSmoking": 2,
                    "Either": 3
                }
                smoking_preference = room_details.get("SmokingPreference", None)
                smoking_preference_numeric = smoking_preference_mapping.get(smoking_preference, None)
                
                formatted_room = {
                    "RoomIndex": room_details.get("RoomIndex", None),
                    "RoomTypeCode": room_details.get("RoomTypeCode", None),
                    "RoomTypeName": room_details.get("RoomTypeName", None),
                    "RatePlanCode": room_details.get("RatePlanCode", None),
                    "BedTypeCode": room_details.get("BedTypeCode", None),
                    "SmokingPreference": smoking_preference_numeric,
                    "Supplements": room_details.get("Supplements", None),
                    "Price": {
                        "CurrencyCode": room_details.get("Price", {}).get("CurrencyCode", None),
                        "RoomPrice": room_details.get("Price", {}).get("RoomPrice", None),
                        "Tax": room_details.get("Price", {}).get("Tax", None),
                        "ExtraGuestCharge": room_details.get("Price", {}).get("ExtraGuestCharge", None),
                        "ChildCharge": room_details.get("Price", {}).get("ChildCharge", None),
                        "OtherCharges": room_details.get("Price", {}).get("OtherCharges", None),
                        "Discount": room_details.get("Price", {}).get("Discount", None),
                        "PublishedPrice": room_details.get("Price", {}).get("PublishedPrice", None),
                        "PublishedPriceRoundedOff": room_details.get("Price", {}).get("PublishedPriceRoundedOff", None),
                        "OfferedPrice": room_details.get("Price", {}).get("OfferedPrice", None),
                        "OfferedPriceRoundedOff": room_details.get("Price", {}).get("OfferedPriceRoundedOff", None),
                        "AgentCommission": room_details.get("Price", {}).get("AgentCommission", None),
                        "AgentMarkUp": room_details.get("Price", {}).get("AgentMarkUp", None),
                        "ServiceTax": room_details.get("Price", {}).get("ServiceTax", None),
                        "TDS": room_details.get("Price", {}).get("TDS", None)
                    }
                }
                
                formatted_hotel_room_details_1.append(formatted_room)

        # Display the resulting formatted hotel room details
        print("HHH")
        print(formatted_hotel_room_details_1)
        # Access values separately
        client_ip = request.session.get('client_ip','')
        result_index = data["ResultIndex"]
        hotel_code = data["HotelCode"]
        end_user_ip = data["EndUserIp"]
        token_id = data["TokenId"]
        trace_id = data["TraceId"]
        nationality = request.session.get('nationality', None)
        totalrooms = request.session.get('totalrooms', '')
        hotel_name = request.session.get('hotel_name')
        payload_data = {
                'ResultIndex': result_index,
                'HotelCode': hotel_code,
                'HotelName': hotel_name,
                'GuestNationality': nationality,
                'NoOfRooms': totalrooms,
                'ClientReferenceNo': 0,
                'IsVoucherBooking': 'true',
                'EndUserIp': client_ip,
                'TokenId': token_id,
                'TraceId': trace_id,
                'HotelRoomsDetails': formatted_hotel_room_details_1
            }
        if category_id_1 is not None:
            payload_data['CategoryId'] = category_id_1
        # trace_id = request.session.get('trace_id', '')
        # print(trace_id)
        # token_id = request.session.get('token_id', '')
        personaldetails_list = request.session.get('personaldetails', '')
        print(personaldetails_list)
        # payload_data = request.session.get('payload_str', '')
        # print(payload_data)
        payment_id = request.session.get('payment_id', '')
        inserted_row_id = request.session.get('inserted_row_id', None)
        Hotelclientdetails.objects.filter(id=inserted_row_id).update(
        payment_flag='paid',
        payment_id= payment_id,
        payed_amount = check_value,
        datetime = datetime.datetime.now()
        )

        # Parsing the JSON string
        user_information_list = json.loads(personaldetails_list['user_information'])

        # Initialize the HotelPassenger array
        result_dict = {}

        # Iterate through room information
        for room_data in user_information_list:
            for room_key, room_value in room_data.items():
                # Initialize the HotelPassenger array for each room
                hotel_passenger_list = []

                # Iterate through adults and children in the room
                for passenger in room_value['adults'] + room_value['children']:
                    # Convert age to integer, handling the case where age is a string
                    age = int(passenger["age"]) if passenger["age"].isdigit() else 0

                    pax_type = 1 if age == 0 else 2


                    hotel_passenger = {
                        "Title": passenger["gender"],
                        "FirstName": passenger["firstName"],
                        "MiddleName": None,
                        "LastName": passenger["lastName"],
                        "Phoneno": None,
                        "Email": None,
                        "PaxType": pax_type,  # Assuming a default value for PaxType
                        "LeadPassenger": True,  # Assuming LeadPassenger is always false for non-lead passengers
                        "Age": age,
                        "PassportNo": None,
                        "PassportIssueDate": None,
                        "PassportExpDate": None,
                        "PAN":'ABCTY1234D'
                    }
                    hotel_passenger_list.append(hotel_passenger)

                # Add the HotelPassenger array to the result dictionary
                result_dict[f"HotelPassenger_{room_key}"] = {"HotelPassenger": hotel_passenger_list}


        # Now result_dict contains separate HotelPassenger arrays for each room
        print(json.dumps(result_dict, indent=2))
        result_dicts = json.dumps(result_dict)
        print(payload_data)
        print(result_dicts)

        result_dicts = json.loads(result_dicts)

        modified_payload_data = copy.deepcopy(payload_data)

        # Now you can proceed with the loop as shown in the previous code snippet
        for index, room_details in enumerate(modified_payload_data['HotelRoomsDetails'], start=1):
            room_key = f"HotelPassenger_room{index}"
            room_passenger = result_dicts.get(room_key, {}).get('HotelPassenger', [])
            room_details['HotelPassenger'] = room_passenger

        # Printing the modified payload_data
        print("123")
        print(modified_payload_data)

        # Printing the modified payload_data
        print("copy")
        print(modified_payload_data)


            # Adding HotelPassenger data to payload_data
        # Adding HotelPassenger data to payload_data
        modified_payload_data['AgencyId'] = 57456 
        #  <---PACKAGEFARE--->
        # modified_payload_data['IsPackageFare'] = True 
        # modified_payload_data['IsPackageDetailsMandatory'] = True
        # modified_payload_data["ArrivalTransport"] = {
        #     "ArrivalTransportType": 0,
        #     "TransportInfoId": "Ab 777",
        #     "Time": "2019-05-21T18:18:00"
        # }
        # category_id_1 = request.session.get('category_id_1')
        # if category_id_1 is not None:
        #     payload_data['CategoryId'] = category_id_1

        # modified_payload_data["DepartureTransport"] = {
        #     "DepartureTransportType": 0,
        #     "TransportInfoId": "Ab 777",
        #     "Time": "2023-10-21T12:43:45"
        # }



        api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/Book'

        headers = {
            'Content-Type': 'application/json',
        }

        # Updating the data dictionary with values from the payload
        data = modified_payload_data
        print("test4")
        print(data)
        try:
            response = requests.post(api_url, json=data, headers=headers, params={'apiKey': 'Feast@123456'})
            response.raise_for_status()

            print("Status Code:", response.status_code)

            response_data = response.json()
            print(response_data)
            block_room_result =  response_data['BookResult']
            Is_cancellation_policy_changed = block_room_result.get('IsCancellationPolicyChanged','')
            Is_Price_Changed = block_room_result.get('IsPriceChanged','')
            if Is_cancellation_policy_changed or Is_Price_Changed:
                error_message = "There are some technical issue the amount will be refunded"
                return render(request, 'home/error.html', {'error_message': error_message})
            if response_data['BookResult']['HotelBookingStatus'] == 'Confirmed':
                booking_details = {
                    'InvoiceNumber': response_data['BookResult']['InvoiceNumber'],
                    'ConfirmationNo': response_data['BookResult']['ConfirmationNo'],
                    'BookingRefNo': response_data['BookResult']['BookingRefNo'],
                    'BookingId': response_data['BookResult']['BookingId'],
                    'IsPriceChanged': response_data['BookResult']['IsPriceChanged'],
                    'IsCancellationPolicyChanged': response_data['BookResult']['IsCancellationPolicyChanged']
                }
                Hotelclientdetails.objects.filter(id=inserted_row_id).update(
                invoice_number = booking_details['InvoiceNumber'],
                confirmation_no = booking_details['ConfirmationNo'],
                booking_ref_no = booking_details['BookingRefNo'],
                booking_id = booking_details['BookingId'],
                is_price_changed = booking_details['IsPriceChanged'],
                is_cancellation_policy_changed = booking_details['IsCancellationPolicyChanged']
                )
                hotel_client_details = Hotelclientdetails.objects.get(id=inserted_row_id)
                customer_phonenumber = user_information["customer_phonenumber"]
                customer_name = user_information["customer_name"]
                customer_email = user_information["customer_email"]
                record_data = {
                    "user_name": customer_name,
                    "email": customer_email,
                    "phone_number": customer_phonenumber,
                    "user_information": hotel_client_details.user_information,
                    "datetime": hotel_client_details.datetime,
                    "published_amount": hotel_client_details.published_amount,
                    "payment_flag": hotel_client_details.payment_flag,
                    "payment_id": hotel_client_details.payment_id,
                    "payed_amount": hotel_client_details.payed_amount,
                    "booking_id": hotel_client_details.booking_id,
                    "booking_ref_no": hotel_client_details.booking_ref_no,
                    "invoice_number": hotel_client_details.invoice_number,
                    "confirmation_no": hotel_client_details.confirmation_no,
                    "is_price_changed": hotel_client_details.is_price_changed,
                    "is_cancellation_policy_changed": hotel_client_details.is_cancellation_policy_changed,
                    "is_price_changed_true": hotel_client_details.is_price_changed_true,
                    "is_cancellation_policy_changed_true": hotel_client_details.is_cancellation_policy_changed_true,
                }

                api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/HotelService.svc/rest/GetBookingDetail'

                headers = {
                    'Content-Type': 'application/json',
                }
                data = {
                    "BookingId": record_data['booking_id'],
                    "EndUserIp": end_user_ip,
                    "TokenId": token_id
                }
                
                response = requests.post(api_url, json=data, headers=headers, params={'apiKey': 'Feast@123456'})
                response.raise_for_status()

                print("Status Code:", response.status_code)

                response_data_1 = response.json() 
                response_data = response_data_1.get('GetBookingDetailResult', {})
                print(response_data)
                def format_datetime(datetime_str):
                    # Parse the datetime string
                    parsed_datetime = datetime.datetime.fromisoformat(datetime_str)

                    # Format the datetime as required
                    formatted_datetime = parsed_datetime.strftime("%b %d %Y %H:%M:%S")

                    return formatted_datetime

                # Format datetime strings in response_data
                response_data["InitialCheckinDate"] = format_datetime(response_data["InitialCheckInDate"])
                response_data["InitialCheckoutDate"] = format_datetime(response_data["InitialCheckOutDate"])
                response_data["BookingDate"] = format_datetime(response_data["BookingDate"])
                cancellation_policy = response_data["HotelPolicyDetail"]
                stripped_content = unescape(cancellation_policy)
                index_of_checkin = stripped_content.find("CheckIn")
                # Remove all content before the "CheckIn"
                stripped_content = stripped_content[index_of_checkin:]

                room_details = []
                for room in response_data["HotelRoomsDetails"]:
                    room_id = room["RoomId"]
                    room_type_name = room["RoomTypeName"]
                    cancellation_policy = room["CancellationPolicy"]
                    adult_count = room["AdultCount"]
                    child_count = room["ChildCount"]
                    
                    # Include hotel passenger details for each room
                    hotel_passengers = []
                    for passenger in room.get("HotelPassenger", []):
                        title = passenger.get("Title")
                        first_name = passenger.get("FirstName")
                        last_name = passenger.get("LastName")
                        
                        hotel_passengers.append({
                            "Title": title,
                            "FirstName": first_name,
                            "LastName": last_name,
                        })

                    room_details.append({
                        "RoomId": room_id,
                        "RoomTypeName": room_type_name,
                        "CancellationPolicy": cancellation_policy,
                        "AdultCount": adult_count,
                        "ChildCount": child_count,
                        "HotelPassengers": hotel_passengers  # Include hotel passenger details
                    })
                booking_details_1 = {
                    "hotel_policy_details":stripped_content,
                    "invoice_number": response_data["InvoiceNo"],
                    "invoice_amount": response_data["InvoiceAmount"],
                    "booking_id": response_data["BookingId"],
                    "hotel_confirmation_number": response_data["HotelConfirmationNo"],
                    "hotel_name": response_data["HotelName"],
                    "star_rating": response_data["StarRating"],
                    "address_line_1": response_data["AddressLine1"],
                    "hotel_booking_status": response_data["HotelBookingStatus"],
                    "address_line_2": response_data["AddressLine2"],
                    "confirmation_no": response_data["ConfirmationNo"],
                    "longitude": response_data["Longitude"],
                    "latitude": response_data["Latitude"],
                    "booking_ref_number": response_data["BookingRefNo"],
                    "city": response_data["City"],
                    "initial_checkin_date": response_data["InitialCheckinDate"],
                    "initial_checkout_date": response_data["InitialCheckoutDate"],
                    "number_of_rooms": response_data["NoOfRooms"],
                    "Hotel_Passengers_Details": room_details,
                    "Booking_Date": response_data["BookingDate"],
                    "Special_Request": response_data["SpecialRequest"]
                } 
                print(booking_details_1)
                Hotelclientdetails.objects.filter(id=inserted_row_id).update(
                booking_information = booking_details_1
                )
                pk = hotel_client_details.booking_id 
                pk = hotel_client_details.booking_id  
                send_pdf_link(customer_phonenumber,customer_name,pk)
                print("Booking Details:", booking_details)
                return render(request, 'home/success.html',{'booking_details': booking_details,'booking_details_1':booking_details_1,'record_data':record_data})
            elif response_data['BookResult']['HotelBookingStatus'] == 'VerifyPrice':
                booking_details = {
                    'InvoiceNumber': response_data['BookResult']['InvoiceNumber'],
                    'ConfirmationNo': response_data['BookResult']['ConfirmationNo'],
                    'BookingRefNo': response_data['BookResult']['BookingRefNo'],
                    'BookingId': response_data['BookResult']['BookingId'],
                    'IsPriceChanged': response_data['BookResult']['IsPriceChanged'],
                    'IsCancellationPolicyChanged': response_data['BookResult']['IsCancellationPolicyChanged'],
                    'ispricechangedtrue':response_data['BookResult']['HotelRoomsDetails'][0]['Price']['OfferedPriceRoundedOff'],
                    'is_cancellation_policy_changed_true':response_data['BookResult']['HotelRoomsDetails'][0]['CancellationPolicy']
                }
                Hotelclientdetails.objects.filter(id=inserted_row_id).update(
                invoice_number = booking_details['InvoiceNumber'],
                confirmation_no = booking_details['ConfirmationNo'],
                booking_ref_no = booking_details['BookingRefNo'],
                booking_id = booking_details['BookingId'],
                is_price_changed = booking_details['IsPriceChanged'],
                is_cancellation_policy_changed = booking_details['IsCancellationPolicyChanged'],
                is_price_changed_true = booking_details['ispricechangedtrue'],
                is_cancellation_policy_changed_true = booking_details['is_cancellation_policy_changed_true']
                )
                hotel_client_details = Hotelclientdetails.objects.get(id=inserted_row_id)
                user_information = hotel_client_details.contact_details
                print(user_information)
                # context = {
                #     'booking_details_1':hotel_client_details.booking_information,
                #     'User_Name':hotel_client_details.user_name,
                #     'phone_number':hotel_client_details.phone_number
                # }
                # print(context)
                customer_phonenumber = user_information["customer_phonenumber"]
                customer_name = user_information["customer_name"]
                customer_email = user_information["customer_email"]
                record_data = {
                    "user_name": customer_name,
                    "email": customer_email,
                    "phone_number": customer_phonenumber,
                    "user_information": hotel_client_details.user_information,
                    "datetime": hotel_client_details.datetime,
                    "published_amount": hotel_client_details.published_amount,
                    "payment_flag": hotel_client_details.payment_flag,
                    "payment_id": hotel_client_details.payment_id,
                    "payed_amount": hotel_client_details.payed_amount,
                    "booking_id": hotel_client_details.booking_id,
                    "booking_ref_no": hotel_client_details.booking_ref_no,
                    "invoice_number": hotel_client_details.invoice_number,
                    "confirmation_no": hotel_client_details.confirmation_no,
                    "is_price_changed": hotel_client_details.is_price_changed,
                    "is_cancellation_policy_changed": hotel_client_details.is_cancellation_policy_changed,
                    "is_price_changed_true": hotel_client_details.is_price_changed_true,
                    "is_cancellation_policy_changed_true": hotel_client_details.is_cancellation_policy_changed_true,
                }
                pk = hotel_client_details.booking_id  
                send_pdf_link(customer_phonenumber,customer_name,pk)# Assuming inserted_row_id is defined earlier in the function
                # current = storePDf(request, pk)
                print("Booking Details:", booking_details)
                error_message = 'There is error in the process if the amount is debitted it will be refunded'
                return render(request, 'home/error.html',{'error_message': error_message})
            else:
                error_message =  response_data['BookResult']['Error']['ErrorMessage']
                return render(request, 'home/error.html', {'error_message': error_message})

        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
            # Handle other exceptions if needed
            return None
    else:
        error_message = "The amount you paid is wrong"
        return render(request, 'home/error.html', {'error_message': error_message})
# config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from io import BytesIO
def generatePDf(request, pk):
    template_path = 'home/pdf.html'
    print(pk)
    hotel_client_details = Hotelclientdetails.objects.get(booking_id=pk)
    context = {
        'booking_details_1':hotel_client_details.booking_information,
        'User_Name':hotel_client_details.user_name,
        'phone_number':hotel_client_details.phone_number
    }
    print(context)
    # Create a Django response object, and specify content_type as pdf
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF

    # # Return a response indicating success
    # return HttpResponse('PDF successfully generated and saved to the database.')
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'filename="{hotel_client_details.booking_id}_payslip.pdf"'
    # find the template and render it.
    

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
        # hotel_client_details.pdf_document.save(f'{hotel_client_details.booking_id}_payslip.pdf', response)
    return response
    return render(request, 'staff/staff_payslip.html', context)
def storePDf(request, pk):
    template_path = 'home/pdf.html'
    print(pk)
    hotel_client_details = Hotelclientdetails.objects.get(booking_id=pk)
    context = {
        'booking_details_1':hotel_client_details.booking_information
    }
    print(context)
    # Create a Django response object, and specify content_type as pdf
    template = get_template(template_path)
    html = template.render(context)
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf)
    # Save the generated PDF to the database
    hotel_client_details.pdf_document.save(f'{hotel_client_details.booking_id}_payslip.pdf', pdf)
def testpdf(request):
    pk = 1879505
    hotel_client_details = Hotelclientdetails.objects.get(booking_id=pk)
    user_information = hotel_client_details.contact_details
    print(user_information)
    # context = {
    #     'booking_details_1':hotel_client_details.booking_information,
    #     'User_Name':hotel_client_details.user_name,
    #     'phone_number':hotel_client_details.phone_number
    # }
    # print(context)
    customer_phonenumber = user_information["customer_phonenumber"]
    customer_name = user_information["customer_name"]
    send_pdf_link(customer_phonenumber,customer_name,pk)
    return render(request, 'home/pdftest.html',{'booking_details_1':hotel_client_details.booking_information,
        'User_Name':hotel_client_details.user_name,
        'phone_number':hotel_client_details.phone_number,
        'payment_id':hotel_client_details.payment_id})
def pdf(request):
    template_path = 'home/pdfs.html'
    pk = 1873454
    hotel_client_details = Hotelclientdetails.objects.get(booking_id=pk)
    context = {
        'booking_details_1':hotel_client_details.booking_information,
        'User_Name':hotel_client_details.user_name,
        'phone_number':hotel_client_details.phone_number,
        'payment_id':hotel_client_details.payment_id
    }
    print(context)
    # Create a Django response object, and specify content_type as pdf
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF

    # # Return a response indicating success
    # return HttpResponse('PDF successfully generated and saved to the database.')
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'filename="{hotel_client_details.booking_id}_payslip.pdf"'
    # find the template and render it.
    

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
        # hotel_client_details.pdf_document.save(f'{hotel_client_details.booking_id}_payslip.pdf', response)
    return response
    return render(request, 'staff/staff_payslip.html', context)



def mail(request):
     return render(request, 'home/mail.html')

def sendemail(request):
    if request.method == 'POST':
        # messages = "your otp is 0004"
  
        # host=settings.EMAIL_HOST, 
        # port=settings.EMAIL_PORT,  
        # username=settings.EMAIL_HOST_USER, 
        # password=settings.EMAIL_HOST_PASSWORD, 
        # use_tls=settings.EMAIL_USE_TLS  
            
        # email_from = settings.EMAIL_HOST_USER  
        recipient_list = [request.POST.get("email"), ]  
        # message = messages  
          

        s = smtplib.SMTP('smtppro.zoho.com','587')
            # start TLS for security
        s.starttls()
            # Authentication
        s.login("tharun@vacationfeast.com", "nBvizb5wji94")
            # message to be sent
        messages = "Subject: vacation Feast \n\n Your OTP 1234"
            # sending the mail
        s.sendmail("bookings@vacationfeast.com", recipient_list, messages) 
        return HttpResponse('Email sent successfully!')
    return render(request, 'home/hotelhome.html')

#Login and signup

def signups(request):
    error_message = None
      # Initialize error message variable
    if request.method == 'POST':
        # Get form data
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(user_name)

        if not user_name or not email or not phone_number or not password or not confirm_password:
            error_message = 'All fields are required.'

        # Generate and send OTP to the user's phone number
        # Check if user with provided email or phone number already exists
        elif Userdetails.objects.filter(email=email).exists() or Userdetails.objects.filter(phone_number=phone_number).exists():
            error_message = 'User with this email or phone number already exists.'
        
        elif password != confirm_password:
            error_message = 'Passwords do not match'

        else:
            # Encrypt the password using MD5 hashing
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            print(hashed_password)

            # Create and save the user with encrypted password
            user = Userdetails(
                username=user_name,
                email=email,
                phone_number=phone_number,
                password=hashed_password
            )
            print(user)
            user.save()

            # Redirect to a success page or login page
            return JsonResponse({'success': True, 'success_message': 'Signup successful'})

    return JsonResponse({'success': False, 'error_message': error_message})

# def login_views(request):
#     error = None
#     if request.method == 'POST':
#         email_or_phone = request.POST.get('email_or_phone')
#         password = request.POST.get('password')
#         print(email_or_phone)
#         # Check if email_or_phone or password is empty
#         if not email_or_phone or not password:
#            error_message = 'Email/Phone and Password fields cannot be empty.'

#         # Check if the user exists with the given email or phone number
#         user = Userdetails.objects.filter(Q(email=email_or_phone) | Q(phone_number=email_or_phone)).first()

#         if user:
#             # Hash the provided password using MD5 hashing for comparison
#             hashed_password = hashlib.md5(password.encode()).hexdigest()

#             # Check if the hashed password matches the one stored in the database
#             if user.password == hashed_password:
#                 print(user.email)
#                 print(user.password)
#                 # client_details = Hotelclientdetails.objects.filter(email=user.email)
#                 # # Serialize the queryset to JSON
#                 # serialized_data = serialize('json', client_details)
                
#                 # # Initialize an empty dictionary to store hotel names and booking IDs
#                 # # Initialize an empty list to store hotel data
#                 # hotel_data = []

#                 # # Deserialize the JSON string to a list of dictionaries
#                 # deserialized_data = json.loads(serialized_data)
#                 # for entry in deserialized_data:
#                 #     # Extracting hotel name
#                 #     fields = entry['fields']
#                 #     user_info = fields.get('booking_information', {})
#                 #     datas = json.dumps(user_info)
#                 #     pdfs = fields.get('pdf_document', '')
#                 #     print(datas)
#                 #     hotel_name = user_info.get('hotel_name', {})
#                 #     booking_id = user_info.get('booking_id', '')

#                 #     # Store hotel name and booking ID in a dictionary
#                 #     entry_data = {'hotel_name': hotel_name, 'booking_id': booking_id,'datas':user_info}

#                 #     # Append entry data to the list
#                 #     hotel_data.append(entry_data)

#                 # print(hotel_data)
#                 # details_dict = json.loads(serialized_data)
#                 # print(details_dict)
#                 # template_path = "home/hotelreview.html"
#                 # # Authenticate user with the provided credentials
#                 # context = request.session.get('hotel_review')
#                 email = user.email
#                 phone_number = user.phone_number
#                 username = user.username
#                 # template = get_template(template_path)
#                 # html = template.render(context)
#                 # print(context)
#                 return JsonResponse({'success': True, 'email': email,'phone_number':phone_number,'username':username})
#                 # return render(request,'signup/success.html',{"email":user.email,"hotel_data":hotel_data})
#             else:
#                 # Password doesn't match, render login page with error message
#                  error_message = 'Invalid email/phone number or password.'

#         else:
#             # User not found, render login page with error message
#            error_message = 'User not found.'

#     # If the request method is not POST, render the login page
#     return JsonResponse({'success': False, 'error_message': error_message})


# def login_views(request):
#     error_message = None

#     if request.method == 'POST':
#         email_or_phone = request.POST.get('email_or_phone')
#         password = request.POST.get('password')

#         if not email_or_phone or not password:
#             error_message = 'Email/Phone and Password fields cannot be empty.'

#         else:
#             user = Userdetails.objects.filter(Q(email=email_or_phone) | Q(phone_number=email_or_phone)).first()

#             if user:
#                 hashed_password = hashlib.md5(password.encode()).hexdigest()

#                 if user.password == hashed_password:
#                     # Authentication successful
#                     # Proceed with your logic
#                     return HttpResponse('Authentication successful')

#                 else:
#                     error_message = 'Invalid email/phone number or password.'

#             else:
#                 error_message = 'User not found.'

#     return render(request, 'signup/signupsample.html', {'error': error_message})

# Link to the mail
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from cryptography.fernet import Fernet
import base64
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad


# Generate a Fernet key
key = Fernet.generate_key()

# Ensure that the key is URL-safe base64-encoded bytes

# Use the URL-safe key with Fernet
fernet = Fernet(key)


def send_pdf_link(phone_number,user,booking_id):
    # if request.method == 'POST':
    #     phone_number = request.POST.get('email')
    #     booking_id = request.POST.get('booking_id')

        # Encrypt the booking ID
        booked = str(booking_id)
        enc_message = fernet.encrypt(booked.encode())
        encrypted_token = base64.urlsafe_b64encode(enc_message).decode()

        # Construct the URL for downloading the PDF
        download_url = reverse('download_pdfview')

        # Construct the PDF download link with the URL
        download_link = f'{download_url}?token={encrypted_token}'

        send_whatsapp_message_3(phone_number,user, download_link)

       # Construct the email message
        subject = "Your PDF Download Link"
        message = f"Subject: {subject}\n\nDear User,\n\nPlease find the link to download your PDF: {download_link}"

        try:
            # Connect to the SMTP server
            s = smtplib.SMTP('smtppro.zoho.com', 587)
            s.starttls()

            # Login to the SMTP server
            s.login("tharun@vacationfeast.com", "nBvizb5wji94")

            # Send the email
            s.sendmail("bookings@vacationfeast.com", message.encode('utf-8'))
            s.quit()

            return JsonResponse({'success': True, 'download_link': download_link})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
def download_pdfview(request):
    if request.method == 'GET':
        encrypted_token = request.GET.get('token')
        print(encrypted_token)

        # Decrypt the encrypted token to get the booking ID
        enc_message = base64.urlsafe_b64decode(encrypted_token.encode())
        decrypted_number = fernet.decrypt(enc_message).decode()
        # decrypted_number = decrypt_number(key, encrypted_token)
        print("Decrypted number:", decrypted_number)
        booking_id = decrypted_number
        print(booking_id)
        template_path = 'home/pdf.html'
        hotel_client_details = Hotelclientdetails.objects.get(booking_id=booking_id)
        context = {
            'booking_details_1':hotel_client_details.booking_information,
            'User_Name':hotel_client_details.user_name,
            'phone_number':hotel_client_details.phone_number
        }
        print(context)
        # Create a Django response object, and specify content_type as pdf
        template = get_template(template_path)
        html = template.render(context)

        # Generate PDF

        # # Return a response indicating success
        # return HttpResponse('PDF successfully generated and saved to the database.')
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = f'filename="{hotel_client_details.booking_id}_payslip.pdf"'
        # find the template and render it.
        

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
            # hotel_client_details.pdf_document.save(f'{hotel_client_details.booking_id}_payslip.pdf', response)
        return response

def send_whatsapp_message_3(phone_number,user, download_link):
    gallabox_api_key = settings.GALLABOX_API_KEY
    gallabox_api_secret = settings.GALLABOX_API_SECRET
    gallabox_Channelid = settings.GALLABOX_CHANNELID
    url = "https://server.gallabox.com/devapi/messages/whatsapp"

    payload = json.dumps({
      "channelId": gallabox_Channelid,  # Replace with your channelId
      "channelType": "whatsapp",
      "recipient": {
        "name": "test",
        "phone": f"91{phone_number}"  # Recipient's phone number
      },
      "whatsapp": {
        "type": "template",
        "template": {
          "templateName": "website_for_pdf_link",
          "bodyValues": {
            "name": user,
          },
          "buttonValues": [
                {
                    "index": 0,
                    "sub_type": "url",
                    "parameters": {
                        "type": "text",
                        "text": download_link
                    }
                }
            ]
        }
      }
    })
    headers = {
      'apiSecret': gallabox_api_secret,  # Replace with your apiSecret
      'apiKey': gallabox_api_key,        # Replace with your apiKey
      'Content-Type': 'application/json'
    }
    print(payload)

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()