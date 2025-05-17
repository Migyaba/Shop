from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def index(request):
    products = Product.objects.all()
    search_query = request.GET.get('search')
    if search_query != '' and search_query is not None:
        products = Product.objects.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(products, 8)  # Voir 8 produits par page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'ecom/index.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'ecom/detail.html', {'product': product})

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        # Ici, tu peux gérer le panier via la session
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'message': 'Produit ajouté au panier'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)

@require_GET
def cart_total(request):
    cart = request.session.get('cart', {})
    total = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(pk=pid)
            total += product.price * qty
        except Product.DoesNotExist:
            continue
    return JsonResponse({'total': total})