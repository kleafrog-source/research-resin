# Contributing to AMMS / MMSS

Спасибо за интерес к проекту! Ниже — краткие правила и рекомендации.

1. Форки и PR
- Форкните репозиторий, создайте feature-ветку из main: git checkout -b feat/your-feature
- Оформляйте PR в main с понятным описанием и ссылкой на issue (если есть).

2. Код-стайл
- Rust: используйте rustfmt и clippy. Запуск локально:
  - cargo fmt --all
  - cargo clippy --all-targets --all-features -- -D warnings

3. Тесты
- Добавляйте модульные тесты для любой новой функциональности.
- Интеграционные тесты для API в examples/tests приветствуются.

4. Документация
- Обновляйте README и API docs при изменениях интерфейсов.
- Для публичных API добавьте OpenAPI/Swagger спецификацию.

5. CI
- На каждый PR CI запускает сборку, clippy, test и python checks.

6. Связь
- Для архитектурных предложений создавайте issue с меткой enhancement, указывайте backward-incompatible изменения.
