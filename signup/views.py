from django.shortcuts import render
from .models import Userdetails
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
import hashlib
import random
import datetime
import json
from requests.exceptions import HTTPError
from django.http import JsonResponse
import requests
from django.conf import settings
from email.mime.text import MIMEText
from booking.models import Hotelclientdetails
import smtplib
from datetime import datetime


def portalhome(request):
    current_date = datetime.now().date()

    filtered_hotel_data = []
    # Retrieve session variables
    hidden_email = request.session.get('hidden_email', '')
    hidden_phone_number = request.session.get('hidden_phone_number', '')
    hidden_username = request.session.get('hidden_username', '')

    # Check if session variables are empty
    if not hidden_email or not hidden_phone_number or not hidden_username:
        return render(request, 'booking/home/error.html', {'error_message': 'Session variables are missing.'})

    client_details = Hotelclientdetails.objects.filter(email=hidden_email, phone_number=hidden_phone_number)

    # Serialize the queryset to JSON
    serialized_data = serialize('json', client_details)
    
    # Initialize an empty dictionary to store hotel names and booking IDs
    # Initialize an empty list to store hotel data
    hotel_data = []

    # Deserialize the JSON string to a list of dictionaries
    deserialized_data = json.loads(serialized_data)
    print(deserialized_data)
    for entry in deserialized_data:
        # Extracting hotel name
        fields = entry['fields']
        booking_information = fields.get('booking_information')
        if not booking_information:
           continue
        user_info = booking_information
        datas = json.dumps(user_info)
        pdfs = fields.get('pdf_document', '')
        print(datas)
        hotel_name = user_info.get('hotel_name', {})
        booking_id = user_info.get('booking_id', '')
        initial_checkin_date = user_info.get('initial_checkin_date', '')

        # Store hotel name and booking ID in a dictionary
        entry_data = {'hotel_name': hotel_name, 'booking_id': booking_id,'datas':user_info}

        # Append entry data to the list
        hotel_data.append(entry_data)
        check_in_date_str = user_info.get('check_in_date')

    total_hotel_booking = len(hotel_data)
    print(total_hotel_booking)

    # Convert check_in_date string to a datetime object
    # check_in_date = datetime.strptime(check_in_date_str, '%d %b %Y').date()

    # # Filter datas based on current and future dates
    # if check_in_date >= current_date:
    #     datas = json.dumps(user_info)
    #     pdfs = fields.get('pdf_document', '')
    #     hotel_name = user_info.get('hotel_name', {})
    #     booking_id = user_info.get('booking_id', '')

    #     # Store hotel name and booking ID in a dictionary
    #     entry_data = {'hotel_name': hotel_name, 'booking_id': booking_id, 'datas': user_info}

    #     # Append entry data to the list
    #     filtered_hotel_data.append(entry_data)

    # cancelation_hotel = Hotelclientdetails.objects.filter(email=hidden_email, changerequestid__isnull=False)
        

    # print(hotel_data)
    details_dict = json.loads(serialized_data)
    # print(details_dict)
    return render(request, 'signup/portalhome.html',{'total_hotel_booking':total_hotel_booking,'hidden_username': hidden_username})

    
def flightportal(request):
    return render(request, 'signup/flightportal.html')
