from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Rooms, Members
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def homepage(request):
    return render(request, 'index.html', {'roomNotExist':0})

def createRoom(request):
    Name = request.POST['name']
    RoomID = request.POST['rmId']
    Username = request.POST['username']
    Password = request.POST['password']
    
    try:
        room = Rooms.objects.get(Room_Name=RoomID)
    except:
        room = Rooms.objects.create(Admin=Name, Room_Name=RoomID, Username=Username, Password=Password)
        room.save()

    return render(request, 'room.html', { 'roomName':RoomID, 'balance':room.Balance })

def joinRoom(request):
    try:
        Name = request.POST['name']
        PaymentID = request.POST['pId']
        RoomID = request.POST['rmId']
        room = Rooms.objects.get(Room_Name = RoomID)
        try:
            m = room.members_set.get(Mem_Name=Name)
        except:
            m = room.members_set.create(Mem_Name=Name, RoomId=RoomID, PayId=PaymentID)
            m.save()

        global nm
        nm = Name

        members = []
        for m in room.members_set.all():
            members.append((m.Mem_Name, m.PayId, m.Balance))
        roomDetails = {
            'roomName':RoomID,
            'roomAdmin':room.Admin,
            'roomBalance':room.Balance,
            'members':members
        }

        return render(request, 'room.html', roomDetails)
    except:
        return render(request, 'index.html', {'roomNotExist':1})
 

def confirm(request):
    try:
        Amount = request.POST['amount']
        RoomId = request.POST['roomId']
        currency = 'INR'
        room = Rooms.objects.get(Room_Name=RoomId)
        assert(int(Amount) >= 1)
    except:
        return render(request, 'paymentFail.html', {'statement':"Data entered is not correct"})

    global amt, rm
    amt = int(Amount)*100
    rm = room

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amt, currency=currency, payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['balance'] = room.Balance
    context['roomId'] = room.Room_Name
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = Amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'confirm.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amt)
                    rm.Balance -= (amt/100)
                    rm.save()
                    # render success page on successful caputre of payment
                    return render(request, 'paymentSuccess.html', {'amount':amt/100, 'balance':rm.Balance, 'room':rm.Room_Name, 'name':nm})
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentFail.html', {'statement':"There is an error while capturing payment"})
            else:
 
                # if signature verification fails.
                return render(request, 'paymentFail.html', {'statement':"Signature verification failed"}) 
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()