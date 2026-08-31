# YaCut - сервис укорачивания ссылок

Сервис YaCut позволяет сокращать длинные ссылки, загружать файлы на Яндекс.Диск и получать короткие ссылки для скачивания.


## Как запустить проект Yacut

### 1. Клонировать репозиторий и перейти в него

```bash
git clone <url-репозитория>
cd yacut
```

### 2. Создать и активировать виртуальное окружение

#### 🐧 Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🪟 Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### 🪟 Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### 🪟 Windows (Git Bash / MINGW64)

```powershell
python -m venv venv
source venv/Scripts/activate
```

### 3. Установить зависимости

#### Обновить pip (рекомендуется)

```bash
python -m pip install --upgrade pip
```

#### Установить все зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать файл .env с переменными окружения

В корневой директории проекта создайте файл .env со следующим содержимым:
Cоздать и активировать виртуальное окружение:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=<ваш_токен_Яндекс_Диска>
```

### 5. Создать базу данных и применить миграции

#### Инициализировать папку миграций (если ещё не создана)

```bash
flask db init
```

#### Создать миграцию (если модели изменились)

```bash
flask db migrate -m "initial"
```

#### Применить миграции к базе данных

```bash
flask db upgrade
```

Для Windows (если команда flask не распознаётся):

```bash
python -m flask db upgrade
```

### 6. Запустить проект

```bash
flask run
```

После запуска сервер будет доступен по адресу: http://127.0.0.1:5000/

Для Windows (альтернатива):

```bash
python -m flask run
```
