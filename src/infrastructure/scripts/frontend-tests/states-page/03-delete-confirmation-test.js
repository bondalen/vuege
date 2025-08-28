// ========================================
// ТЕСТ ПОДТВЕРЖДЕНИЯ УДАЛЕНИЯ
// ========================================
// Назначение: Тестирование диалога подтверждения удаления
// Использование: Выполнить в консоли браузера на странице /states
// Автор: AI Assistant
// Дата: 25 августа 2025

console.log('🎯 Тест подтверждения удаления');

// ========================================
// ТЕСТ: Удаление с принудительным ожиданием
// ========================================
function testDeleteWithConfirmation() {
  console.log('\n🗑️ ТЕСТ: Удаление с принудительным ожиданием ответа');
  
  const rows = document.querySelectorAll('tbody tr');
  console.log(`📊 Всего записей в таблице: ${rows.length}`);
  
  if (rows.length > 0) {
    // Берем предпоследнюю запись для теста (менее важную)
    const targetRow = rows[rows.length - 2];
    const cells = targetRow.querySelectorAll('td');
    const name = cells[0] ? cells[0].textContent.trim() : 'Нет названия';
    
    console.log(`📝 Целевая запись: ${name}`);
    
    const deleteButton = targetRow.querySelectorAll('button')[2]; // Кнопка удаления
    
    if (deleteButton) {
      console.log('🔘 Нажимаем кнопку удаления...');
      console.log('📋 Ожидаем появление диалога подтверждения');
      console.log('💡 Теперь процесс должен быть:');
      console.log('   1. Диалог подтверждения появляется');
      console.log('   2. Удаление НЕ происходит до ответа пользователя');
      console.log('   3. Кнопка "Отмена" предотвращает удаление');
      console.log('   4. Кнопка "Удалить" выполняет удаление');
      console.log('   5. В консоли видны логи действий пользователя');
      
      deleteButton.click();
      
      console.log('\n📋 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:');
      console.log('1. Должен появиться диалог с кнопками "Удалить" и "Отмена"');
      console.log('2. Нажмите "Отмена" - в консоли должно появиться "❌ Пользователь нажал Отмена"');
      console.log('3. Нажмите "Удалить" - в консоли должно появиться "✅ Пользователь нажал Удалить"');
      console.log('4. Проверьте, что удаление происходит только после подтверждения');
      
    } else {
      console.log('❌ Кнопка удаления не найдена');
    }
  } else {
    console.log('⚠️ Нет записей для тестирования удаления');
  }
}

// ========================================
// ТЕСТ: Удаление конкретной записи
// ========================================
function testDeleteSpecificRecord(recordIndex = 0) {
  console.log(`\n🗑️ ТЕСТ: Удаление записи с индексом ${recordIndex}`);
  
  const rows = document.querySelectorAll('tbody tr');
  console.log(`📊 Всего записей в таблице: ${rows.length}`);
  
  if (rows.length > recordIndex) {
    const targetRow = rows[recordIndex];
    const cells = targetRow.querySelectorAll('td');
    const name = cells[0] ? cells[0].textContent.trim() : 'Нет названия';
    
    console.log(`📝 Целевая запись: ${name}`);
    
    const deleteButton = targetRow.querySelectorAll('button')[2]; // Кнопка удаления
    
    if (deleteButton) {
      console.log('🔘 Нажимаем кнопку удаления...');
      deleteButton.click();
      
      console.log('\n📋 ИНСТРУКЦИИ:');
      console.log(`1. Будет удалена запись: "${name}"`);
      console.log('2. Подтвердите удаление в диалоге');
      console.log('3. Проверьте результат');
      
    } else {
      console.log('❌ Кнопка удаления не найдена');
    }
  } else {
    console.log(`❌ Запись с индексом ${recordIndex} не найдена`);
  }
}

// ========================================
// ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
// ========================================
function runDeleteTests() {
  console.log('🚀 ЗАПУСК ТЕСТОВ ПОДТВЕРЖДЕНИЯ УДАЛЕНИЯ');
  console.log('='.repeat(60));
  
  testDeleteWithConfirmation();
  
  console.log('\n💡 Дополнительные тесты:');
  console.log('- testDeleteSpecificRecord(0) - удалить первую запись');
  console.log('- testDeleteSpecificRecord(1) - удалить вторую запись');
  console.log('- testDeleteSpecificRecord(5) - удалить шестую запись');
}

// Запуск тестов
runDeleteTests();