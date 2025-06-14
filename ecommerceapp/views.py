from django.shortcuts import render, redirect
from ecommerceapp.models import Contact, Product, OrderUpdate, Orders
from django.contrib import messages
from math import ceil
from ecommerceapp import keys
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache

MERCHANT_KEY = keys.MK
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum







# In your app's views.py file

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Orders

def place_order(request):
    if request.method == 'POST':
        # Assuming you have form data containing the product ID and quantity ordered
        product_id = request.POST.get('product_id')
        quantity_ordered = int(request.POST.get('quantity'))

        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)

        # Check if there's enough quantity available
        if product.remaining_quantity >= quantity_ordered:
            # Update the remaining quantity of the product
            product.remaining_quantity -= quantity_ordered
            product.save()

            # Create the order
            order = Orders.objects.create(
                # Populate other order fields as needed
            )

            return HttpResponse("Order placed successfully!")
        else:
            return HttpResponse("Insufficient quantity available!")

    else:
        return HttpResponse("Invalid request method")

# Create your views here.
# def index(request):
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     print(catprods)
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         prod = Product.objects.filter(category=cat)
#         n = len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])

#     params = {'allProds': allProds}
#     return render(request, "index.html", params)


from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Orders

def place_order(request):
    if request.method == 'POST':
        # Assuming you have form data containing the product ID and quantity ordered
        product_id = request.POST.get('product_id')
        quantity_ordered = int(request.POST.get('quantity'))

        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)

        # Check if there's enough quantity available
        if product.remaining_quantity >= quantity_ordered:
            # Update the remaining quantity of the product
            product.remaining_quantity -= quantity_ordered
            product.save()

            # Create the order
            order = Orders.objects.create(
                # Populate other order fields as needed
            )

            return HttpResponse("Order placed successfully!")
        else:
            return HttpResponse("Insufficient quantity available!")

    else:
        return HttpResponse("Invalid request method")



# views.py
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

        # Fetch remaining quantity for each product
        for p in prod:
            remaining_quantity = p.remaining_quantity  # Assuming 'remaining_quantity' is a field in your Product model
            p.remaining_quantity = remaining_quantity

        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "index.html", params)





def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "we will get back to you soon..")
        return render(request, "contact.html")
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    # Check if the cart is empty
    cart_items = json.loads(request.COOKIES.get('cart', '{}'))
    if not cart_items:
        messages.error(request, "No items in the cart. Please add items before proceeding to checkout.")
        return redirect('index')  # Redirect to the homepage or any other appropriate page



    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1, address2=address2,
                       city=city, state=state, zip_code=zip_code, phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id, update_desc="the order has been placed")
        update.save()
        thank = True
       
       
       # Check if the cart is still empty after form submission (edge case)
        if not items_json:
            messages.error(request, "No items in the cart. Please add items before proceeding to checkout.")
            return redirect('index')

        # Save order
        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1, address2=address2,
                       city=city, state=state, zip_code=zip_code, phone=phone)
        Order.save()

        # Update order status
        update = OrderUpdate(order_id=Order.order_id, update_desc="The order has been placed")
        update.save()
       
        # PAYMENT INTEGRATION
        id = Order.order_id
        oid = str(id) + "ShopyCart"
        param_dict = {
            'MID': keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        # paytm will send you post request here
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]

        # Always treat payment as successful
        if 'ORDERID' in response_dict:
            a = response_dict['ORDERID']
            b = response_dict['TXNAMOUNT']
            rid = a.replace("ShopyCart", "")
            filter2 = Orders.objects.filter(order_id=rid)
            for post1 in filter2:
                post1.oid = a
                post1.amountpaid = b
                post1.paymentstatus = "PAID"
                post1.save()
            return JsonResponse({"success": "Order status updated successfully"})

    return JsonResponse({"error": "Invalid request method."}, status=405)



def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    rid = ""
    for i in items:
        print(i.oid)
        # print(i.order_id)
        myid = i.oid
        rid = myid.replace("ShopyCart", "")
        print(rid)
    status = OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)
    context = {"items": items, "status": status}
    # print(currentuser)
    return render(request, "profile.html", context)
