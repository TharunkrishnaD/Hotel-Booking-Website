from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from html import unescape
from django.utils.html import strip_tags
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseServerError
from django.utils.html import escape
from django.http import HttpResponseBadRequest
import razorpay
import json
import ast

# Create your views here.
def empty(request):
    return render(request,"empty.html")



# "YOUR_ID", "YOUR_SECRET"
key = settings.RAZORPAY_MERCHANT_KEY
secret = settings.RAZORPAY_MERCHANT_SECRET

razorpay_client = razorpay.Client(auth=(key, secret))


from django.shortcuts import render

def paymentflight(request):
    print(key)
    values = request.session.get('published_amount')
    print("price values in payment",values)
    flightdetails = request.session.get('flight_details', '')
    single_flight_del = request.session.get('fullflight_details','')
    userinformation = request.session.get('userinformation','')
    preview_data = request.session.get('preview_data', None)
    
    print("new",type(values))
    print("preview data",preview_data)
    publish_amount = preview_data.get('flight_information', '')
   
    print(publish_amount)    
    email = preview_data.get('email', '')
    phone_number = preview_data.get('phone_number', '')


    combined_data = {
       
        'email':email,
        'phone_number': phone_number,
        # 'hotel_name': hotel_name,
        # 'rating': rating,
        # 'address': address,
        # 'cancellation_policy': stripped_content,
        # 'check_in_date': check_in_date,
        # 'check_out_date': check_out_date,
        # 'adults': adults,
        # 'childs': childs,
        # 'total_rooms': total_rooms,
        # 'no_of_nights': no_of_nights,
        # 'published_price': published_price,
        # 'final_tax': final_tax,
        # 'total_price': total_price,
        # 'time_difference':time_difference,
        'flight_details':flightdetails
    }
    
    # price =float(values)*100
    price = 200*100
    currency = 'INR'
    print(price)

    razorpay_order = razorpay_client.order.create(dict(amount=price,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'Flightpaymenthandler/'
    context = {
        'flightdetails': flightdetails,
        'single_flight_del':single_flight_del,
        'userinformation' : userinformation,
        'combined_data': combined_data,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': "rzp_test_5bpcghNaRd7Qqg",
        'razorpay_amount': price,
        'currency': 'INR',
        'callback_url': callback_url,
        'hidden_email':'gokul@gmail.com','hidden_phone_number':9360461524,'hidden_username':'hidden_username',
    } 
    # print(context)

    # Render the template with the context
    return render(request, 'payment/paymentflight.html',context=context)


@csrf_exempt
def Flightpaymenthandler(request):

    value = request.session.get('publish_amount', None)
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            request.session['payment_id'] = payment_id
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            print(razorpay_order_id)
            signature = request.POST.get('razorpay_signature', '')
            payed_amount = request.POST.get('razorpay_amount', '')
            print({'payed': payed_amount})
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
                'razorpay_amount': payed_amount,
            }
            
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            
            return redirect(reverse('onetrip_book'))
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()





    return render(request,'payment/empty.html')

    # return redirect(reverse('hotelbooked'))


# hotel bookimg 
def home(request):
    try:
        print(key)
        value = request.session.get('total_price', None)
        preview_data = request.session.get('preview_data', None)
        current_time_extra = request.session.get('current_time_extra', None)
        current_time = request.session.get('current_time', None)
        future_time = request.session.get('future_time', None)
        formatted_hotel_room_details = request.session.get('formatted_hotel_room_details',None)
        print(formatted_hotel_room_details)
        total_guests = request.session.get('total_guests',None)
        hidden_email = request.session.get('hidden_email','')
        hidden_phone_number = request.session.get('hidden_phone_number','')
        hidden_username = request.session.get('hidden_username','')
        print(total_guests)
        # Extract hotel name and offer price
        hotel_details = []
        for detail in formatted_hotel_room_details:
            hotel_detail = {}
            hotel_detail["HotelName"] = detail["RoomTypeName"]  # Replace this with the actual hotel name extraction logic
            hotel_detail["OfferedPrice"] = detail["Price"]["OfferedPrice"]
            # for detail in total_guests:
            #     hotel_detail["total_guest"] = detail["TotalGuests"]
            hotel_details.append(hotel_detail)


        print(hotel_details)
        print(future_time)
        print(current_time)
        print(current_time_extra)
        # Parse the input string into a datetime object
        # parsed_time = datetime.strptime(current_time_extra, "%b %d %Y %H:%M:%S")

        # # Format the datetime object into the desired format
        # previous_time = parsed_time.strftime("%Y-%m-%d %H:%M:%S")
        previous_time = datetime.strptime(current_time_extra, "%b %d %Y %H:%M:%S")

    #     input_time = datetime.strptime(current_time_extra, "%Y-%m-%d %H:%M:%S GMT%z (India Standard Time)")
    # # Format the datetime object into the desired format
    #     # previous_time = input_time.strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(future_time, "%Y-%m-%d %H:%M:%S")
    #     previous_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    #     # Calculate the time difference
        time_difference = current_time - previous_time
        # Print the time difference in hours, minutes, and seconds
        print("Time Difference:", time_difference)
        user_name = preview_data.get('user_name', '')
        email = preview_data.get('email', '')
        phone_number = preview_data.get('phone_number', '')

        room_information = request.session.get('details_dict', None)
        print(room_information)
        
        
        hotel_name = room_information.get('hotel_name', '')
        rating = room_information.get('rating', '')
        address = room_information.get('address', '')
        cancellation_policy = room_information.get('cancellation_policy', '')
        # Unescaping HTML entities
        stripped_content = unescape(cancellation_policy)
        index_of_checkin = stripped_content.find("CheckIn")

        # Remove all content before the "CheckIn"
        stripped_content = stripped_content[index_of_checkin:]

        # Removing HTML tags
        # stripped_content = unescaped_content.split('||', 1)[-1]

        print(stripped_content)
        check_in_date = room_information.get('check_in_date', '')
        check_out_date = room_information.get('check_out_date', '')
        adults = room_information.get('adults', 0)
        childs = room_information.get('childs', 0)
        total_rooms = room_information.get('totalrooms', 0)
        no_of_nights = room_information.get('No_of_Night', 0)
        published_price = room_information.get('published_price', 0.0)
        final_tax = room_information.get('final_tax', '')
        total_price = room_information.get('total_price', '')
        combined_data = {
            'user_name': user_name,
            'email': email,
            'phone_number': phone_number,
            'hotel_name': hotel_name,
            'rating': rating,
            'address': address,
            'cancellation_policy': stripped_content,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'adults': adults,
            'childs': childs,
            'total_rooms': total_rooms,
            'no_of_nights': no_of_nights,
            'published_price': published_price,
            'final_tax': final_tax,
            'total_price': total_price,
            'time_difference':time_difference,
            'hotel_details':hotel_details
        }
        
        # payed_amount = preview_data.get('payed_amount', '')
        # if value is not None and value == total_price:
        price = value*100
        # price = 20000
        currency = 'INR'
        print(price)

        razorpay_order = razorpay_client.order.create(dict(amount=price,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
        # context = {}
        # context['razorpay_order_id'] = razorpay_order_id
        # context['razorpay_merchant_key'] = "rzp_test_5bpcghNaRd7Qqg"
        # context['razorpay_amount'] = price
        # context['currency'] = currency
        # context['callback_url'] = callback_url

        context = {
        'combined_data': combined_data,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': key,
        'razorpay_amount': price,
        'currency': 'INR',
        'callback_url': callback_url,
        'hidden_email':hidden_email,'hidden_phone_number':hidden_phone_number,'hidden_username':hidden_username,
        }
    
        return render(request, 'payment/payment.html', context=context,)
    except Exception as e:
        # Log the error if needed
        print("An error occurred:", e)
        error_message = "Sorry for the error,if the payment is done the amount will be refunded"
        # Render the error template
        return HttpResponseServerError(render(request, 'payment/error.html' , {'error_message': error_message}))

    if request.method == "POST":
        amount = price
        

        payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
    return render(request, 'payment/payment.html' , {'price': price})
    # else:
    #      print("The values are not equal or 'total_price' is not in the session.")

# @csrf_exempt
# def success(request):
#     print("success")
#     return redirect(reverse('hotelbooked'))
#     # return render(request, "payment/success.html")
# # def order_payment(request):
# #     if request.method == "POST":
# #         amount = request.POST.get("amount")
# #         client = razorpay.Client(auth=("LVrsvsQjYwYh8RATwpnd3XHQ", "rzp_test_xnTIynqnQBCTTm"))
# #         razorpay_order = client.order.create(
# #             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
# #         )
# #         # order = Order.objects.create(
# #         #     name=name, amount=amount, provider_order_id=razorpay_order["id"]
# #         # )
# #         # order.save()
# #         # return render(
# #         #     request,
# #         #     "payment.html",
# #         # )
# #     return render(request, "payment.html")
# # # Create your views here.
# # @csrf_exempt
# # def success(request):
# #     return render(request, "success.html")
@csrf_exempt
def paymenthandler(request):

    value = request.session.get('total_price', None)
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            request.session['payment_id'] = payment_id
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            print(razorpay_order_id)
            signature = request.POST.get('razorpay_signature', '')
            payed_amount = request.POST.get('razorpay_amount', '')
            print(payed_amount)
            print({'payed': payed_amount})
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
                'razorpay_amount': payed_amount,
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            return redirect(reverse('hotelbooked'))
            if result is not None:
                amount = value  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()