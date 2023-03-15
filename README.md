[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
![Pylint](https://github.com/bsa7/baseg/actions/workflows/pylint.yml/badge.svg)&nbsp;
![Pytest](https://github.com/bsa7/baseg/actions/workflows/pytest.yml/badge.svg)&nbsp;
![Coverage](https://gist.github.com/bsa7/03a5a726b2a02f55dc676a0e8df174f6/raw/coverage.svg)&nbsp;

# Сегментация клиентов банка

## Работа с кодом. Соглашения по стилям и т.п.
[Здесь](./docs/code-style.md) находится документация по стилю написания кода и т.п.

## Git flow. Соглашения по командной разработке.
[Здесь](./docs/git-flow.md) находится памятка по работе с ветками в Git.

## Запуск проверок
### Запуск тестов:
```bash
./scripts/run_pytest
```
После запуска тестов в папке coverage формируется файл index.html с отчётом по текущему покрытию кода проекта тестами.

### Запуск линтера PyLint
```bash
./scripts/run_pylint
```
