from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart




def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category") # Считали 'category'
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            reverse = request.GET.get("reverse")
            if reverse and reverse.lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=False)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})



def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data,
                               "category": category_key})




def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    data_other_products = [p for p in DATABASE.values() if p['category'] == data['category']
                                           and p['id'] != data ['id']][:5]
                    return render(request, 'app_store/product.html', context={'product': data,
                                                                              'other_products': data_other_products})

        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                data_other_products = [p for p in DATABASE.values() if p['category'] == data['category']
                                           and p['id'] != data ['id']][:5]
                return render(request, 'app_store/product.html', context={'product': data,
                                                                          'other_products': data_other_products})

        return HttpResponse(status=404)





def cart_view_json(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_view(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username)[username]

        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]
            product["quantity"] = quantity
            product["price_total"] = round(quantity * product["price_after"], 2)
            products.append(product)


        return render(request, "app_store/cart.html", context={"products": products})




def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True},
        "coupon_old": {
            "discount": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if name_coupon in DATA_COUPON:
            coupon = DATA_COUPON[name_coupon]
            return JsonResponse({"discount": coupon["discount"], "is_valid": coupon["is_valid"]})

        return HttpResponseNotFound("Неверный купон")



def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 90},
            "Санкт-Петербург": {"price": 78},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')

        if country in DATA_PRICE:
            if city in DATA_PRICE[country]:
                price = DATA_PRICE[country][city]["price"]
                return JsonResponse({"price": price})

            elif "fix_price" in DATA_PRICE[country]:
                price = DATA_PRICE[country]["fix_price"]
                return JsonResponse({"price": price})


        return HttpResponseNotFound("Неверные данные")

        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе c есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём,
        # {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём,
        # {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")
