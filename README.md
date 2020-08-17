# show rates of currencies
## Description
Test web app for getting and displaying currencies' exchange rates.
All rates and list of currencies are gotten from https://ru.cryptonator.com/api/

## Installing and running
1. Build and run project: `docker-compose up --build -d`
1. Run migrations on DB: `docker-compose exec web python manage.py migrate`
1. Populate DB with initial list of available currencies: `docker-compose exec web python manage.py migrate`
1. Try to open `http://0.0.0.0:8000` 
