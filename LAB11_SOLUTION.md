# Лабораторная 11: Организация CI/CD и автоматизированного тестирования

Ниже готовое решение варианта с **GitHub Actions**.

## 1) Простая веб-страница

Сделана форма обратной связи:
- `index.html`
- `styles.css`
- `script.js`

Логика:
- кнопка отправки неактивна, пока поля невалидны;
- после успешной отправки показывается сообщение пользователю.

## 2) Репозиторий и ветки

Локально инициализируйте git и создайте ветки:

```bash
git init
git branch -M main
git add .
git commit -m "Initial commit: lab11 base"
git branch dev
git branch fix
```

Подключите удалённый репозиторий GitHub и отправьте ветки:

```bash
git remote add origin <URL_ВАШЕГО_REPO>
git push -u origin main
git push -u origin dev
git push -u origin fix
```

## 3) Автоматизированные UI-тесты (3-4 теста)

Реализовано 4 теста Selenium + pytest:
- `tests/ui/test_feedback_form.py`

Проверки:
1. Заголовок формы отображается.
2. Кнопка отправки отключена на пустой форме.
3. Кнопка активируется при валидных данных.
4. После отправки показывается сообщение об успехе.

## 4) Автозапуск тестов на push / PR (CI)

Workflow: `.github/workflows/ci.yml`

Что делает:
- запускается на `push` в `main/dev/fix/fix/**`;
- запускается на `pull_request` в `main` и `dev`;
- ставит Python, Chrome, зависимости;
- запускает `pytest -v`.

## 5) Проверка падения тестов при ошибках

Для демонстрации:
1. Измените ожидаемый текст в `index.html` (например заголовок формы).
2. Сделайте push в ветку.
3. В Actions тесты должны упасть.

## 6) Работа через Pull Requests

Прямые коммиты в `main` не используйте. Поток:
- feature/fix-ветка от `dev`;
- PR `fix/* -> dev`;
- после зелёных тестов merge в `dev`;
- затем PR `dev -> main`;
- после зелёных тестов merge в `main`.

## 7) Сценарий из задания (fix -> dev -> main)

Пример команд:

```bash
git checkout dev
git checkout -b fix/change-button-text
# вносим изменения в код
git add .
git commit -m "Change button text"
git push -u origin fix/change-button-text
```

Далее на GitHub:
1. Создать PR `fix/change-button-text -> dev`.
2. Дождаться прохождения CI, исправить ошибки при необходимости.
3. Merge PR в `dev`.
4. Создать второй PR `dev -> main`.
5. После прохождения тестов выполнить merge.

## 8) Автопубликация на GitHub Pages (CD)

В `ci.yml` есть job `deploy`:
- стартует только если `tests` прошли успешно;
- работает только для `push` в `main`;
- публикует сайт через GitHub Pages.

Условие деплоя:
- `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`

## 9) Локальный запуск тестов

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

---

Если хочешь, я могу дополнительно сделать версию этого же решения под Jenkins (`Jenkinsfile`) для второго варианта задания.
