from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product, Ptype, Brand, Categories
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
from django.db.models import Q

# class productListView(ListView, search=None):
#     """
#     Alternative product list view
#     """
#     if 'search' in request.GET:
#     queryset = Product.objects.all()
#     context_object_name = 'product'
#     paginate_by = 9
#     template_name = 'shop/product/list.html'

def Product_list(request, search=None,offer=None):
    if "search" in request.GET:    
        Search=request.GET.get("search")
        Product_list = Product.objects.filter(  # Filter products based on search query
        Q(name__icontains=Search) |  # Search in product name
        Q(ptype__name__contains=Search) |  # Search in product type
        Q(brand__name__contains=Search) |  # Search in product brand
        Q(description__contains=Search) |
        Q(ptype__categories__name__contains=Search)  # Search in product description
    ).order_by('name')  # Order results alphabetically by name (optional)
    elif 'offer' in request.GET:
        Offer=request.GET.get('offer')
        min, max = map(int, Offer.split('-'))
        Product_list = Product.objects.filter(offer__gte=min , offer__lte=max)
    else: 
        Product_list = Product.objects.all()

    # Pagination with 3 posts per page
    paginator = Paginator(Product_list, 9)
    page_number = request.GET.get('page')
    try:
         product = paginator.page(page_number)
    except PageNotAnInteger:
    # If page_number is not an integer deliver the first page
        product = paginator.page(1)
    except EmptyPage:
    # If page_number is out of range deliver last page of results
        product = paginator.page(paginator.num_pages)
    categories = Categories.objects.all().prefetch_related('subcategory')
    ptype = Ptype.objects.all()
    
    return render(request,'shop/product/list.html',{'product': product , "type": ptype , "categories":categories})

def home(request):
    categories = Categories.objects.all().prefetch_related('subcategory')
    product = Product.objects.all().prefetch_related('ptype', 'brand')
    ptype = Ptype.objects.all()
    brand = Brand.objects.all()
    page = {'name': 'home'}

    return render(request,'shop/product/home.html',{'product': product , "type": ptype , "brand": brand, "categories":categories, "page":page})

def product_detail(request, product_slug):#, brand_slug, ptype_slug ):
    product = get_object_or_404(Product,
                                slug=product_slug)
                                #ptype__slug=ptype_slug ,
                                #brand__slug=brand_slug)
  
    return render(request,'shop/product/detail.html',{'product': product})

