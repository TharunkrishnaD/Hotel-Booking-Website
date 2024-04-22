from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import datetime
import json
import math
import ast
from .models import NewCityListHotelCSV
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "home/flighthomepage.html")
def hotel(request):
    return render(request, "home/hotelhome.html")

def search_destinations(request):
    query = request.GET.get('query', '')
    results = NewCityListHotelCSV.objects.filter(
        Q(DESTINATION__icontains=query) | Q(COUNTRY__icontains=query)
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

def process_form(request):

    if request.method == 'POST':
        city_name = request.POST.get('cityname', '')
        cityid = request.POST.get('city_id', '')
        countrycode = request.POST.get('country_code', '')
        check_in_str = request.POST.get('check-in', '')
        check_out = request.POST.get('check-out', '')
        nationality = request.POST.get('nation', '')
        personsdetails = request.POST.get('roomInfoInput','')
        totalroom= request.POST.get('totalRoomInfoInput','')
        data = json.loads(personsdetails)
        no_of_adults = data[0]["NoOfAdults"]
        no_of_children = data[0]["NoOfChild"]
        print(personsdetails)
        data_dict = json.loads(totalroom)
        total_rooms = data_dict['TotalRooms']
        guest_details = f"{no_of_adults} Adults,{no_of_children} Childs,{total_rooms} Rooms"
        print(check_in_str)

        print(total_rooms)
        print(guest_details)

        check_in_date = datetime.datetime.strptime(check_in_str, '%d %B %Y')
        formatted_check_in_date =  check_in_date.strftime('%d/%m/%Y')
        print(formatted_check_in_date)

        check_out_date = datetime.datetime.strptime(check_out, '%d %B %Y')
        formatted_check_out_date = check_out_date.strftime('%d/%m/%Y')
        print(formatted_check_out_date)

        request.session['check_in_date'] = formatted_check_in_date
        request.session['check_out_date'] = formatted_check_out_date
        request.session['guestdetails'] = guest_details
        request.session['totalrooms'] = total_rooms
        request.session['adults'] = no_of_adults
        request.session['childs'] = no_of_children
        


    # Calculate the number of nights
        num_nights = (check_out_date - check_in_date).days
        request.session['No_of_Night'] = num_nights



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
                end_user_ip = '123.1.1.1'
                token_id = f"{token}"
                print(room_guests)

                hotel_info = get_hotel_results(api_url, api_key, check_in_date, no_of_nights, country_code, city_id,
                                               result_count, preferred_currency, guest_nationality, no_of_rooms, room_guests, max_rating, min_rating,
                                               is_nearby_search_allowed, end_user_ip, token_id)
                print(hotel_info)

                if hotel_info:

                    hotel_prices = hotel_info[-3]['HotelPrices']
                    # Getting the maximum and minimum prices
                    max_price = max(hotel_prices)
                    min_price = min(hotel_prices)

                    return render(request, 'home/listofhotel.html', {'hotel_info': hotel_info , 'token_id': token_id, 'nationality': city_name , 'min_price': min_price, 'max_price': max_price,'formatted_check_in_date':check_in_str ,'formatted_check_out_date':check_out,'num_nights':num_nights,})
                   
                    # return render(request, 'home/listofhotel.html', {'hotel_info': hotel_info , 'token_id': token_id, 'min_price': min_price, 'max_price': max_price,'formatted_check_in_date':formatted_check_in_date,'formatted_check_out_date':formatted_check_out_date,'num_nights':num_nights,})
                else:
                    error_message = "Error occurred during the hotel search request."
            else:
                print("Authentication failed:", response_data)
        
        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
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
    print(data)

    try:
        response = requests.post(url, json=data, headers=headers, params={'apiKey': api_key})
        response.raise_for_status()

        print("Status Code:", response.status_code)

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
            price = hotel.get('Price', {}).get('PublishedPriceRoundedOff', 0)
            hotel_code = hotel.get('HotelCode', '')
            hotel_category = hotel.get('HotelCategory', '')
            result_index = hotel.get('ResultIndex', None)


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

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()

        response_data = response.json().get('GetHotelRoomResult', {})

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
    hotel_code = request.POST.get('hotelCode', None)
    trace_id = request.POST.get('traceId', None)
    result_index = request.POST.get('resultIndex', None)
    token_id = request.POST.get('tokenId', None)

    check_in_date = request.session.get('check_in_date', '')
    check_out_date = request.session.get('check_out_date', '')
    guest_details = request.session.get('guestdetails', '')
    No_of_nights = request.session.get('No_of_Night','')





    # First API request
    api_url1 = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelInfo'
    headers1 = {
        'Content-Type': 'application/json',
    }
    data1 = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': '123.1.1.1',  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }

    try:
        response1 = requests.post(api_url1, json=data1, headers=headers1)
        response1.raise_for_status()

        response_data1 = response1.json().get('HotelInfoResult', {}).get('HotelDetails', {})
        print(response_data1)
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

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Second API request
    api_url2 = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetHotelRoom'
    headers2 = {
        'Content-Type': 'application/json',
    }
    data2 = {
        'ResultIndex': result_index,
        'HotelCode': hotel_code,
        'EndUserIp': '123.1.1.1',  # Replace with actual end user IP
        'TokenId': token_id,
        'TraceId': trace_id,
    }

    try:
        response2 = requests.post(api_url2, json=data2, headers=headers2)
        response2.raise_for_status()

        response_data2 = response2.json().get('GetHotelRoomResult', {})

        if response_data2.get('ResponseStatus') == 1:
            room_details = response_data2.get('HotelRoomsDetails', [])

            # Create a list to store formatted room details HTML
            formatted_rooms_html = []

            for room in room_details:
                room_json = json.dumps(room)
                data_json = json.dumps(data2)
                room_html = f"""
                    <div class="room-info">
                        <div>
                            <p class="room-info-name">{room.get('RoomTypeName', '')}</p>
                        </div>
                    </div>    
                    <div class="can-pol">
                        <p><a href="" >Cancellation Policy</a></p>
                    </div>
                    <div class="price-info">
                        <div class="rub-price">
                            <p>INR</p>
                            <p class="price">{room.get('Price', {}).get('PublishedPriceRoundedOff', 0)}</p>
                        </div>
                        <div>
                            <p>Per Room/Night</p>
                        </div>
                        <div class="hide-elements" style="display: none;">
                            <p class="room-json" style="display: none;">{room_json}</p>
                            <p class="data-json" style="display: none;">{data_json}</p>
                        </div>
                        <div>
                            <button class="btn btn-primary book-btn"  onclick="bookRoom1()">BOOK ROOM</button>
                        </div>
                    </div>
                """

                formatted_rooms_html.append(room_html)

            # Join the formatted HTML for all rooms
            all_rooms_html = ''.join(formatted_rooms_html)

            # Combine information from both API responses
            combined_info = {
                'hotel_info': extracted_info,
                'room_details_html': all_rooms_html,
            }
            print(combined_info)

            # Render the template to a string
            html_content = render_to_string('home/viewhotels.html', {'combined_info': combined_info})

            # Return the HTML content in the JSON response
            return JsonResponse({'html': html_content})
        else:
            error_message = response_data2.get('Error', {}).get('ErrorMessage', '')
            return JsonResponse({'error': error_message})

    except requests.exceptions.RequestException as ex:
        return JsonResponse({'error': f"Error: {ex}"})

def get_room_details(request):
    hotel_code = request.POST.get('hotelCode', None)
    trace_id = request.POST.get('traceId', None)
    result_index = request.POST.get('resultIndex', None)
    token_id = request.POST.get('tokenId', None)

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

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()

        response_data = response.json().get('GetHotelRoomResult', {})

        if response_data.get('ResponseStatus') == 1:
            room_details = response_data.get('HotelRoomsDetails', [])
            print(room_details)

            # Create a list to store formatted room details HTML
            formatted_rooms_html = []

            for room in room_details:
                room_json = json.dumps(room)
                data_json = json.dumps(data)
                room_html = f"""
                    <div class="hide-room1">
                        <div class="book-room">
                            <h3>{room.get('RoomTypeName', '')}</h3>
                            <p>{room.get('Breakfast', '')}</p>
                        </div>
                        <div class="book-room-price">
                            <p class="price">INR{room.get('Price', {}).get('PublishedPriceRoundedOff', 0)}</p>
                            <p>Per Room/Night</p>
                        </div>
                        <div class="hide-elements" style="display: none;">
                            <p class="tax">{room.get('Price', {}).get('Tax', 0)}</p>
                            <p class="room-json" style="display: none;">{room_json}</p>
                            <p class="data-json" style="display: none;">{data_json}</p>
                        </div>
                        <div class="book-room-btn">
                            <button class="btn btn-primary book-btn" onclick="bookRoom()">Book Room</button>
                        </div>
                    </div>
                """

                formatted_rooms_html.append(room_html)

            # Join the formatted HTML for all rooms
            all_rooms_html = ''.join(formatted_rooms_html)

            return JsonResponse({'room_details_html': all_rooms_html})
        else:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
            return JsonResponse({'error': error_message})

    except requests.exceptions.RequestException as ex:
        return JsonResponse({'error': f"Error: {ex}"})
def hotelreview(request):
    if request.method == 'POST':
        try:
            check_in_date = request.session.get('check_in_date', '')
            check_out_date = request.session.get('check_out_date', '')
            adults = request.session.get('adults', '')
            childs = request.session.get('childs', '')
            totalrooms = request.session.get('totalrooms', '')
            No_of_nights = request.session.get('No_of_Night','')
            payload = json.loads(request.body.decode('utf-8'))

            # Your view logic here
            print(payload)

            api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/BlockRoom'
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            # Handle the API response as needed
            api_response = response.json()
            print(api_response)
            block_room_result = api_response.get('BlockRoomResult', {})
            availability_type = block_room_result.get('AvailabilityType', '')
            hotel_rooms_details = block_room_result.get('HotelRoomsDetails', [])
            published_price = hotel_rooms_details[0].get('Price', {}).get('PublishedPrice', None)
            discount_amount = 0.05 * published_price

            # Calculate GST on the discounted price
            gst_amount = 0.18 * discount_amount

            # Calculate the final price after applying GST
            final_tax = math.ceil(gst_amount + discount_amount)

            # total price of the room
            total_price = math.ceil(final_tax + published_price)
            print(published_price)

            if availability_type == 'Confirm':
                # Extract required details into a dictionary
                details_dict = {
                    'hotel_name': block_room_result.get('HotelName', ''),
                    'rating': block_room_result.get('StarRating', 0),
                    'address': f"{block_room_result.get('AddressLine1', '')}, {block_room_result.get('AddressLine2', '')}",
                    'cancellation_policy': block_room_result.get('HotelPolicyDetail', ''),
                    'check_in_date':check_in_date,
                    'check_out_date':check_out_date,
                    'adults':adults,
                    'childs':childs,
                    'totalrooms':totalrooms,
                    'No_of_Night':No_of_nights,
                    'published_price':published_price,
                    'final_tax':final_tax,
                    'total_price':total_price
                }
                print(details_dict)

                # Pass the details dictionary to another HTML page

                html_content = render_to_string('home/hotelreview.html', {'details': details_dict})

            # Return the HTML content in the JSON response
                return JsonResponse({'html': html_content})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f"JSON decoding error: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)