## Git flow

### Настройте Git для удобства использования:
Добавьте алиасы (псевдонимы) для часто используемых команд:
```
git config --global alias.br 'branch'
git config --global alias.cd 'checkout develop'
git config --global alias.co 'checkout'
git config --global alias.pod 'pull origin develop'
git config --global alias.rd 'rebase develop'
git config --global alias.st 'status'
```

Добавьте информацию о себе:
```
git config user.name 'John Doe'
git config user.email John.Doe@urfu.me
```

Добавьте плагин rerere - он сэкономит вам (но это не точно) кучу нервов при разрешении конфликтов правок.
```
git config pull.rebase true
git config --global rerere.enabled true
git config --global rerere.autoUpdate true
```

Так же вы можете использовать конфигурационный файл для Git, поместив его в своей домашней директории, либо в папке проекта:
```
# ~/.gitconfig
[user]
  email = John.Doe@urfu.me
  name = John Doe

[alias]
  st = status
  br = branch
  co = checkout
  rd = rebase develop
  pod = pull origin develop
[cola]
  spellcheck = false
  tabwidth = 2
  textwidth = 100
[init]
  defaultBranch = develop
[rerere]
  enabled = true
  autoUpdate = true
```

### 1. Получение проекта
Откройте терминал и смените текущую папку на папку с вашими проектами:
```bash
cd /home/username/projects
```

Клонируйте код проекта - будет создана папка `/home/username/projects/baseg`:
```bash
git clone git@github.com:bsa7/baseg.git
```

Перейдите в созданную директорию
```bash
cd ./baseg
```

Синхронизируйтесь с репозиторием проекта:
```bash
git fetch
```

Посмотрите список веток:
```bash
git br
```

Смените текущую ветку на `develop`:
```bash
git co develop
```

> Запомните! `develop` - это основная ветка для разработки. Все ваши ветки будут создаваться только от неё. Это просто.

Создайте свою ветку:
```bash
git checkout -b BS-001-create-something
```

Внесите изменения в код и посмотрите, что покажет Git:
```bash
git st
```

Посмотрите изменения, внесённые в файлы. В консоли это можно сделать так:
```bash
git diff ./file_name.py
```

Сохраните результаты вашей работы:
```bash
git add .
git commit -m 'BS-001 Создать кое-что'
```

Когда вы собираетесь добавить ещё изменения в тот же коммит (новый, а не последний в `develop`) - используйте `amend`:
```bash
git add .
git commit --amend
```

Пушить текущую ветку в репозиторий:
```bash
git push origin HEAD
```

Используйте ключ `force` если вы хотите "перепушить" ваш новый текущий коммит:
```bash
git push -f origin HEAD
```

Если ваша ветка устарела, то есть в ветку `develop` был влит новый код, обновите свою ветку:
```bash
git co develop
git pod
git co BS-001-add-gitflow-documentation-to-readme
git rd
git push -f origin BS-001-add-gitflow-documentation-to-readme
```

### 2. Работа с трекером задач.
Присваивайте задачам в Trello префикс вида `BS-001-`. Например, задача в трелло называется:
`BS-001 Добавить описание Gitflow`. Называем ветку `BS-001-add-gitflow-documentation-to-readme`.

Commit changes in your current task:
```bash
git add .
git commit -m 'BS-001 Добавить описание Gitflow'
```

После того, как коммит сделан, изменения сохранены. Нужно обновить вашу ветку:
```bash
git co develop
git pod
```

Обновите вашу ветку к текущей голове ветки `develop`:
```bash
git co BS-001-add-gitflow-documentation-to-readme
git rd
```

Теперь можно пушить ветку в репозиторий
```bash
git push -f origin BS-001-add-gitflow-documentation-to-readme
```

перейдите в раздел "[Пулл-реквесты](https://github.com/bsa7/baseg/pulls)", создайте пулл-реквест, назначьте ревьюверов, проверьте код.


## Разрешение конфликтов правок
Лучшее на сегодняшний день решение, помогающее снизить объём правок - [rerere](https://git-scm.com/book/ru/v2/%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B-Git-Rerere) - инструкции по активации по ссылке или см. выше по тексту.

Основной тактикой по снижению расходов на разрешение конфликтов является создание пулл-реквестов, содержащих только один коммит. Запомните, каждый конфликт в вашем коммите в вашей ветке вы будете разрешать по отдельности. Если вы сделаете много коммитов, процесс ресолвинга может растянуться.
