// Получаем все элементы с классами "quantity" и "total"
let quantityInputs = document.querySelectorAll('.quantity input');
let totalElements = document.querySelectorAll('.total');
let priceElements = document.querySelectorAll('.price');
// Функция для обновления промежуточного итога
function updateSubtotal() {
    // Инициализируем переменные для промежуточного итога и цены товара
    let subtotal = 0;

    // Проходимся по всем элементам с классом "quantity"
    quantityInputs.forEach(function(input, index) {
        // Получаем значение количества товара
        let quantity = parseInt(input.value, 10);

        // Получаем цену товара из HTML (хотя обычно идёт запрос на сервер)
        let price = parseFloat(priceElements[index].textContent);

        // Рассчитываем общую цену для данной позиции
        let itemTotal = quantity * price;

        // Обновляем элемент с классом "total" для данной позиции
        totalElements[index].textContent = itemTotal.toFixed(2);

        // Добавляем общую цену данной позиции к общему промежуточному итогу
        subtotal += itemTotal;
    });

    // Обновляем элемент с итогом
    document.getElementById('subtotal-value').textContent = subtotal.toFixed(2); // Форматируем итог в нужный вид

    updateTotal(); // Вызываем пересчёт корзины
    // document.querySelector('.total-price span:last-child').textContent = '₽ ' + subtotal.toFixed(2); // Форматируем итог в нужный вид
}

// Слушаем событие изменения ввода количества товара
quantityInputs.forEach(function(input) {
    input.addEventListener('change', updateSubtotal);
});

// Вызываем функцию для первичного расчета итога
updateSubtotal();