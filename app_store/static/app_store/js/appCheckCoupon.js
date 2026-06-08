// Проверка действия купона

let promoElement = document.getElementById('promo-input');
let checkCouponButton = document.getElementById('checkCoupon');
let subtotal_with_discount = 0;
// Функция для проверки действия купона
function checkCoupon() {
    // Получаем значение купона, которое вы хотите проверить
    let couponCode = promoElement.value;

    console.log(couponCode);

    // Делаем кнопку неактивной, чтобы предотвратить повторные запросы
    checkCouponButton.disabled = true;

    // Отправляем асинхронный GET-запрос на сервер для проверки купона
    fetch('/coupon/check/' + couponCode, {
        method: 'GET'
    })
    .then(function(response) {
        // Проверяем статус ответа
        if (!response.ok) {
            throw new Error('Ошибка при проверке купона');
        }
        return response.json();
    })
    .then(function(data) {
        // Обрабатываем данные, которые пришли с сервера
        if (data.is_valid) {
            document.getElementById('couponResult').textContent = 'Купон действителен! Размер скидки: ' + data.discount + '%';
            subtotal_with_discount = parseFloat(subtotalElement.textContent) * 0.01 * data.discount;
            discountElement.textContent = subtotal_with_discount.toFixed(2);
        } else {
            document.getElementById('couponResult').textContent = 'Купон не действителен!';
            discountElement.textContent = 0.00.toFixed(2);
        }
    })
    .catch(function(error) {
        // Обрабатываем ошибку
        console.error(error);
        document.getElementById('couponResult').textContent = 'Произошла ошибка при проверке купона';
        discountElement.textContent = 0.00.toFixed(2);
    })
    .finally(function() {
        // Включаем кнопку обратно после получения ответа (успешного или с ошибкой)
        updateTotal();
        checkCouponButton.disabled = false;
    });
};

checkCouponButton.addEventListener('click', checkCoupon);