from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from store.models import Wishlist,Product

@login_required(login_url="loginpage")
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context= {'wishlist':wishlist}
    return render(request,'store/wishlist.html', context)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Producto ya está en la lista de deseados"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Producto agregado a la lista de deseados"})
            else: 
                return JsonResponse({'status':"Producto no encontrado"})
        else:
            return JsonResponse({'status':"Inicia sesión para continuar"})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status':"Producto eliminado"})
            else:
                Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status':"El producto no se encuentra en la lista de deseados"})
        else:
            return JsonResponse({'status':"Inicia sesión para continuar"})
    return redirect('/')