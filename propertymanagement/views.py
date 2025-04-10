import requests
import uuid,json,urllib.parse,hmac,hashlib,base64 
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm,RegisterForm,KYCForm,PropertyForm
from django.contrib.auth import login,logout,authenticate
from .models import Property
from django.http import JsonResponse
from django.contrib import messages


def home(request):
    return render(request,'home.html')

def my_view(request):
    return render(request, 'dashboard.html', {'br_range': range(8)})


def user_login(request):
    form = LoginForm()
    errors = None  

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('adminDashboard')
                else:
                    return redirect('dashboard')
            else:
                errors = 'Invalid credentials'  
                
    return render(request, 'login.html', {'form': form, 'errors': errors})  



def dashboard(request):

    return render(request,'dashboard.html')

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        kyc_form = KYCForm(request.POST,request.FILES)
        if user_form.is_valid() and kyc_form.is_valid():
            user = user_form.save()
            kyc = kyc_form.save(commit=False)
            kyc.user = user
            kyc.save()
            return redirect('login')
        

    else:
        user_form = RegisterForm()
        kyc_form = KYCForm()
    return render(request,'register.html',{'user_form':user_form,'kyc_form':kyc_form}) 

def dashboard(request):
    mem = Property.objects.filter(posted_by=request.user)
    return render(request,'dashboard.html',{'mem':mem})

def user_logout(request):
    logout(request)
    return render(request,'home.html')

def register_property(request):
    form = PropertyForm()

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.posted_by = request.user
            property.save()
            return redirect('dashboard')

    return render(request, 'registerproperty.html', {'form': form})


def payment(request, id):
    mem = get_object_or_404(Property, id=id)

    mem.transaction_uuid = str(uuid.uuid4())
    mem.save()  

    total_amount = str(mem.stamp_duty)
    product_code = "EPAYTEST"
    secret_key = settings.PAYMENT_SECRET_KEY

    message = f"total_amount={total_amount},transaction_uuid={mem.transaction_uuid},product_code={product_code}".encode('utf-8')
    secret = secret_key.encode('utf-8')

    hmac_sha256 = hmac.new(secret, message, hashlib.sha256)
    digest = hmac_sha256.digest()
    signature = base64.b64encode(digest).decode('utf-8')



    return render(request, 'payment.html', {
        'mem': mem,
        'signature': signature,
        'transaction_uuid': mem.transaction_uuid
    })


def check_payment_status(transaction_uuid, product_code, total_amount):
    url = "https://rc.esewa.com.np/api/epay/transaction/status/"
    params = {
        "product_code": product_code,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return None



def payment_success(request):
        encoded_data = request.GET.get('data')

        if encoded_data:
            try:
                decoded_data = base64.b64decode(encoded_data).decode('utf-8')
                
                data = json.loads(decoded_data)
                
                transaction_uuid = data.get('transaction_uuid')
                total_amount = data.get('total_amount')
                product_code = data.get('product_code')
                
                if transaction_uuid and total_amount and product_code:
                    payment_status = check_payment_status(transaction_uuid, product_code, total_amount)
                    
                    if payment_status and payment_status.get('status') == 'COMPLETE':
                        mem = Property.objects.filter(posted_by=request.user, transaction_uuid=transaction_uuid).first()
                        if mem:
                            mem.is_paid = True
                            mem.save()  
                            return redirect('dashboard')  
                        else:
                            return HttpResponse("Property not found for this transaction.")
                    else:
                        return HttpResponse("Payment failed or invalid transaction.")
                else:
                    return HttpResponse("Required transaction information is missing.")
            
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                return HttpResponse("Error processing the transaction data.")
        else:
            return HttpResponse("No data parameter provided.")
        


def adminDashboard(request):
    mem = Property.objects.filter(is_paid=True).order_by('-id')
    return render(request,'adminDashboard.html',{'mem':mem})


def accept(request,id):
    mem = Property.objects.get(id=id)
    mem.status = 'Approved'
    mem.save()
    return redirect('adminDashboard')


def reject(request,id):
    mem = Property.objects.get(id=id)
    mem.status = 'Rejected'
    mem.save()
    return redirect('adminDashboard')


def generate_certificate(request, id):
    mem = Property.objects.get(id=id)
    return render(request,'certificate.html',{'mem':mem})