from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,ProfileForm


from django.views.decorators.csrf import csrf_exempt
import razorpay

# for logout and login
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.http import HttpResponse,JsonResponse
from django.views import View

from django.db.models import Q #import for getting multiple condition



from . import models

# Create your views here.
@csrf_exempt
def home(request):
    return render(request,'dashboard/home.html')


def register(request):
    
    form = CreateUserForm()
    
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            
            
            return redirect('login')

    context = {'form':form}
    return render(request, 'dashboard/register.html',context=context)


#login  function
def login(request):
    form = LoginForm()
    
    if request.method == "POST":
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username = username , password = password)
            
            if user is not None:
                auth.login(request,user)
                return redirect('home')
                
                
                
          
    context = {'form':form}
    return render (request, 'dashboard/login.html',context=context)
        
    
#logout
def logout(request):
    
    auth.logout(request)
    return redirect("login")
    
#product cetagory
def producut_cetagory(request,val):
   
    obj = models.Product.objects.filter(cetagory=val)
    
    return render(request,'dashboard/cetagory.html',{'obj':obj})


#product details

def productdetails(request,id):
    data = models.Product.objects.get(id=id)
    return render(request,'dashboard/productdetails.html',{'data':data})

#fetch all products
def get_product(request):
    
    data = models.Product.objects.all()
    
    return render(request,'dashboard/product.html',{'data':data})



#add profile address

def AddProfile(request):
    form = ProfileForm()
    if request.method == 'POST':
        
        form = ProfileForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('showProfile')
    
    return render(request,'dashboard/profile.html',{'form':form})


#show profile

def showProfile(request):
    user = request.user
    record = models.Customer.objects.filter(user=user)
    print(record[0].pk,'******************************************************')
    return render(request,'dashboard/showProfile.html',{'record':record})


#update profile


def updateRecord(request,id):
    obj = models.Customer.objects.get(id=id)
    form = ProfileForm(instance=obj)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=obj)
        
        if form.is_valid():
            form.save()
            return redirect('showProfile')
    return render(request,'dashboard/updateprofile.html',{'form':form})


#delete address

def deleteRecord(request,id):
    obj= models.Customer.objects.get(id=id)
    obj.delete()
    return redirect('showProfile')


#Add to cart section
def add_to_cart(request,id):
    user = request.user
    product = models.Product.objects.get(id=id)
    c = models.cart(user=user,product=product)
    c.save()
    return redirect('cart')
    
    
def show_cart(request):
    user = request.user
    cart = models.cart.objects.filter(user=user)
    total = 0
    for x in cart:
        total += (x.quantity * x.product.discounted_price)
    tamount = total + 60
    
    if models.cart.objects.count() > 0:
        return render(request,'dashboard/addcart.html',{'cart':cart,'total':total,'tamount':tamount})
    else:
        return render(request,'dashboard/addcart.html')

#Delete Cart Item 

def deleteItem(request,id):
    # here Q is used for getting multiple condition at a time 
    p = models.cart.objects.get(Q(product = id),Q(user=request.user))
    p.delete()
    return redirect('cart')

# Buynow Button

def buyNow(request):
        user = request.user
        cart = models.cart.objects.filter(user=user)
        print(cart)
        total =0
        for x in cart:
            total += (x.quantity * x.product.discounted_price)
        tamount = total + 60
        obj = models.Customer.objects.filter(user=user)
        razoramount = int(tamount * 100)
        client = razorpay.Client(auth=("rzp_test_GtGb9Vr2OnmrNY","QkKg4lSvHt3YgWEmNh4OAD6N"))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment_response = client.order.create(data=data)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = models.Payment(
                user = user,
                amount = tamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        
        return render(request,'dashboard/buynow.html',{'totalamount':tamount,'address':obj,'payment':payment_response,'cart':cart})
#this is for payment button

@csrf_exempt
def payment_done(request):
    if request.method =='POST':
        # order_id = request.GET.get('order_id')
        # payment_id = request.GET.get('payment_id')
        
        # cust_id = request.GET.get('cust_id')
        # order_id = models.Payment.objects.get(id =  cust_id)
        
        
        
      
        # payment  = models.Payment.objects.get(razorpay_order_id = order_id)
        # payment.paid= True
        # # payment.razorpay_payment_id = payment_id
        # payment.save()
        
        
        customer = models.Customer.objects.get(id = 17)
        user = request.user 
        print(user,"88888888888888888888888888888-------------------------------8888888888888")
        cart= models.cart.objects.filter(user = user)
        print(cart,'----------------------------')
        for c in cart:
            models.orderPlaced(user = user , customer = customer,product = c.product,quantity = c.quantity).save()
            c.delete()
        return redirect('home')





#plus cart function
def plusCart(request):
    
    if request.method == "GET":
        p_id = request.GET['product_id']
        print(p_id)
        p = models.cart.objects.get(Q(product = p_id),Q(user=request.user))
        p.quantity+=1
        p.save()
        user = request.user
        cart = models.cart.objects.filter(user=user)
        total =0
        for x in cart:
            total += (x.quantity * x.product.discounted_price)
        tamount = total + 60
        
        data={
            'quantity':p.quantity,
            'amount':total,
            'totalamount':tamount
        }
        
        return JsonResponse(data)
    
# minus cart
def minusCart(request):
    
    if request.method == "GET":
        p_id = request.GET['product_id']
        
        p = models.cart.objects.get(Q(product = p_id),Q(user=request.user))
        p.quantity -= 1
        p.save()
        
        data={
            'quantity':p.quantity,
            
        }
        
        return JsonResponse(data)
    
    

#for serach item 

def search(request):
    if request.method == 'POST':
        query =  request.POST['search']
    
        mydata = models.Product.objects.filter(cetagory__icontains=query).values()
        c = len(models.Product.objects.filter(cetagory__icontains=query).values())
        
        return render(request,'dashboard/search.html',{'product':mydata,'count':c})
    
    else:
        return redirect('product')

    
def about(request):
    return render(request,'dashboard/about.html')


def contact(request):
    if request.method == 'POST':
      
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        models.contact.objects.create(name = name , email = email,message= message)
        return redirect('success')
    return render(request,'dashboard/contact.html')

def contact_success(request):
    return render(request,'dashboard/success.html')


@csrf_exempt
def order_success(request):
    
    return render(request,'dashboard/ordersuccess.html')