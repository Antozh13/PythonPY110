// Функция для показа всплывающего сообщения
function showPopupMessage(productID, message) {
    let popupMessage = document.querySelector(`.custom-popup-message[data-product-id="${productID}"]`);
    popupMessage.textContent = message;
    popupMessage.style.display = 'block';
    setTimeout(function() {
        popupMessage.style.opacity = 1;
    }, 10);
    setTimeout(function() {
        popupMessage.style.opacity = 0;
        setTimeout(function() {
            popupMessage.style.display = 'none';
        }, 250); // Исчезнет через 0.25 секунды
    }, 750); // Показывается в течение 0.75 секунд
}


// Добавление продукта в корзину
function addToCart(event) {
    // Получаем значение купона, которое вы хотите проверить
    event.preventDefault();
    let linkCart = event.target; // Получаем элемент ссылки, на которой был клик
    // console.log(linkCart)
    let productId = linkCart.getAttribute('data-product-id'); // Получаем ID товара
    console.log(productId)
    linkCart.disabled = true;

    // Отправляем асинхронный GET-запрос на сервер для проверки купона
    fetch('/cart/add/' + productId, {
        method: 'GET'
    })
    .then(function(response) {
        // Проверяем статус ответа
        if (!response.ok) {
            throw new Error('Ошибка при добавлении в корзину');
        }

        // Проверяем наличие редиректа
        if (response.redirected) {
            console.log('Произошел редирект на:', response.url);
            window.location.href = response.url; // Пример перенаправления на другую страницу
            return; // Прерываем выполнение функции
        }

        return response.json(); // Продолжаем обработку JSON-данных
    })
    .then(function(data) {
        // Обрабатываем данные, которые пришли с сервера
        if (data.answer === 'Продукт успешно добавлен в корзину') {
            showPopupMessage(productId, 'Продукт успешно добавлен в корзину');
        }
    })
    .catch(function(error) {
        // Обрабатываем ошибку
        console.error(error);
    })
    .finally(function() {
        // Включаем ссылку обратно после получения ответа (успешного или с ошибкой)
        linkCart.disabled = false;
    });
};
let addButtons = document.querySelectorAll('.add-to-cart');
addButtons.forEach(function(button) {
    button.addEventListener('click', addToCart);
});