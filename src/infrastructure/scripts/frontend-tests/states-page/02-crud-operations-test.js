// ========================================
// ТЕСТ CRUD ОПЕРАЦИЙ СТРАНИЦЫ "ГОСУДАРСТВА"
// ========================================
// Назначение: Тестирование создания, чтения, обновления, удаления записей
// Использование: Выполнить в консоли браузера на странице /states
// Автор: AI Assistant
// Дата: 25 августа 2025

console.log('🧪 Тестирование CRUD операций страницы "Государства"');

// ========================================
// ТЕСТ 1: Создание записи
// ========================================
function testCreateRecord() {
  console.log('\n➕ ТЕСТ 1: Создание записи');
  
  const addButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Добавить государство')
  );
  
  if (addButton) {
    console.log('✅ Кнопка добавления найдена');
    addButton.click();
    
    setTimeout(() => {
      const dialog = document.querySelector('.q-dialog');
      if (dialog) {
        console.log('✅ Диалог создания открылся');
        
        // Проверяем поля формы
        const nameInput = dialog.querySelector('input[type="text"]');
        const typeSelect = dialog.querySelector('select');
        const periodSelect = dialog.querySelector('select:last-child');
        
        if (nameInput && typeSelect && periodSelect) {
          console.log('✅ Все поля формы найдены');
          
          // Заполняем форму
          nameInput.value = 'Тестовое государство (CRUD тест)';
          typeSelect.value = 'STATE';
          periodSelect.value = '2'; // Высокое Средневековье
          
          // Триггерим события для Vue
          nameInput.dispatchEvent(new Event('input'));
          typeSelect.dispatchEvent(new Event('change'));
          periodSelect.dispatchEvent(new Event('change'));
          
          console.log('📝 Форма заполнена:');
          console.log('  Название:', nameInput.value);
          console.log('  Тип:', typeSelect.value);
          console.log('  Период:', periodSelect.value);
          
          // Проверяем кнопку
          const createButton = dialog.querySelector('button[label="Создать"]');
          if (createButton) {
            console.log('✅ Кнопка "Создать" найдена');
            console.log('💡 Готово к созданию записи');
          } else {
            console.log('❌ Кнопка "Создать" не найдена');
          }
        } else {
          console.log('❌ Не все поля найдены');
        }
      } else {
        console.log('❌ Диалог создания не открылся');
      }
    }, 500);
  } else {
    console.log('❌ Кнопка добавления не найдена');
  }
}

// ========================================
// ТЕСТ 2: Редактирование записи
// ========================================
function testEditRecord() {
  console.log('\n✏️ ТЕСТ 2: Редактирование записи');
  
  const rows = document.querySelectorAll('tbody tr');
  if (rows.length > 0) {
    const firstRow = rows[0];
    const editButton = firstRow.querySelectorAll('button')[0]; // Кнопка редактирования
    
    if (editButton) {
      console.log('✅ Кнопка редактирования найдена');
      editButton.click();
      
      setTimeout(() => {
        const dialog = document.querySelector('.q-dialog');
        if (dialog) {
          console.log('✅ Диалог редактирования открылся');
          
          // Проверяем, что кнопка "Сохранить"
          const saveButton = dialog.querySelector('button[label="Сохранить"]');
          if (saveButton) {
            console.log('✅ Кнопка "Сохранить" найдена (правильный режим редактирования)');
          } else {
            console.log('❌ Кнопка "Сохранить" не найдена (возможно, режим создания)');
          }
          
          // Проверяем заполнение полей
          const nameInput = dialog.querySelector('input[type="text"]');
          if (nameInput && nameInput.value) {
            console.log('✅ Поле названия заполнено:', nameInput.value);
          } else {
            console.log('❌ Поле названия не заполнено');
          }
          
          // Закрываем диалог
          const cancelButton = dialog.querySelector('button[label="Отмена"]');
          if (cancelButton) {
            cancelButton.click();
            console.log('🔘 Диалог закрыт');
          }
        } else {
          console.log('❌ Диалог редактирования не открылся');
        }
      }, 500);
    } else {
      console.log('❌ Кнопка редактирования не найдена');
    }
  } else {
    console.log('⚠️ Нет записей для редактирования');
  }
}

// ========================================
// ТЕСТ 3: Удаление записи
// ========================================
function testDeleteRecord() {
  console.log('\n🗑️ ТЕСТ 3: Удаление записи');
  
  const rows = document.querySelectorAll('tbody tr');
  if (rows.length > 0) {
    // Берем последнюю запись для теста
    const lastRow = rows[rows.length - 1];
    const cells = lastRow.querySelectorAll('td');
    const name = cells[0] ? cells[0].textContent.trim() : 'Нет названия';
    
    console.log(`📝 Целевая запись: ${name}`);
    
    const deleteButton = lastRow.querySelectorAll('button')[2]; // Кнопка удаления
    
    if (deleteButton) {
      console.log('✅ Кнопка удаления найдена');
      console.log('🔘 Нажимаем кнопку удаления...');
      console.log('📋 Ожидаем появление диалога подтверждения');
      
      deleteButton.click();
      
      console.log('\n📋 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:');
      console.log('1. Должен появиться диалог с кнопками "Удалить" и "Отмена"');
      console.log('2. Нажмите "Отмена" - запись НЕ должна удалиться');
      console.log('3. Нажмите "Удалить" - запись должна удалиться');
      console.log('4. Проверьте консоль на правильную последовательность логов');
      
    } else {
      console.log('❌ Кнопка удаления не найдена');
    }
  } else {
    console.log('⚠️ Нет записей для удаления');
  }
}

// ========================================
// ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
// ========================================
function runCRUDTests() {
  console.log('🚀 ЗАПУСК ТЕСТОВ CRUD ОПЕРАЦИЙ');
  console.log('='.repeat(50));
  
  testCreateRecord();
  
  setTimeout(() => {
    testEditRecord();
  }, 3000);
  
  setTimeout(() => {
    testDeleteRecord();
  }, 6000);
  
  console.log('\n⏳ Тесты выполняются с задержками...');
  console.log('💡 Следуйте инструкциям в консоли для каждого теста');
}

// Запуск тестов
runCRUDTests();