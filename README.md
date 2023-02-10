# Practice blog



## Description



This app is an extensible web blog api.



## Built with

* Python

* Django

* DRF

* Docker

* PostgreSQL



## Getting Started



In order to use this app: clone this repository to your machine, in terminal go to project directory and run either development or production version of docker command:

### Development version

```

docker compose up -d --build

```

### Production version

```

docker compose -f docker-compose.prod.yml up -d --build

```

### After that you will need to apply database migrations

```

docker exec practice_blog-web-1 sh -c "python manage.py migrate"

```

### After that you have two options:

* populate reactions table by yourself
* populate reactions with premade command and than extend with additional types if needed

### Command to populate reaction table with default data

```

docker exec practice_blog-web-1 sh -c "python manage.py init_reactions"

```

## To put containers down you can use next command

### Development version

```

docker compose down

```

### Production version

```

docker compose -f docker-compose.prod.yml down

```

### On either of versions you can use "-v" option to delete volumes