def hotelhistory(request):
    current_date = datetime.now().date()
    print(current_date)

    hidden_email = request.session.get('hidden_email', '')
    hidden_phone_number = request.session.get('hidden_phone_number', '')
    hidden_username = request.session.get('hidden_username', '')

    if not hidden_email or not hidden_phone_number or not hidden_username:
        return render(request, 'booking/home/error.html', {'error_message': 'Session variables are missing.'})

    client_details = Hotelclientdetails.objects.filter(email=hidden_email, phone_number=hidden_phone_number)
    # Serialize the queryset to JSON
    serialized_data = serialize('json', client_details)
    deserialized_data = json.loads(serialized_data)

    Hotel_history = []
    for entry in deserialized_data:
        fields = entry['fields']
        booking_id = fields.get('booking_id', '')
        changerequestid = fields.get('changerequestid', '')
        print(booking_id)

        # Skip processing if booking_id is empty
        if not booking_id:
            continue

        booking_information = fields.get('booking_information')

        # Skip processing if booking_information is empty
        if not booking_information:
            continue

        user_info = booking_information
        print(user_info)
        # Extracting relevant information
        check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()
        check_out_date = datetime.strptime(user_info['initial_checkout_date'], '%b %d %Y %H:%M:%S').date()

        # Calculate total nights
        total_nights = (check_out_date - check_in_date).days

        # Extracting relevant information
        check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()

        # Testing
        # current_date = datetime.strptime(current_date, '%b %d %Y %H:%M:%S').date()

        # Check if check-in date is on or after the current date
        if check_in_date <= current_date:
            booking_details = {
                'booking_id': booking_id,
                'hotel_name': user_info['hotel_name'],
                'star_rating': user_info['star_rating'],
                'address_line_1': user_info['address_line_1'],
                'address_line_2': user_info['address_line_2'],
                'check_in_date': check_in_date.strftime('%b %d %Y'),
                'check_out_date': check_out_date.strftime('%b %d %Y'),
                'total_nights': total_nights
            }

            # Fetch paid amount using booking_id
            try:
                booking_details['paid_amount'] = Hotelclientdetails.objects.get(booking_id=booking_id).payed_amount
            except Hotelclientdetails.DoesNotExist:
                booking_details['paid_amount'] = None
            # Fetch paid amount using booking_id
            try:
                booking_details['changerequestid'] = Hotelclientdetails.objects.get(booking_id=booking_id).changerequestid
            except Hotelclientdetails.DoesNotExist:
                booking_details['changerequestid'] = None

            Hotel_history.append(booking_details)

    print(Hotel_history)
    return render(request, 'signup/hotelhistory.html', {'upcoming_bookings': Hotel_history,'hidden_username': hidden_username})

def hotelcancelled(request):
     # Retrieve session variables
    hidden_email = request.session.get('hidden_email', '')
    hidden_phone_number = request.session.get('hidden_phone_number', '')
    hidden_username = request.session.get('hidden_username', '')

    if not hidden_email or not hidden_phone_number or not hidden_username:
        return render(request, 'booking/home/error.html', {'error_message': 'Session variables are missing.'})

    client_details = Hotelclientdetails.objects.filter(email=hidden_email, phone_number=hidden_phone_number)
    # Serialize the queryset to JSON
    serialized_data = serialize('json', client_details)
    deserialized_data = json.loads(serialized_data)

    Canceled_hotel = []
    for entry in deserialized_data:
        fields = entry['fields']
        booking_id = fields.get('booking_id', '')
        changerequestid = fields.get('changerequestid', '')
        print(booking_id)

        # Skip processing if booking_id is empty
        if not booking_id:
            continue

        booking_information = fields.get('booking_information')

        # Skip processing if booking_information is empty
        if not booking_information:
            continue

        user_info = booking_information
        print(user_info)
        if changerequestid:
           # Extracting relevant information
            check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()
            check_out_date = datetime.strptime(user_info['initial_checkout_date'], '%b %d %Y %H:%M:%S').date()

            # Calculate total nights
            total_nights = (check_out_date - check_in_date).days

            # Extracting relevant information
            check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()

            # Testing
            dummy_date_string = 'Jan 05 2024 00:00:00'
            current_date = datetime.strptime(dummy_date_string, '%b %d %Y %H:%M:%S').date()

            # Check if check-in date is on or after the current date
            if check_in_date >= current_date:
                booking_details = {
                    'booking_id': booking_id,
                    'hotel_name': user_info['hotel_name'],
                    'star_rating': user_info['star_rating'],
                    'address_line_1': user_info['address_line_1'],
                    'address_line_2': user_info['address_line_2'],
                    'check_in_date': check_in_date.strftime('%b %d %Y'),
                    'check_out_date': check_out_date.strftime('%b %d %Y'),
                    'total_nights': total_nights
                }

                # Fetch paid amount using booking_id
                try:
                    booking_details['paid_amount'] = Hotelclientdetails.objects.get(booking_id=booking_id).payed_amount
                except Hotelclientdetails.DoesNotExist:
                    booking_details['paid_amount'] = None
                # Fetch paid amount using booking_id
                try:
                    booking_details['changerequestid'] = Hotelclientdetails.objects.get(booking_id=booking_id).changerequestid
                except Hotelclientdetails.DoesNotExist:
                    booking_details['changerequestid'] = None

                Canceled_hotel.append(booking_details)

    print(Canceled_hotel)
    return render(request, 'signup/hotelcancel.html', {'upcoming_bookings': Canceled_hotel,'hidden_username': hidden_username})

