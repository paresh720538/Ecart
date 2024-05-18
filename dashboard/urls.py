from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('success',views.contact_success,name='success'),
    path('suc-order',views.order_success,name='suc-order'),
    path('register',views.register, name="register"),
    path('login',views.login,name="login"),
    path("logout",views.logout,name="logout"),
    
    path('cetagory/<slug:val>',views.producut_cetagory,name='cetagory'),
    path('cetagory',views.producut_cetagory,name='cetagory'),
    path('product-details/<int:id>',views.productdetails,name='details'),
    
    path('profile',views.AddProfile,name='profile'),
    path('product',views.get_product,name='product'),
    path('showProfile',views.showProfile,name='showProfile'),
    path('updaterecord/<int:id>',views.updateRecord,name='updaterecord'),
    path('deleterecord/<int:id>',views.deleteRecord,name='deleterecord'),
    
    path('search',views.search,name='search'),
    
    path('pluscart',views.plusCart,name='pluscart'),
    path('minuscart',views.minusCart,name='minuscart'),
    
    path('add-to-cart/<int:id>',views.add_to_cart,name='add-to-cart'),
    path('del-cart-item/<int:id>',views.deleteItem,name='del-cart-item'),
    path('cart',views.show_cart,name='cart'),
    path('checkout',views.buyNow,name='checkout'),
    path('paymentdone',views.payment_done,name='paymentdone'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)