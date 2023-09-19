# Train Station Api
- Api service for Train Station written on DRF

## Features:
- JWT authenticated
- Admin panel /admin/
- Documentation is located via /api/doc/swagger/
- Creating, updating trains, type_trains, stations, routes(Only for staff) 
- Coordinate Geolocation: Using Postgis extension. Locations of stations, routes, and entities can be represented as point coordinates
- Notification on email when create new order
- Notification when your departure time min then 1 day
- Task control using the flower
- Payment using the Stripe service
- Docker app starts only when db is available ( custom command via management/commands )

## Installing using GitHub:
 - Install Postgres and Postgis extension, then create DB
 - Open .env.sample and change environment variables on yours !Rename file from .env_sample to .env

```shell
git clone https://github.com/bythewaters/train-station-api.git
cd train_station_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- Use the following command to load prepared data from fixture(if you need):
  - `python manage.py loaddata fixture.json`.

## Defaults users:
```
1. Staff:
  email: trainadmin@admin.com
  password: trainadmin
  
Also you can create your superuser using command:
python manage.py createsuperuser
```

## Connect Stripe Payment:
1. Register on site [stripe.com](https://www.stripe.com)
2. Copy your secret key and set in .env file.

## Run with Docker:
- Docker should be installed
```
- docker-compose build .
- docker-compose up
```
- Use the following command to load prepared data from fixture in docker(if you need):
  `docker-compose run --rm app python manage.py loaddata library_service_data.json`

## Getting access:
- Create user via /api/user/register/
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR 
- Install ModHeader extension and create Request header with value ```Bearer <Your access token>```

## Addition information
```
If you want to work in local emvironment, you must to add GDAL and GEO path in settings.py file.
If you want to work in docker, you must coment or delete this piece of code.
```