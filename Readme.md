# Server Dashboard

Flask-страница с кнопками для перехода к инструментам дата-инженерии и аналитики.

## Запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Откройте http://localhost:5000

## Как добавить секцию или кнопку

Инструменты сгруппированы в `config/tools.yaml` по секциям. Порядок секций на странице = порядок в файле.

### Новая секция

```yaml
sections:
  - id: my-section
    title: "Моя секция"
    row: top              # опционально: одинаковый row у соседних секций = одна строка
    tools: []
```

Чтобы разместить две секции рядом, задайте им одинаковое значение `row` (например `row: top`) и расположите их подряд в YAML.

### Новая кнопка

Добавьте блок в `tools` нужной секции:

```yaml
      - id: my-tool
        name: My Tool
        url: "http://172.17.1.100:8080"
        icon: "icons/my-tool.png"   # или emoji: "🔧"
        running: true                 # true = «ЗАПУЩЕН», false = «НЕ ЗАПУЩЕН»
        credentials:                  # null — сразу открывает url
          login: user
          password: pass
        open_url: true                # true — кнопка «Открыть» в модалке
        connection_guide: null        # инструкция подключения (обязательна при open_url: false)
```

### Поля

| Поле | Описание |
|------|----------|
| `id` | Уникальный идентификатор |
| `name` | Название на кнопке |
| `url` | Адрес инструмента |
| `icon` | Emoji или путь к PNG/JPG/SVG в `static/` (например `icons/airflow.png`) |
| `running` | `true` — зелёная плашка «ЗАПУЩЕН», `false` — красная «НЕ ЗАПУЩЕН» |
| `credentials` | `null` или `{ login, password }` |
| `open_url` | `true` — в модалке есть кнопка «Открыть»; `false` — только креды и инструкция |
| `connection_guide` | Текст инструкции (многострочный через `\|`) |

### PNG-иконки

1. Положите файл в `static/icons/` (например `static/icons/airflow.png`)
2. Укажите путь в поле `icon`: `icons/airflow.png`
3. Рекомендуемый размер: 128×128 px, прозрачный фон

## Как изменить цветовую палитру

Откройте `static/css/style.css` и измените переменные в блоке `:root`:

| Переменная | Назначение |
|------------|------------|
| `--bg-gradient-start`, `--bg-gradient-end` | Фон страницы |
| `--card-bg`, `--card-bg-hover` | Фон карточек |
| `--accent`, `--accent-hover` | Кнопки и ссылки |
| `--status-running` | Зелёная плашка «ЗАПУЩЕН» |
| `--status-stopped` | Красная плашка «НЕ ЗАПУЩЕН» |
| `--text-primary`, `--text-secondary` | Текст |

## Поведение модального окна

- **Есть credentials + `open_url: true`** — показываются логин/пароль и кнопка «Открыть»
- **Есть credentials + `open_url: false`** — показываются логин/пароль и `connection_guide`, без кнопки «Открыть»
- **Нет credentials** — клик сразу открывает `url` в новой вкладке (если указан)
