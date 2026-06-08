from django.urls import path
from .views import product_view_json, shop_view, product_page_view
from .views import cart_view_json, cart_add_view_json, cart_del_view_json, cart_view

app_name = 'app_store'

urlpatterns = [
    path('product/', product_view_json),
    path('', shop_view),
    path('product/<slug:page>.html', product_page_view, name='product_page_view'),
    path('product/<int:page>', product_page_view),
    path('cart/json/', cart_view_json),
    path('cart/add/<id_product>', cart_add_view_json),
    path('cart/del/<id_product>', cart_del_view_json),
    path('cart/', cart_view)
]