def upcominghotel(request):
    current_date = datetime.now().date()

    # Retrieve session variables
    hidden_email = request.session.get('hidden_email', '')
    hidden_phone_number = request.session.get('hidden_phone_number', '')
    hidden_username = request.session.get('hidden_username', '')

    if not hidden_email or not hidden_phone_number or not hidden_username:
        return render(request, 'booking/home/error.html', {'error_message': 'Session variables are missing.'})

    client_details = Hotelclientdetails.objects.filter(email=hidden_email, phone_number=hidden_phone_number)
    # Serialize the queryset to JSON
    serialized_data = serialize('json', client_details)
    deserialized_data = json.loads(serialized_data)
    # print(deserialized_data)

    upcoming_bookings = []

    for entry in deserialized_data:
        fields = entry['fields']
        booking_id = fields.get('booking_id', '')
        changerequestid = fields.get('changerequestid', '')
        print(booking_id)
        # print(changerequestid)

        # Skip processing if booking_id is empty
        if not booking_id or changerequestid is not None:
            continue

        booking_information = fields.get('booking_information')

        # Skip processing if booking_information is empty
        if not booking_information:
            continue

        user_info = booking_information
        # print(user_info)
        check_in_date_str = user_info.get('initial_checkin_date', None)
        if check_in_date_str:
           # Extracting relevant information
            check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()
            check_out_date = datetime.strptime(user_info['initial_checkout_date'], '%b %d %Y %H:%M:%S').date()

            # Calculate total nights
            total_nights = (check_out_date - check_in_date).days

            # Extracting relevant information
            check_in_date = datetime.strptime(user_info['initial_checkin_date'], '%b %d %Y %H:%M:%S').date()

            # Testing
            # dummy_date_string = 'Jan 05 2024 00:00:00'
            # current_date = datetime.strptime(dummy_date_string, '%b %d %Y %H:%M:%S').date()

            # Check if check-in date is on or after the current date
            if check_in_date >= current_date:
                booking_details = {
                    'booking_id': booking_id,
                    'hotel_name': user_info['hotel_name'],
                    'star_rating': user_info['star_rating'],
                    'address_line_1': user_info['address_line_1'],
                    'address_line_2': user_info['address_line_2'],
                    'check_in_date': check_in_date.strftime('%b %d %Y'),
                    'check_out_date': check_out_date.strftime('%b %d %Y'),
                    'total_nights': total_nights
                }

                # Fetch paid amount using booking_id
                try:
                    booking_details['paid_amount'] = Hotelclientdetails.objects.get(booking_id=booking_id).payed_amount
                except Hotelclientdetails.DoesNotExist:
                    booking_details['paid_amount'] = None

                upcoming_bookings.append(booking_details)
    print(upcoming_bookings)
    
    return render(request, 'signup/hotelupcoming.html', {'upcoming_bookings': upcoming_bookings,'hidden_username': hidden_username})
