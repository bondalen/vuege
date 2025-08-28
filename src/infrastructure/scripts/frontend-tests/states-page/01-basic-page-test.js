// ========================================
// БАЗОВЫЙ ТЕСТ СТРАНИЦЫ "ГОСУДАРСТВА"
// ========================================
// Назначение: Проверка загрузки страницы и основных элементов
// Использование: Выполнить в консоли браузера на странице /states
// Автор: AI Assistant
// Дата: 25 августа 2025

console.log('🔧 Запуск базового теста страницы "Государства"');

// ========================================
// ТЕСТ 1: Проверка загрузки страницы
// ========================================
function testPageLoad() {
  console.log('\n📋 ТЕСТ 1: Проверка загрузки страницы');
  
  // Проверка заголовка
  const title = document.querySelector('h4.text-h4');
  if (title && title.textContent.includes('Государства')) {
    console.log('✅ Заголовок страницы корректный');
  } else {
    console.log('❌ Заголовок страницы не найден или некорректен');
  }
  
  // Проверка кнопки добавления
  const addButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Добавить государство')
  );
  
  if (addButton) {
    console.log('✅ Кнопка "Добавить государство" найдена');
    console.log('🔍 Текст кнопки:', addButton.textContent.trim());
  } else {
    console.log('❌ Кнопка "Добавить государство" не найдена');
    console.log('🔍 Доступные кнопки:', Array.from(document.querySelectorAll('button')).map(b => b.textContent.trim()));
  }
  
  // Проверка таблицы
  const table = document.querySelector('table');
  if (table) {
    console.log('✅ Таблица найдена');
  } else {
    console.log('❌ Таблица не найдена');
  }
}

// ========================================
// ТЕСТ 2: Проверка данных в таблице
// ========================================
function testTableData() {
  console.log('\n📊 ТЕСТ 2: Проверка данных в таблице');
  
  const rows = document.querySelectorAll('tbody tr');
  console.log(`📈 Найдено записей в таблице: ${rows.length}`);
  
  if (rows.length > 0) {
    // Проверка первой записи
    const firstRow = rows[0];
    const cells = firstRow.querySelectorAll('td');
    
    if (cells.length >= 5) {
      console.log('✅ Структура таблицы корректная (5+ колонок)');
      console.log(`📝 Первая запись: ${cells[0].textContent.trim()}`);
      
      // Выводим все данные первой строки
      console.log('📋 Данные первой строки:');
      cells.forEach((cell, index) => {
        console.log(`  Колонка ${index + 1}: ${cell.textContent.trim()}`);
      });
    } else {
      console.log('❌ Неправильная структура таблицы');
    }
    
    // Проверка кнопок действий
    const actionButtons = firstRow.querySelectorAll('button, .q-btn');
    console.log(`🔧 Кнопок действий в строке: ${actionButtons.length}`);
    
    if (actionButtons.length >= 3) {
      console.log('✅ Кнопки действий присутствуют');
      
      // Анализ кнопок
      actionButtons.forEach((button, index) => {
        const icon = button.querySelector('i, .q-icon');
        const ariaLabel = button.getAttribute('aria-label');
        const title = button.getAttribute('title');
        
        console.log(`  Кнопка ${index + 1}:`, {
          icon: icon ? icon.className : 'нет иконки',
          ariaLabel: ariaLabel || 'нет aria-label',
          title: title || 'нет title',
          text: button.textContent.trim()
        });
      });
    } else {
      console.log('❌ Недостаточно кнопок действий');
    }
  } else {
    console.log('⚠️ Таблица пуста или данные не загружены');
  }
}

// ========================================
// ТЕСТ 3: Проверка фильтров
// ========================================
function testFilters() {
  console.log('\n🔍 ТЕСТ 3: Проверка фильтров');
  
  // Проверка поля поиска
  let searchInput = null;
  const allInputs = document.querySelectorAll('input');
  
  for (let input of allInputs) {
    const placeholder = input.placeholder || '';
    const ariaLabel = input.getAttribute('aria-label') || '';
    
    if (placeholder.includes('Поиск') || ariaLabel.includes('Поиск')) {
      searchInput = input;
      break;
    }
  }
  
  if (searchInput) {
    console.log('✅ Поле поиска найдено');
    console.log('🔍 Placeholder:', searchInput.placeholder);
    
    // Тест поиска
    searchInput.value = 'Византийская';
    searchInput.dispatchEvent(new Event('input'));
    console.log('🔍 Выполнен поиск по "Византийская"');
  } else {
    console.log('❌ Поле поиска не найдено');
    console.log('🔍 Доступные input поля:', Array.from(allInputs).map(i => ({
      type: i.type,
      placeholder: i.placeholder,
      ariaLabel: i.getAttribute('aria-label')
    })));
  }
  
  // Проверка фильтра по типу
  const typeSelect = document.querySelector('select');
  if (typeSelect) {
    console.log('✅ Фильтр по типу найден');
    console.log(`📋 Доступных опций: ${typeSelect.options.length}`);
    
    // Проверка опций
    const options = Array.from(typeSelect.options).map(opt => opt.text);
    console.log('📝 Опции фильтра:', options);
  } else {
    console.log('❌ Фильтр по типу не найден');
  }
}

// ========================================
// ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
// ========================================
function runBasicTests() {
  console.log('🚀 ЗАПУСК БАЗОВЫХ ТЕСТОВ СТРАНИЦЫ "ГОСУДАРСТВА"');
  console.log('='.repeat(60));
  
  testPageLoad();
  testTableData();
  testFilters();
  
  console.log('\n' + '='.repeat(60));
  console.log('✅ БАЗОВЫЕ ТЕСТЫ ЗАВЕРШЕНЫ');
  console.log('📋 Проверьте результаты выше');
}

// Запуск тестов
runBasicTests();