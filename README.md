# Deep Player

An online video streaming service which automatically extracts insights like actors, scenes, keywords and multilingual subtitles using Microsoft's Video Indexer API.

## Screenshots

[Screenshot 1](https://github.com/codervivek/deep_player/blob/master/.vscode/Screenshot%20(1).png "Home Page")
[Screenshot 2](https://github.com/codervivek/deep_player/blob/master/.vscode/Screenshot%20(2).png "Video Page")

## Getting Started

Clone or fork the repo to make changes and test the site.

### Prerequisites

Install django and PostgreSQL.


### Installing

Create a vitual enviroment if you have deal with multiple python projects.

```
sudo apt-get install python-virtualenv
or
sudo easy_install virtualenv
or
sudo pip3 install virtualenv
```

```
mkdir ~/virtualenvironment
virtualenv ~/virtualenvironment/my_new_app
cd ~/virtualenvironment/my_new_app/bin
source activate
```

To install django.
Note: Use sudo only if some errors pop up.

```
sudo pip3 install django
```

Follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) to run PostgreSQL database.
PostgreSQL provides much better searching, indexing and scaliblity options.

Configure your Database settings in settings.py to run the database. Assign DEBUG False and configure the Apache/Nginx to host the django app, PostgreSQL database and required static files.

Finally run

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

in the directory which has manage.py to get your site up and running.


## Built With

* [Django](https://www.djangoproject.com/) - A python-based web framework
* [PostgreSQL](https://www.postgresql.org/) -  A powerful, open source object-relational database system
* [Microsoft Video Indexer API](https://azure.microsoft.com/en-us/services/cognitive-services/video-indexer/?cdn=disable) - A Video Indexing Service by Microsoft

## Contributing

TODO

## Authors

* **Vivek Raj**  - [Deep Player](https://github.com/codervivek/deep_player)
* **Ekagra Ranjan**
* **[Pawan Kumar](https://github.com/pavan71198)**

## License

TODO
