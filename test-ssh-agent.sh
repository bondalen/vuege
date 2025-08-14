#!/bin/bash

echo "=== Тест SSH-агента ==="
echo

echo "1. Проверка переменной SSH_AUTH_SOCK:"
echo "SSH_AUTH_SOCK = $SSH_AUTH_SOCK"
echo

echo "2. Проверка добавленных ключей:"
ssh-add -l
echo

echo "3. Тест подключения к GitHub:"
ssh -T git@github.com
echo

echo "4. Тест git push (если есть изменения для коммита):"
if [ -n "$(git status --porcelain)" ]; then
    echo "Обнаружены изменения в репозитории"
    echo "Для тестирования git push выполните:"
    echo "  git add ."
    echo "  git commit -m 'Тестовый коммит'"
    echo "  git push origin main"
else
    echo "Нет изменений для коммита"
fi
echo

echo "=== Тест завершен ==="
