# 📸 Telegram Photo Analysis Bot

Бот анализирует фотографии с помощью Claude Vision AI и даёт подробное описание на русском языке.

---

## 🚀 Деплой на Railway (бесплатно, без вашего компьютера)

### Шаг 1 — Получить токены

**Telegram Bot Token:**
1. Откройте Telegram → найдите `@BotFather`
2. Напишите `/newbot`
3. Придумайте имя и username для бота
4. Скопируйте токен вида `1234567890:ABCdef...`

**Anthropic API Key:**
1. Зайдите на https://console.anthropic.com
2. Создайте аккаунт (или войдите)
3. Перейдите в `API Keys` → `Create Key`
4. Скопируйте ключ вида `sk-ant-...`

---

### Шаг 2 — Загрузить код на GitHub

1. Создайте новый репозиторий на https://github.com (нажмите `+` → `New repository`)
2. Назовите его `telegram-photo-bot`, нажмите `Create repository`
3. Загрузите файлы: `bot.py`, `requirements.txt`, `Procfile`
   - Нажмите `uploading an existing file`
   - Перетащите все три файла
   - Нажмите `Commit changes`

---

### Шаг 3 — Деплой на Railway

1. Зайдите на https://railway.app
2. Нажмите `Start a New Project`
3. Выберите `Deploy from GitHub repo`
4. Подключите GitHub и выберите ваш репозиторий `telegram-photo-bot`
5. Railway начнёт сборку — подождите 1-2 минуты

**Добавить переменные окружения:**
1. В вашем проекте нажмите на сервис
2. Перейдите во вкладку `Variables`
3. Нажмите `New Variable` и добавьте:
   - `TELEGRAM_TOKEN` = ваш токен от BotFather
   - `ANTHROPIC_API_KEY` = ваш ключ от Anthropic
4. Railway автоматически перезапустит бота

---

### Шаг 4 — Проверить работу

1. Откройте Telegram
2. Найдите вашего бота по username
3. Напишите `/start`
4. Отправьте любое фото → получите описание!

---

## 💡 Что умеет бот

- `/start` — приветствие
- `/help` — инструкция
- 📷 **Отправка фото** → подробное описание на русском
- 📎 **Фото как файл** (без сжатия) → тоже работает!

## 🔧 Альтернативный хостинг

Если Railway не подходит, можно использовать:
- **Render.com** — аналогично, бесплатный tier
- **Fly.io** — чуть сложнее настройка
- **VPS** — любой сервер с Python 3.10+

На VPS запуск:
```bash
pip install -r requirements.txt
export TELEGRAM_TOKEN="ваш_токен"
export ANTHROPIC_API_KEY="ваш_ключ"
python bot.py
```

---

## 📁 Структура файлов

```
telegram-photo-bot/
├── bot.py           # Основной код бота
├── requirements.txt # Зависимости Python
├── Procfile         # Команда запуска для Railway
└── README.md        # Эта инструкция
```