def send_whatsapp_message(user_name,phone_number,otp):
    gallabox_api_key = settings.GALLABOX_API_KEY
    gallabox_api_secret = settings.GALLABOX_API_SECRET
    gallabox_Channelid = settings.GALLABOX_CHANNELID
    url = "https://server.gallabox.com/devapi/messages/whatsapp"

    payload = json.dumps({
      "channelId": gallabox_Channelid,  # Replace with your channelId
      "channelType": "whatsapp",
      "recipient": {
        "name": user_name,
        "phone": f"91{phone_number}"  # Recipient's phone number
      },
      "whatsapp": {
        "type": "template",
        "template": {
          "templateName": "registration_website",
          "bodyValues": {
            "Name": user_name,
            "variable_2": otp
          }
        }
      }
    })
    headers = {
      'apiSecret': gallabox_api_secret,  # Replace with your apiSecret
      'apiKey': gallabox_api_key,        # Replace with your apiKey
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def send_email(otp,recipient_email):
    try:
        email_subject = "Vacation Feast OTP"
        email_message = f"Your OTP: {otp}"
        # Create an SMTP session
        s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        s.starttls()  # Start TLS for security
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Authentication

        # Construct the email message
        msg = MIMEText(email_message)
        msg['Subject'] = email_subject
        msg['From'] = "bookings@vacationfeast.com"
        msg['To'] = recipient_email

        # Send the email
        s.sendmail("bookings@vacationfeast.com", recipient_email, msg.as_string())
        
        # Close the SMTP session
        s.quit()

        return True
    except Exception as e:
        print("Error:", e)
        return False
    
def send_otp(request):
    # phone_number = request.POST.get('phone_number')
    # print(phone_number)
    """
    Function to send OTP to the provided phone number
    (You may need to use a third-party service for sending OTP via SMS)
    """
    # Generate a 4-digit OTP
   
    # Code to send OTP to the user's phone number (e.g., via SMS)
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        
        # Generate OTP and send it to the provided phone number (implement this logic)
        otp = str(random.randint(1000, 9999)) 
        request.session['otp'] = {
            'value': otp,
            'created_at': str(datetime.now())  # Convert datetime object to string
        }
        print(otp)

        recipient_email = email
        
        # Sending OTP via email
        email_sent = send_email(otp,recipient_email)
        
        whatsapp_response = send_whatsapp_message(user_name,phone_number,otp)

        # Assuming OTP sending is successful, return a JSON response
        if otp:
            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to send OTP'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        print(otp_entered)
        print(saved_otp)
        if saved_otp and 'value' in saved_otp and 'created_at' in saved_otp:
            otp_value = saved_otp['value']
            otp_created_at = datetime.strptime(saved_otp['created_at'], '%Y-%m-%d %H:%M:%S.%f')  # Convert string to datetime object
            current_time = datetime.now()
            time_difference = current_time - otp_created_at
            
            if otp_entered == otp_value and time_difference.total_seconds() <= 180:  # 180 seconds = 3 minutes
                # OTP is valid
                return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
        
        # OTP is either invalid or expired
        return JsonResponse({'success': False, 'message': 'Invalid or expired OTP'})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'})

# def signup(request):
#     error_message = None
#       # Initialize error message variable
#     if request.method == 'POST':
#         # Get form data
#         user_name = request.POST.get('user_name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         print(user_name)

#         if not user_name or not email or not phone_number or not password or not confirm_password:
#             error_message = 'All fields are required.'

#         # Generate and send OTP to the user's phone number
#         # Check if user with provided email or phone number already exists
#         elif Userdetails.objects.filter(email=email).exists() or Userdetails.objects.filter(phone_number=phone_number).exists():
#             error_message = 'User with this email or phone number already exists.'
        
#         elif password != confirm_password:
#             error_message = 'Passwords do not match'

#         else:
#             # Encrypt the password using MD5 hashing
#             hashed_password = hashlib.md5(password.encode()).hexdigest()
#             print(hashed_password)

#             # Create and save the user with encrypted password
#             user = Userdetails(
#                 username=user_name,
#                 email=email,
#                 phone_number=phone_number,
#                 password=hashed_password
#             )
#             print(user)
#             user.save()

#             # Redirect to a success page or login page
#             return render(request, 'signup/thankyou.html')
#     return render(request, 'signup/loginsample.html', {'error_message': error_message})
# Create your views here.
def signup_view(request):
    return render(request, 'signup/signupsample.html')

from django.contrib.auth import authenticate, login
import re
from django.core.serializers import serialize
from django.contrib import messages

def login_view(request):
    error = None
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        print(email_or_phone)
        # Check if email_or_phone or password is empty
        if not email_or_phone or not password:
            return render(request, 'signup/signupsample.html', {'error': 'Email/Phone and Password fields cannot be empty.'})

        # Check if the user exists with the given email or phone number
        user = Userdetails.objects.filter(Q(email=email_or_phone) | Q(phone_number=email_or_phone)).first()

        if user:
            # Hash the provided password using MD5 hashing for comparison
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            # Check if the hashed password matches the one stored in the database
            if user.password == hashed_password:
                print(user.email)
                print(user.password)
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
                template_path = "home/hotelreview.html"
                # Authenticate user with the provided credentials
                context = request.session.get('hotel_review')
                context['useremail'] = user.email
                context['userphone'] = user.phone_number
                template = get_template(template_path)
                html = template.render(context)
                print(context)
                return HttpResponse(html)
                return render(request, 'home/hotelreview.html')
                # return render(request,'signup/success.html',{"email":user.email,"hotel_data":hotel_data})
            else:
                # Password doesn't match, render login page with error message
                return render(request, 'signup/signupsample.html', {'error': 'Invalid email/phone number or password.'})
        else:
            # User not found, render login page with error message
            return render(request, 'signup/signupsample.html', {'error': 'User not found.'})

    # If the request method is not POST, render the login page
    return render(request, 'signup/signupsample.html')

def success(request):
    email = request.POST.get('email')
    success = "success"
    return render(request,'signup/success.html',{"success":email})
def check_cancel(request):
    if request.method == 'POST':
        # Retrieve booking_id and remark from POST data
        booking_id = request.POST.get('booking_id')
    # Get the record with the given booking_id, non-null changerequestid, and non-null remarks
        booking_details = Hotelclientdetails.objects.filter(booking_id=booking_id, changerequestid__isnull=False, remarks__isnull=False).first()
        if booking_details:
            remarks = booking_details.remarks
            return JsonResponse({'bookingid': booking_id,'remarks':remarks})
            print(f"Remarks for booking ID {booking_id}: {remarks}")
        else:
            return JsonResponse({'bookingid': booking_id,'remarks':"None"})
            print(f"No change request found with remarks for booking ID: {booking_id}")
def cancel_booking(request):
    if request.method == 'POST':
        # Retrieve booking_id and remark from POST data
        booking_id = request.POST.get('booking_id')
        remark = request.POST.get('remark')
        client_ip = request.session.get('client_ip','')
        print(remark)

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
            if response.status_code == 200:
                api_data = response.json()

            #     # Construct the file path on the C drive
            #     c_drive_path = "C:\Response"
            #     file_name = "auth.txt"
            #     notepad_file_path = os.path.join(c_drive_path, file_name)

            # # Open the file in write mode ("w") to overwrite existing content
            # with open(notepad_file_path, "w") as notepad_file:
            #     notepad_file.write(str(api_data))

            if response_data.get('TokenId', None):
                token = response_data['TokenId']
                print("Authentication successful. Token:", token)
                api_url = 'http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/SendChangeRequest'
                end_user_ip = "192.168.11.120"

                payload = {
                    "BookingMode": 5,
                    "RequestType": 4,
                    "Remarks": remark,
                    "BookingId": booking_id,
                    "EndUserIp": client_ip,
                    "TokenId": token
                }

                headers = {
                    'Content-Type': 'application/json'
                }

                try:
                    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
                    response.raise_for_status()  # Raise an exception for HTTP errors (status codes >= 400)
                    data = response.json()
                    Hotelclientdetails.objects.filter(booking_id=booking_id).update(remarks = remark)
                    change_request_id = data['HotelChangeRequestResult']['ChangeRequestId']
                    print(change_request_id)
                    print("Success:", data)
                    url = "http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetChangeRequestStatus/"
                    payload = {
                        "BookingMode": 5,
                        "ChangeRequestId": change_request_id,
                        "EndUserIp": "123.1.1.1",
                        "TokenId": token
                    }
                    response = requests.post(url, json=payload)
                    data2 = response.json()
                    Hotelclientdetails.objects.filter(booking_id=booking_id).update(changerequestid = change_request_id)
                    change_request_status = data2['HotelChangeRequestStatusResult']['ChangeRequestStatus']
                    print("Change Request Status:", change_request_status)
                    print(data2)
                    status_mapping = {
                        0: 'NotSet',
                        1: 'Pending',
                        2: 'InProgress',
                        3: 'Processed',
                        4: 'Rejected'
                    }

                    # Access the ChangeRequestStatus from data2
                    change_request_status = data2['HotelChangeRequestStatusResult']['ChangeRequestStatus']

                    # Assign the content according to the mapping
                    content = status_mapping.get(change_request_status, 'Unknown')
                    Hotelclientdetails.objects.filter(booking_id=booking_id).update(cancel_status = content)
                    print(content)
                    if change_request_status == 3:
                        # Extract CancellationCharge and RefundedAmount
                        cancellation_charge = data2['HotelChangeRequestStatusResult']['CancellationCharge']
                        refunded_amount = data2['HotelChangeRequestStatusResult']['RefundedAmount']
                        
                        # Create a new JSON object
                        new_json = {
                            'CancellationCharge': cancellation_charge,
                            'RefundedAmount': refunded_amount
                        }
                        
                        # Convert to JSON format
                        new_json_str = json.dumps(new_json)
                        Hotelclientdetails.objects.filter(booking_id=booking_id).update(cancellation_details = new_json_str)
                        
                        print(new_json_str)

                        return JsonResponse({'result': new_json_str})

                    return JsonResponse({'result': content})

                        
                    # Handle success response if needed
                except requests.exceptions.RequestException as e:
                    print("Error:", e)
                    # Handle error response if needed

        
        except requests.exceptions.RequestException as ex:
            print(f"Error: {ex}")
def cancel_status(request):
    if request.method == 'POST':
        # Retrieve booking_id and remark from POST data
        book_id = request.POST.get('booking_id')
        hotel_client_details = Hotelclientdetails.objects.get(booking_id=book_id)
        change_request_id = hotel_client_details.changerequestid
        print(change_request_id)
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
            if response.status_code == 200:
                api_data = response.json()

            if response_data.get('TokenId', None):
                token = response_data['TokenId']
                print("Authentication successful. Token:", token)
            
                url = "http://api.tektravels.com/BookingEngineService_Hotel/hotelservice.svc/rest/GetChangeRequestStatus/"
                payload = {
                    "BookingMode": 5,
                    "ChangeRequestId": change_request_id,
                    "EndUserIp": "123.1.1.1",
                    "TokenId": token
                }
                print(payload)
                response = requests.post(url, json=payload)
                data2 = response.json()
                print(data2)
                status_mapping = {
                    0: 'NotSet',
                    1: 'Pending',
                    2: 'InProgress',
                    3: 'Processed',
                    4: 'Rejected'
                }

                # Access the ChangeRequestStatus from data2
                change_request_status = data2['HotelChangeRequestStatusResult']['ChangeRequestStatus']

                # Assign the content according to the mapping
                content = status_mapping.get(change_request_status, 'Unknown')
                Hotelclientdetails.objects.filter(booking_id=book_id).update(cancel_status = content)
                print(content)
                if change_request_status == 3:
                    # Extract CancellationCharge and RefundedAmount
                    cancellation_charge = data2['HotelChangeRequestStatusResult']['CancellationCharge']
                    refunded_amount = data2['HotelChangeRequestStatusResult']['RefundedAmount']
                    
                    # Create a new JSON object
                    new_json = {
                        'CancellationCharge': cancellation_charge,
                        'RefundedAmount': refunded_amount
                    }
                    
                    # Convert to JSON format
                    new_json_str = json.dumps(new_json)
                    Hotelclientdetails.objects.filter(booking_id=book_id).update(cancellation_details = new_json_str)
                    
                    print(new_json_str)

                    return JsonResponse({'result': new_json_str})

                return JsonResponse({'result': content})

                    
                # Handle success response if needed
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            # Handle error response if needed

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, Http404, FileResponse
import io
def download_pdf(request, pk):
    template_path = 'signup/downloadpdf.html'
    hotel_client_details = Hotelclientdetails.objects.get(booking_id=pk)
    context = {
        'booking_details_1': hotel_client_details.booking_information,
        'User_Name': hotel_client_details.user_name,
        'phone_number': hotel_client_details.phone_number
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{hotel_client_details.booking_id}_payslip.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

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


def send_pdf_link(request):
    if request.method == 'POST':
        phone_number = request.POST.get('email')
        booking_id = request.POST.get('booking_id')
        print(type(booking_id))

        # Encrypt the booking ID
        enc_message = fernet.encrypt(booking_id.encode())
        encrypted_token = base64.urlsafe_b64encode(enc_message).decode()

        # Construct the URL for downloading the PDF
        download_url = reverse('download_pdf')

        # Construct the PDF download link with the URL
        download_link = f'{download_url}?token={encrypted_token}'

        send_whatsapp_message_2(phone_number, download_link)

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

    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def download_pdf(request):
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

def send_whatsapp_message_2(phone_number, download_link):
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
            "name": 'nAME',
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
# def decrypt_encrypted_token(encrypted_token):
#     try:
#         # Convert the hexadecimal string to bytes
#         token_bytes = bytes.fromhex(encrypted_token)

#         # Decode the bytes from base64
#         decoded_bytes = base64.urlsafe_b64decode(token_bytes)

#         # Hash the decoded bytes to get the booking ID
#         booking_id = hashlib.sha256(decoded_bytes).hexdigest()

#         return booking_id
#     except (ValueError, TypeError):
#         # Handle invalid input or decoding errors
#         return None  # Or raise an exception, log an error, etc.