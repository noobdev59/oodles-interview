# Oodle Interview Application

This application was built as a task for the position of Django Developer at [Oodles Technologies](https://www.oodlestechnologies.com/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

Install the dependencies

```bash
pip install -r requirements.txt
```

Default DB being used is [Sqlite](https://www.sqlite.org/index.html) for better compatibility to run on all environments without the hassle to setup a DB on local machine.

The DB has been reset using the following command 

```bash
./manage.py reset_db
```


## Usage

```python
./manage.py migrate && ./manage.py createsuperuser
```

Once the superuser is created you can navigate to baked in Admin interface provided by [Django](http://djangoproject.com/).

The base URL to start navigating API's is at ```/api/v1/```  this will list all the routes registered through [DRF's](https://www.django-rest-framework.org/) [default router](https://www.django-rest-framework.org/api-guide/routers/#defaultrouter).

Other than that you can directly visit ```/api/v1/redoc``` to learn about all the URL's registered inside ```urlparameters```.

## License
[MIT](https://choosealicense.com/licenses/mit/)
