from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import JsonResponse
import json
# Create your views here.




def store(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		product=Product.objects.all()
		order, created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		context={'product':product,'order':order,'items':items}
	else:
		product=Product.objects.all()
		context={'product':product,'order':None,'items':None}


	return render(request,'store.html',context)




def cart(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		context={'order':order,'items':items}
	else:
		context={'order':None,'items':None}
	return render(request, 'cart.html',context)



def checkout(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		context={'order':order,'items':items}
	else:
		context={'order':None,'items':None}
	return render(request, 'checkout.html',context)


def register(request):
	form=UserCreationForm()
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():

			user=form.save()
			Customer.objects.create(user=user,name='vide',email='vide@vv')
			return redirect('login')


	return render(request,'registration/register.html',{'form':form})



def update_item(request):


	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = orderItem.quantity + 1
	elif action == 'down':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity  <= 0:
		orderItem.delete()
	elif action=='remove':
		orderItem.delete()


	return JsonResponse('Item was added', safe=False)