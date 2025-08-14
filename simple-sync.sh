#!/bin/bash

echo "Синхронизация с GitHub..."

# Простые команды без pager
git add docs/changelog.md docs/tasktracker.md docs/others/terminal-rules.md .cursorrules sync-to-github.sh simple-sync.sh

git commit -m "Обновление: правила работы с терминалом и задачи"

git push origin main

echo "Синхронизация завершена!"
