# PHPSupportBot
 
This project is the telegram chat-bot, created to organize the PHP order exchange and help 
to interact with clients and contractors, support them and collect statistic of it.

Bot allows: 
 * for clients: to create and edit orders, connect to contractor and support, and buy a subscription of service
 * for contractors: take and close orders, connect to client and support, take work statistic
 * for managers: receive notifications, look information about orders(exclude secret information, like passwords from site)
 * for admin: get statistic of clients, contractor and orders by admin page, give and close access for contractors

Service used [Redis](https://redis.com/) to save temporary data and [Yookassa](https://yookassa.ru/) to
take payment

## `env's`

Env variables needet to run project:

```commandline
# url with your postgres db data
POSTGRES_URL=postgres://user:password@host:port/database

# settings of redis database
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=

# token of your telegram chat-bot
TELEGRAM_TOKEN=

# yookassa payment token
PAYMENT_TOKEN = 

# django settings
ALLOWED_HOSTS=
DEBUG=
SECRET_KEY=
```

## Requirements

All requirements collected in `requirements.txt` file, to install:

```commandline
pip install -r requirements.txt
```

## Local launch

Bot contains two parts: django-site and chat-bot. To run in locally, set
```commandline
DEBUG=True
SECRET_KEY= `any secret key`
```
And your postgres, redis and telegram settings. Yookassa is optional setting, 
but without it payment doesn't work

Commands to launch
```commandline
python manage.py runserver   # django-site
python manage.py start_bot   # bot
```