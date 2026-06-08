// Переключение сердечка избранного
function toggleWishlistState(event) {
    event.preventDefault();
    let linkWish = event.target;

    if (linkWish.getAttribute('data-action') !== 'toggle') {
        linkWish = linkWish.querySelector('i');
    }

    const productId = linkWish.getAttribute('data-product-id');
    const currentState = linkWish.getAttribute('data-state');

    linkWish.disabled = true;

    if (currentState === 'inactive') {
        // Отправить запрос на добавление в избранное
        fetch('/wishlist/api/add/' + productId, { method: 'GET' })
            .then(function (response) {
                // Проверяем статус ответа
                if (!response.ok) {
                    throw new Error('Ошибка при добавлении в избранное');
                }

                // Проверяем наличие редиректа
                if (response.redirected) {
                    console.log('Произошел редирект на:', response.url);
                    window.location.href = response.url; // Перенаправление на другую страницу
                    return; // Прерываем выполнение функции
                }

                return response.json(); // Продолжаем обработку JSON-данных
            })
            .then(function(data) {
                showPopupMessage(productId, 'Продукт успешно добавлен в избранное');
                linkWish.classList.remove('ion-ios-heart-empty');
                linkWish.classList.add('ion-ios-heart');
                linkWish.setAttribute('data-state', 'active');
            })
            .catch(function (error) {
                // Обрабатываем ошибку
                console.error(error);
            })
            .finally(function () {
                // Включаем ссылку обратно после получения ответа (успешного или с ошибкой)
                linkWish.disabled = false;
            });
    } else {
        // Отправить запрос на удаление из избранного
        fetch('/wishlist/api/del/' + productId, { method: 'GET' })
            .then(function (response) {
                // Проверяем статус ответа
                if (!response.ok) {
                    throw new Error('Ошибка при удалении из избранного');
                }

                // Проверяем наличие редиректа
                if (response.redirected) {
                    console.log('Произошел редирект на:', response.url);
                    window.location.href = response.url; // Перенаправление на другую страницу
                    return; // Прерываем выполнение функции
                }

                return response.json(); // Продолжаем обработку JSON-данных
            })
            .then(function(data) {
                    showPopupMessage(productId, 'Продукт успешно удалён из избранного');
                    linkWish.classList.remove('ion-ios-heart');
                    linkWish.classList.add('ion-ios-heart-empty');
                    linkWish.setAttribute('data-state', 'inactive');
            })
            .catch(function (error) {
                // Обрабатываем ошибку
                console.error(error);
            })
            .finally(function () {
                // Включаем ссылку обратно после получения ответа (успешного или с ошибкой)
                linkWish.disabled = false;
            });
    }
}

const addButtonsHeart = document.querySelectorAll('.heart');
addButtonsHeart.forEach(function (button) {
    button.addEventListener('click', toggleWishlistState);
});

function showHearts(favoriteProducts) {
    // Проходим по всем ссылкам с классом "heart" и изменяем классы:
    let addButtonsHeart1 = document.querySelectorAll('.heart');
    addButtonsHeart1.forEach(function(button) {
        let productId = button.querySelector('i').getAttribute('data-product-id');

        // Если data-product-id товара есть в списке избранных, меняем классы
        if (favoriteProducts.includes(productId)) {
            let icon = button.querySelector('.ion-ios-heart-empty');
            if (icon) {
                icon.classList.remove('ion-ios-heart-empty');
                icon.classList.add('ion-ios-heart');
                icon.setAttribute('data-state', 'active');
            }
        }

    });
}


// Отправляем запрос на получение всех товаров в избранном
fetch('/wishlist/api/', {
        method: 'GET'
    })
    .then(function(response) {
        // Проверяем статус ответа
        if (!response.ok) {
            throw new Error('Ошибка');
        }
        return response.json();
    })
    .then(function(data) {
        // Обрабатываем данные, которые пришли с сервера
        let favoriteProducts = data.products
        showHearts(favoriteProducts);
    })
    .catch(function(error) {
        // Обрабатываем ошибку
        console.error(error);
    });
