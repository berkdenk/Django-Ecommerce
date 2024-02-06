from django.shortcuts import render
from . models import *
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from . utils import cookieCart,cartData,guestOrder

def store(request):
	data=cartData(request)

	cartItems=data['cartItems']
		

	products=Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	data=cartData(request)

	cartItems=data['cartItems']
	order=data['order']
	items=data['items']

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

#@csrf_exempt
def checkout(request):
	data=cartData(request)

	cartItems=data['cartItems']
	order=data['order']
	items=data['items']
		
	
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

#@csrf_exempt
from django.http import JsonResponse

def updateItem(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data.get('productId', None)
    action = data.get('action', None)

    if productId is None or action is None:
        return JsonResponse({'error': 'Missing productId or action'}, status=400)

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)



def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		

	else:
		customer,order=guestOrder(request,data)
	total=float(data['form']['total'])
	order.transaction_id=transaction_id

	if total==order.get_cart_total:
		order.complete=True
	order.save()

	if order.shipping==True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)
	return JsonResponse('Payment completed!',safe=False)