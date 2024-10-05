from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

path('', views.home, name='home'),
path('shop/', views.Product_list, name='product_list'),
path('shop/?search=<search_term>', views.Product_list, name='product_search'),
path('shop/?offer=<offer>', views.Product_list, name='product_offer'),
#path('<int:id>/', views.shop_detail, name='shop_detail'),
#path('<int:year>/<int:month>/<int:day>/<slug:ptype>/<slug:brand>/<slug:product>/', views.product_detail, name='product_detail'),
path('<slug:product_slug>/', views.product_detail, name='product_detail'),]
