## What about
This is a TODO api as a step by step tutorial to create a RESTful API using [Flask](https://flask.palletsprojects.com/)
* Get TODO list
* Connect to DB 
* POST to add new task
* improve with mvc MODEL
* Frontend with React
* User login
* Docker
* AWS ELB  
* K8S

## Installation

1. [virtualenv](https://realpython.com/python-virtual-environments-a-primer/)
2. [Installation](https://flask.palletsprojects.com/en/1.1.x/installation/)

## Test Driven Develop 
Typical of all our web apps, we'll use the TDD approach. It's really simple. Here's how we do Test Driven Development:

* Write a test. – The test will help flesh out some functionality in our app
* run the test – The test should fail, since there's no code(yet) to make it pass.
* Write the code – To make the test pass
* Run the test – If it passes, we are confident that the code we've written meets the test requirements
* Refactor code – Remove duplication, prune large objects and make the code more readable.
* Re-run the tests every time we refactor our code

Repeat – That's it!



1. Write a test: let's check out if the Flask is working as expected or not, the test file will be like: **tests/flaksInfr.py**

``` python
import unittest
import requests

testPageUrl = "http://localhost:8080/testPage"


class testWebBasic(unittest.TestCase):
    def test_flask_running(self):
        response = requests.get(testPageUrl)
        self.assertEqual(response.status_code, 200)
        self.assertIn('testPage', response.text)
        print(f"response:  {response.text}")
        self.assertIn('testPage', response.text)
```

2. run the test

``` bash
$ython -m unittest tests.flaskInfra
E
======================================================================
ERROR: test_flask_running (tests.flaskInfra.testWebBasic)
----------------------------------------------------------------------
Traceback (most recent call last):

(omitted)
```
This is expected, as we donot have any code written yet, let's get start with the very first code.

3. Write the code
File name is  **./app/run.py** 
``` python
from flask import Flask


# create and initialize a new Flask app
app = Flask(__name__)


@app.route("/testPage")
def home():
    return "testPage!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

in the terminal, run the code 
``` bash 
$# python ./app/run.py 
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)

```

4. Run the test

``` bash
python -m unittest tests.flaskInfra
.
----------------------------------------------------------------------
Ran 1 test in 0.008s

OK
```

5. Refactor code
    * manage.py
    * app/instance folder 
``` python
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Test environment."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
}
```

`Config`  is the parent class which has common settings, **test** **dev** and **prod** will take their settings accordingly with associated classes: `DevelopmentConfig`, `TestingConfig` and `ProductionConfig`.

./app/core/\_\_init__.py

``` python
# local import
from flask import Flask
from instance.config import app_config


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app
```

`instance_relative_config=True` tells the app that configuration files are relative to the instance folder. The instance folder is located outside the flaskr package and can hold local data that shouldn’t be committed to version control, such as configuration secrets and the database file.
More about [instance path](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders)

app/run.py will be used to lauch the flask application:
``` python
from core import create_app

config_name = 'dev'  
app = create_app(config_name)


@app.route("/testPage")
def testPage():
    return "testPage!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
```

6. run the test

```
 python -m unittest tests.flaskInfra
.
----------------------------------------------------------------------
Ran 1 test in 0.007s

OK
```
 
Until now, our Flask instance is up and running, we have kind of refactored the project layout a bit.
Before we connect our application with a DB, let's create a bassica RestFul API to handle GET, the reason I am doing this is without DB, I can easily use this code to build a docker image, test with AWS ECS, EKS or K8S etc, bare with me, I will get this part ASAP.

## RestFul API - GET

edit you test python file `tests/flaskinfra.py`

```
import unittest
import requests

HomePage = "http://localhost:8080/"


class testWebBasic(unittest.TestCase):
    def test_flask_running(self):
        response = requests.get(HomePage)
        self.assertEqual(response.status_code, 200)
        self.assertIn('HomePage', response.text)

    def test_first_get(self):
        response = requests.get(HomePage+"/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["title"], "Python is great")
        self.assertEqual(response.json()[1]["title"], "Flask is awsome")
        self.assertEqual(response.json()[2]["title"], "Django is the best")
```
Run the test

``` bash
python -m unittest tests.flaskInfra
F.
======================================================================
FAIL: test_first_get (tests.flaskInfra.testWebBasic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/wenluli/projects/flask/todo-api/tests/flaskInfra.py", line 16, in test_first_get
    self.assertEqual(response.status_code, 200)
AssertionError: 404 != 200

----------------------------------------------------------------------
Ran 2 tests in 0.011s

FAILED (failures=1)
```
app/run.py

```
from core import create_app
from flask import jsonify
config_name = 'dev'
app = create_app(config_name)

posts = [
    {
        "id": "12345678123456781234567812345678",
        "title": "Python is great",
        "body": "Python's convenience has made it the most popular language for machine learning and artificial intelligence. "
    },
    {
        "id": "d2841738-6f5b-4530-87d1-11349e27f29e",
        "title": "Flask is awsome",
        "body": "Flask is a micro web framework written in Python."
    },
    {
        "id": "216d8f22-4a66-434b-9efa-f6b5f1d4838d",
        "title": "Django is the best",
        "body": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. "
    }
]


@app.route("/")
def home():
    return "HomePage!"


@app.route("/posts")
def getPosts():
    return jsonify(posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

```

run the test again
``` bash
python -m unittest tests.flaskInfra
..
----------------------------------------------------------------------
Ran 2 tests in 0.011s

OK
```
## Docker file
*  Run the at localhost
``` bash
docker run -itd -p 8080:8080 REPLACE-AWS-ACCOUNT-ID.dkr.ecr.ap-southeast-2.amazonaws.com/REPLACE-project/flask:latest
```
* check out if the container is running as expected
``` bash
docker container ls
curl http://localhost:8080
curl http://localhost:8080/posts
```

##  Swagger/OpenAPI UI

[OpenAPI](https://www.openapis.org/)