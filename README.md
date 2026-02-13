# Todo List bot


A Telegram bot which uses Django REST API, providing users with simple ToDo list app.

### Quick start

1. Clone the repository

```bash
git clone https://github.com/Prisma4/todo-list-bot.git
cd todo-list-bot
```

2. Create .env file in the root folder and fill it:

```env
DJANGO_SECRET_KEY=django-insecure-...  # you django secret key.
DJANGO_DEBUG=True  # set to False in prod
DJANGO_ALLOWED_HOSTS=backend,localhost  # 'backend' is required, 'localhost' is optional if you want to use Django admin.
PSQL_NAME=todo_list
PSQL_USER=user
PSQL_PASS=some_password
PSQL_PORT=5432
BOT_TOKEN=your_telegram_bot_token  # you can get telegram bot token from @BotFather bot in telegram
BASE_API_URL=http://backend:8000  # base django api url for bot. format: 'container_name:internal_port'
BOT_API_AUTH_TOKEN=your_rest_framework_auth_token_with_admin_rights  # django-rest auth token for bot to authentificate requests.
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

#### You can generate `DJANGO_SECRET_KEY` with command bellow ( make sure Django is installed beforehand ):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### You can generate `BOT_API_AUTH_TOKEN` with commands below:

Firstly, you need to create superuser account with the command bellow ( in the **backend** container ). It will ask you to type name, email and password. First two is optional - and default name is 'root'.

```bash
python manage.py createsuperuser
```

Then, you have **two** options.

The first one is to use django shell. You need to replace 'your_username' with name you gave superuser account. Make sure you're in the **backend** container. The following command will print auth_token in console.

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; from rest_framework.authtoken.models import Token; User = get_user_model(); u = User.objects.get(username='your_username'); t, _ = Token.objects.get_or_create(user=u); print(t.key)"
```

The second one is to use django-admin. Go to 'localhost:8000/admin', chose 'Tokens' in the 'Auth Tokens' app, then choose created user and create a token.

3. Run docker-compose

```bash
docker-compose up --build 
```

Now just wait for containers to build, and the bot is ready to use!