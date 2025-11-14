from django.contrib import admin
from django.urls import path,include
from.views import*
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('',home),
    path('index',home),
    path('contact',contact),
    # path('forms',forms),
    path('fetch',fetch),
    path('shop',shop),
    path('update/<int:id>',update),
    path('signup',signup),
    path('about',about),
    path('cart',cart),
    path('services',services),
    path('blog',blog),
    path('login',logins,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('orders', views.orders_view, name='orders'),
    path('product_detail/<int:id>',product_detail),
    path('remove_from_cart/<int:id>',remove_from_cart),
    path('checkouts/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
]

# urlpatterns = [
#     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('product/<int:product_id>/', views.product_detail, name='product_detail'),
#     # other paths...
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)