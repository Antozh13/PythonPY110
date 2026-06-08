// Расчёт стоимости доставки

let deliveryCountry = document.getElementById('delivery-country');
let deliveryCity = document.getElementById('delivery-city');
let deliveryCode = document.getElementById('delivery-post-code');
let estimateButton = document.getElementById('estimateDelivery');
// let deliveryElement = document.getElementById('delivery-value');
// Функция для расчёта стоимости доставки
function estimateDelivery() {
    // Получаем значение купона, которое вы хотите проверить
    let country = deliveryCountry.value;
    let city = deliveryCity.value;
    let code = deliveryCode.value;

    console.log(country, city, code);

    // Делаем кнопку неактивной, чтобы предотвратить повторные запросы
    estimateButton.disabled = true;

    // Отправляем асинхронный GET-запрос на сервер для расчёта стоимости доставки
    fetch('/delivery/estimate?country=' + country + '&city=' + city + '&code=' + code, {
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
        deliveryElement.textContent = data.price.toFixed(2);
        document.getElementById('estimateResult').textContent = 'Доставка рассчитана и внесена в стоимость заказа';
    })
    .catch(function(error) {
        // Обрабатываем ошибку
        console.error(error);
        document.getElementById('estimateResult').textContent = 'Сюда, к сожалению, не доставляем';
        deliveryElement.textContent = 0.00.toFixed(2);
    })
    .finally(function() {
        // Включаем кнопку обратно после получения ответа (успешного или с ошибкой)
        updateTotal();
        estimateButton.disabled = false;
    });
};

estimateButton.addEventListener('click', estimateDelivery);