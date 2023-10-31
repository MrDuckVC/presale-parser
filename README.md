# presale-parser

Django based project with notifications about changes in parsed sites.
Searches for new tenders and sends notifications to users. Each user have own list of keywords to search.

To run project:
1. Create and fill files:
    - database.env (example in database.env.dev)
    - backend.env (example in backend.env.dev)
    - docker-compose.override.yml (example in docker-compose.override-dev.yml)
2. Run `docker-compose up -d --build`
3. Run `docker-compose run backend python manage.py migrate`
4. Run `docker-compose run backend python manage.py createsuperuser`
5. Run `docker-compose run backend python manage.py collectstatic`
6. Run `docker-compose restart backend`
