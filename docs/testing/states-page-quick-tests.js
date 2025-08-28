// ========================================
// БЫСТРЫЕ ТЕСТЫ СТРАНИЦЫ "ГОСУДАРСТВА"
// Vuege - Автоматизированные тесты для браузера
// ========================================

console.log('🚀 Запуск быстрых тестов страницы "Государства"');

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
  const addButton = document.querySelector('button[label="Добавить государство"]');
  if (addButton) {
    console.log('✅ Кнопка "Добавить государство" найдена');
  } else {
    console.log('❌ Кнопка "Добавить государство" не найдена');
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
    } else {
      console.log('❌ Неправильная структура таблицы');
    }
    
    // Проверка кнопок действий
    const actionButtons = firstRow.querySelectorAll('button');
    console.log(`🔧 Кнопок действий в строке: ${actionButtons.length}`);
    
    if (actionButtons.length >= 3) {
      console.log('✅ Кнопки действий присутствуют');
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
  const searchInput = document.querySelector('input[placeholder*="Поиск"]');
  if (searchInput) {
    console.log('✅ Поле поиска найдено');
    
    // Тест поиска
    searchInput.value = 'Византийская';
    searchInput.dispatchEvent(new Event('input'));
    console.log('🔍 Выполнен поиск по "Византийская"');
  } else {
    console.log('❌ Поле поиска не найдено');
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
// ТЕСТ 4: Проверка диалога создания
// ========================================

function testCreateDialog() {
  console.log('\n➕ ТЕСТ 4: Проверка диалога создания');
  
  // Нажатие кнопки создания
  const addButton = document.querySelector('button[label="Добавить государство"]');
  if (addButton) {
    addButton.click();
    console.log('🔘 Нажата кнопка "Добавить государство"');
    
    // Ждем появления диалога
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        console.log('✅ Диалог создания открылся');
        
        // Проверка полей формы
        const nameInput = dialog.querySelector('input[label="Название"]');
        const typeSelect = dialog.querySelector('select');
        const dateInput = dialog.querySelector('input[type="date"]');
        const checkbox = dialog.querySelector('input[type="checkbox"]');
        
        if (nameInput) console.log('✅ Поле "Название" найдено');
        if (typeSelect) console.log('✅ Поле "Тип" найдено');
        if (dateInput) console.log('✅ Поле "Дата" найдено');
        if (checkbox) console.log('✅ Чекбокс "Вымышленное" найден');
        
        // Закрытие диалога
        const cancelButton = dialog.querySelector('button[label="Отмена"]');
        if (cancelButton) {
          cancelButton.click();
          console.log('🔘 Диалог закрыт');
        }
      } else {
        console.log('❌ Диалог создания не открылся');
      }
    }, 500);
  } else {
    console.log('❌ Кнопка создания не найдена');
  }
}

// ========================================
// ТЕСТ 5: Проверка кнопок действий
// ========================================

function testActionButtons() {
  console.log('\n🔧 ТЕСТ 5: Проверка кнопок действий');
  
  const rows = document.querySelectorAll('tbody tr');
  if (rows.length > 0) {
    const firstRow = rows[0];
    const buttons = firstRow.querySelectorAll('button');
    
    console.log(`🔘 Найдено кнопок в первой строке: ${buttons.length}`);
    
    // Проверка иконок кнопок
    buttons.forEach((button, index) => {
      const icon = button.querySelector('i') || button.getAttribute('icon');
      console.log(`🔘 Кнопка ${index + 1}: ${icon || 'без иконки'}`);
    });
    
    // Тест кнопки редактирования
    const editButton = firstRow.querySelector('button[icon="edit"]');
    if (editButton) {
      console.log('✅ Кнопка редактирования найдена');
    } else {
      console.log('❌ Кнопка редактирования не найдена');
    }
    
    // Тест кнопки карты
    const mapButton = firstRow.querySelector('button[icon="map"]');
    if (mapButton) {
      console.log('✅ Кнопка карты найдена');
    } else {
      console.log('❌ Кнопка карты не найдена');
    }
    
    // Тест кнопки удаления
    const deleteButton = firstRow.querySelector('button[icon="delete"]');
    if (deleteButton) {
      console.log('✅ Кнопка удаления найдена');
    } else {
      console.log('❌ Кнопка удаления не найдена');
    }
  } else {
    console.log('⚠️ Нет данных для проверки кнопок действий');
  }
}

// ========================================
// ТЕСТ 6: Проверка GraphQL данных
// ========================================

function testGraphQLData() {
  console.log('\n🔗 ТЕСТ 6: Проверка GraphQL данных');
  
  // Проверка Apollo Client
  if (window.__APOLLO_CLIENT__) {
    console.log('✅ Apollo Client доступен');
    
    // Получение кэша
    const cache = window.__APOLLO_CLIENT__.cache.extract();
    console.log('📦 Данные в кэше Apollo:', Object.keys(cache));
    
    // Поиск данных организаций
    const orgData = Object.values(cache).find(item => 
      item && typeof item === 'object' && item.__typename === 'OrganizationalUnit'
    );
    
    if (orgData) {
      console.log('✅ Данные организаций найдены в кэше');
      console.log('📝 Пример записи:', {
        id: orgData.id,
        name: orgData.name,
        type: orgData.type
      });
    } else {
      console.log('⚠️ Данные организаций не найдены в кэше');
    }
  } else {
    console.log('❌ Apollo Client не доступен');
  }
}

