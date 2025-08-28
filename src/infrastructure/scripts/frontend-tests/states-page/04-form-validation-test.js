// ========================================
// ТЕСТ ВАЛИДАЦИИ ФОРМЫ
// ========================================
// Назначение: Тестирование валидации полей формы создания/редактирования
// Использование: Выполнить в консоли браузера на странице /states
// Автор: AI Assistant
// Дата: 25 августа 2025

console.log('🔍 Тест валидации формы');

// ========================================
// ТЕСТ 1: Валидация обязательных полей
// ========================================
function testRequiredFieldsValidation() {
  console.log('\n📋 ТЕСТ 1: Валидация обязательных полей');
  
  const addButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Добавить государство')
  );
  
  if (addButton) {
    addButton.click();
    
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        console.log('✅ Диалог создания открылся');
        
        // Очищаем обязательные поля
        const nameInput = dialog.querySelector('input[type="text"]');
        const dateInput = dialog.querySelector('input[type="date"]');
        
        if (nameInput && dateInput) {
          // Очищаем поля
          nameInput.value = '';
          dateInput.value = '';
          
          // Триггерим события
          nameInput.dispatchEvent(new Event('input'));
          dateInput.dispatchEvent(new Event('input'));
          
          console.log('📝 Поля очищены');
          console.log('💡 Теперь попробуйте нажать "Создать" - должны появиться уведомления об ошибках');
          
          // Находим кнопку создания
          const createButton = dialog.querySelector('button[label="Создать"]');
          if (createButton) {
            console.log('🔘 Кнопка "Создать" найдена');
            console.log('📋 Нажмите на неё для проверки валидации');
          }
        }
      }
    }, 500);
  }
}

// ========================================
// ТЕСТ 2: Проверка заполнения формы
// ========================================
function testFormFilling() {
  console.log('\n📝 ТЕСТ 2: Проверка заполнения формы');
  
  const addButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Добавить государство')
  );
  
  if (addButton) {
    addButton.click();
    
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        console.log('✅ Диалог создания открылся');
        
        // Заполняем форму корректными данными
        const nameInput = dialog.querySelector('input[type="text"]');
        const typeSelect = dialog.querySelector('select');
        const dateInput = dialog.querySelector('input[type="date"]');
        const periodSelect = dialog.querySelector('select:last-child');
        
        if (nameInput && typeSelect && dateInput && periodSelect) {
          // Заполняем поля
          nameInput.value = 'Тестовое государство (валидация)';
          typeSelect.value = 'EMPIRE';
          dateInput.value = '2024-01-01';
          periodSelect.value = '5'; // Новейшее время
          
          // Триггерим события
          nameInput.dispatchEvent(new Event('input'));
          typeSelect.dispatchEvent(new Event('change'));
          dateInput.dispatchEvent(new Event('input'));
          periodSelect.dispatchEvent(new Event('change'));
          
          console.log('📝 Форма заполнена корректными данными:');
          console.log('  Название:', nameInput.value);
          console.log('  Тип:', typeSelect.value);
          console.log('  Дата основания:', dateInput.value);
          console.log('  Исторический период:', periodSelect.value);
          
          console.log('✅ Форма готова к созданию записи');
        }
      }
    }, 500);
  }
}

// ========================================
// ТЕСТ 3: Проверка исторического периода
// ========================================
function testHistoricalPeriodField() {
  console.log('\n📅 ТЕСТ 3: Проверка поля исторического периода');
  
  const addButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Добавить государство')
  );
  
  if (addButton) {
    addButton.click();
    
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        console.log('✅ Диалог создания открылся');
        
        // Проверяем поле исторического периода
        const periodSelect = dialog.querySelector('select:last-child');
        if (periodSelect) {
          console.log('✅ Поле исторического периода найдено');
          console.log('📋 Доступные опции:');
          
          Array.from(periodSelect.options).forEach((option, index) => {
            console.log(`  ${index + 1}. ${option.text} (${option.value})`);
          });
          
          // Проверяем значение по умолчанию
          console.log('📝 Значение по умолчанию:', periodSelect.value);
          
        } else {
          console.log('❌ Поле исторического периода не найдено');
        }
        
        // Закрываем диалог
        const cancelButton = dialog.querySelector('button[label="Отмена"]');
        if (cancelButton) {
          cancelButton.click();
          console.log('🔘 Диалог закрыт');
        }
      }
    }, 500);
  }
}

// ========================================
// ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
// ========================================
function runValidationTests() {
  console.log('🚀 ЗАПУСК ТЕСТОВ ВАЛИДАЦИИ ФОРМЫ');
  console.log('='.repeat(50));
  
  console.log('💡 Выберите тест для запуска:');
  console.log('1. testRequiredFieldsValidation() - проверка обязательных полей');
  console.log('2. testFormFilling() - проверка заполнения формы');
  console.log('3. testHistoricalPeriodField() - проверка поля исторического периода');
  
  console.log('\n📋 Для запуска конкретного теста введите его название в консоли');
}

// Запуск тестов
runValidationTests();