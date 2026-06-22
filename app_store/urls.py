from django.urls import path
from .views import product_view_json, shop_view, product_page_view
from .views import cart_view_json, cart_add_view_json, cart_del_view_json, cart_view
from .views import coupon_check_view, delivery_estimate_view, cart_buy_now_view, cart_remove_view

app_name = 'app_store'

urlpatterns = [
    path('product/', product_view_json, name='product_json'),
    path('', shop_view, name="shop_view"),
    path('product/<slug:page>.html', product_page_view, name='product_page_view'),
    path('product/<int:page>', product_page_view),
    path('cart/json/', cart_view_json),
    path('cart/add/<id_product>', cart_add_view_json),
    path('cart/del/<id_product>', cart_del_view_json),
    path('cart/', cart_view, name='cart_view'),
    path('coupon/check/<slug:name_coupon>', coupon_check_view, name='coupon_check'),
    path('delivery/estimate', delivery_estimate_view),
    path('cart/buy/<str:id_product>', cart_buy_now_view, name="buy_now"),
    path('cart/remove/<str:id_product>', cart_remove_view, name="remove_now"),
]