// ========================================
// ТЕСТ 7: Проверка производительности
// ========================================

function testPerformance() {
  console.log('\n⚡ ТЕСТ 7: Проверка производительности');
  
  // Время загрузки страницы
  const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
  console.log(`⏱️ Время загрузки страницы: ${loadTime}мс`);
  
  // Время до интерактивности
  const domContentLoaded = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
  console.log(`⚡ Время до интерактивности: ${domContentLoaded}мс`);
  
  // Количество DOM элементов
  const domElements = document.querySelectorAll('*').length;
  console.log(`🏗️ Количество DOM элементов: ${domElements}`);
  
  // Оценка производительности
  if (loadTime < 3000) {
    console.log('✅ Отличная производительность загрузки');
  } else if (loadTime < 5000) {
    console.log('⚠️ Приемлемая производительность загрузки');
  } else {
    console.log('❌ Медленная загрузка страницы');
  }
}

// ========================================
// ТЕСТ 8: Проверка адаптивности
// ========================================

function testResponsiveness() {
  console.log('\n📱 ТЕСТ 8: Проверка адаптивности');
  
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight
  };
  
  console.log(`📐 Размер viewport: ${viewport.width}x${viewport.height}`);
  
  // Проверка адаптивных классов
  const responsiveElements = document.querySelectorAll('.col-12, .col-sm-6, .col-md-4');
  console.log(`📱 Адаптивных элементов: ${responsiveElements.length}`);
  
  // Проверка мобильной навигации
  const mobileNav = document.querySelector('.q-header, .q-drawer');
  if (mobileNav) {
    console.log('✅ Мобильная навигация найдена');
  } else {
    console.log('⚠️ Мобильная навигация не найдена');
  }
  
  // Оценка адаптивности
  if (viewport.width < 768) {
    console.log('📱 Мобильный режим');
  } else if (viewport.width < 1024) {
    console.log('📱 Планшетный режим');
  } else {
    console.log('💻 Десктопный режим');
  }
}

// ========================================
// ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
// ========================================

function runAllTests() {
  console.log('🚀 ЗАПУСК ВСЕХ ТЕСТОВ СТРАНИЦЫ "ГОСУДАРСТВА"');
  console.log('=' .repeat(60));
  
  // Ждем полной загрузки страницы
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(runTests, 1000);
    });
  } else {
    setTimeout(runTests, 1000);
  }
}

function runTests() {
  testPageLoad();
  testTableData();
  testFilters();
  testCreateDialog();
  testActionButtons();
  testGraphQLData();
  testPerformance();
  testResponsiveness();
  
  console.log('\n' + '=' .repeat(60));
  console.log('✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ');
  console.log('📋 Проверьте результаты выше');
}

// ========================================
// УТИЛИТЫ ДЛЯ РУЧНОГО ТЕСТИРОВАНИЯ
// ========================================

// Функция для тестирования поиска
window.testSearch = function(query) {
  const searchInput = document.querySelector('input[placeholder*="Поиск"]');
  if (searchInput) {
    searchInput.value = query;
    searchInput.dispatchEvent(new Event('input'));
    console.log(`🔍 Выполнен поиск: "${query}"`);
  } else {
    console.log('❌ Поле поиска не найдено');
  }
};

// Функция для тестирования фильтра
window.testFilter = function(type) {
  const typeSelect = document.querySelector('select');
  if (typeSelect) {
    typeSelect.value = type;
    typeSelect.dispatchEvent(new Event('change'));
    console.log(`🔍 Применен фильтр: "${type}"`);
  } else {
    console.log('❌ Фильтр не найден');
  }
};

// Функция для создания тестовой записи
window.createTestRecord = function() {
  const addButton = document.querySelector('button[label="Добавить государство"]');
  if (addButton) {
    addButton.click();
    
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        const nameInput = dialog.querySelector('input[label="Название"]');
        const typeSelect = dialog.querySelector('select');
        
        if (nameInput) nameInput.value = 'Тестовое государство';
        if (typeSelect) typeSelect.value = 'STATE';
        
        const createButton = dialog.querySelector('button[label="Создать"]');
        if (createButton) createButton.click();
        
        console.log('✅ Тестовая запись создана');
      }
    }, 500);
  }
};

// Автоматический запуск тестов
console.log('🎯 Для запуска тестов выполните: runAllTests()');
console.log('🔧 Доступные утилиты:');
console.log('  - testSearch("запрос") - тест поиска');
console.log('  - testFilter("TYPE") - тест фильтра');
console.log('  - createTestRecord() - создание тестовой записи');

// Экспорт функций для использования
window.runAllTests = runAllTests;
window.testSearch = window.testSearch;
window.testFilter = window.testFilter;
window.createTestRecord = window.createTestRecord;