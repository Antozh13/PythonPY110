// Получаем элементы с значениями
let subtotalElement = document.getElementById('subtotal-value');
let deliveryElement = document.getElementById('delivery-value');
let discountElement = document.getElementById('discount-value');
let totalElement = document.getElementById('total-value');

// Функция для обновления итога
function updateTotal() {
    // Получаем значения промежуточного итога, доставки и скидок из элементов
    let subtotal = parseFloat(subtotalElement.textContent);
    let delivery = parseFloat(deliveryElement.textContent);
    let discount = parseFloat(discountElement.textContent);

    // Вычисляем итог
    let total = subtotal + delivery - discount;

    // Убеждаемся, что итог не становится отрицательным
    if (total < 0) {
        total = 0;
    }

    // Обновляем элемент с итогом
    totalElement.textContent = total.toFixed(2);
}

// Вызываем функцию для первичного расчета итога
updateTotal();