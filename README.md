# Petstore API Test Automation

Автоматизированное тестирование API для [Petstore Swagger](https://petstore.swagger.io).

## Описание проекта

Проект содержит автотесты для публичного API Petstore, демонстрирующий:
- Функциональное тестирование REST API
- Расширяемую архитектуру для масштабирования тестов
- Покрытие основных CRUD операций
- Обработку позитивных и негативных сценариев

## Технологический стек

- **Python 3.8+**
- **pytest** - фреймворк для написания и запуска тестов
- **requests** - библиотека для HTTP-запросов

## Структура проекта

```
.
├── tests/                  # Тестовые файлы
│   ├── test_pet.py         # Тесты для /pet endpoint
│   └── test_store.py       # Тесты для /store/order endpoint
├── helpers/                # Вспомогательные модули
│   ├── api_client.py       # API клиент для HTTP-запросов
│   └── data_generators.py  # Генераторы тестовых данных
├── conftest.py            # Pytest фикстуры и настройки
├── requirements.txt       # Зависимости проекта
└── README.md             # Документация
```

## Установка и настройка

### Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

### Установка зависимостей

1. Клонируйте репозиторий (или убедитесь, что вы находитесь в директории проекта)

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

Или для установки только основных зависимостей:

```bash
pip install pytest requests
```

## Запуск тестов

### Запуск всех тестов

```bash
pytest
```

### Запуск тестов для конкретного endpoint

```bash
# Тесты для /pet
pytest tests/test_pet.py

# Тесты для /store
pytest tests/test_store.py
```

### Запуск конкретного теста

```bash
pytest tests/test_pet.py::TestPetCreate::test_create_pet_success
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск с выводом print-ов

```bash
pytest -s
```

### Запуск с покрытием кода (требует pytest-cov)

```bash
pytest --cov=helpers --cov-report=html
```

После выполнения откройте `htmlcov/index.html` в браузере для просмотра отчета.

### Запуск только позитивных тестов

```bash
pytest -k "success"
```

### Запуск только негативных тестов

```bash
pytest -k "invalid or nonexistent"
```
