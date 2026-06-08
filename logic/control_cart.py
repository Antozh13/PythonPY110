import json
import os
from app_store.models import DATABASE

PATH_CART = 'cart.json'  # Путь до файла корзины


def view_in_cart(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое корзины cart.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'cart.json'
    """
    empty_user_cart = {'products': {}}  # Пустая корзина для пользователя

    if os.path.exists(PATH_CART):  # Если файл с корзиной существует
        with open(PATH_CART, encoding='utf-8') as f:  # Открываем файл
            cart = json.load(f)  # Считываем корзину
            if username not in cart:  # Если пользователя нет в корзине, то создаем запись с пустой корзиной для него
                cart[username] = empty_user_cart
    else:  # Если файла с корзиной нет
        cart = {username: empty_user_cart}

    # Запись словаря cart в cart.json
    with open(PATH_CART, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем корзину
        json.dump(cart, f)

    return cart  # Возвращаем содержимое корзины


def add_to_cart(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart = view_in_cart(username)

    if id_product not in DATABASE:
        return False

    user_cart = cart[username] ["products"]

    if id_product in user_cart:
        user_cart[id_product] += 1

    else:
        user_cart[id_product] = 1

    with open(PATH_CART, mode='w', encoding='utf-8') as f:
        json.dump(cart, f)


    return True


def remove_from_cart(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart = view_in_cart(username)

    user_cart = cart[username] ["products"]

    if id_product not in user_cart:
        return False

    del user_cart[id_product]

    with open(PATH_CART, mode='w', encoding='utf-8') as f:
        json.dump(cart, f)

    return True


if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину

    print('Проверяем корзину', "Ответ:     {'': {'products': {}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 0', 'Ответ:     False', f'Результат: {add_to_cart("0")}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 2', 'Ответ:     True', f'Результат: {add_to_cart("2")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'1': 2, '2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Удаляем товар с id = 0', "Ответ:     False", f'Результат: {remove_from_cart("0")}\n', sep='\n')
    print('Удаляем товар с id = 1', "Ответ:     True", f'Результат: {remove_from_cart("1")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')

    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину
