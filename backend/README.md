# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API
### Base URL
`http://127.0.0.1:5000`
### Error
#### 404
```
{
  "success": False,
  "error": 404,
  "message": "Not found"
}
```
#### 422
```
{
  "success": False,
  "error": 422,
  "message": "Unprocessable entity"
}
```
### Endpoints
#### `GET` /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```
{
	'success': True,
	'categories': {
					'1' : "Science",
					'2' : "Art",
					'3' : "Geography",
					'4' : "History",
					'5' : "Entertainment",
					'6' : "Sports"
	}
}
```

#### `GET` /questions
- Fetches a dictionary of questions, total number of questions and categories
- Requst Arguments: None
- Returns: An Object with questions, total number of questions, current category and categories

```
{
	'succcess': True,
	'categories': {
					'1' : "Science",
					'2' : "Art",
					'3' : "Geography",
					'4' : "History",
					'5' : "Entertainment",
					'6' : "Sports"
	},
	'questions':  [{
					"answer": "Maya Angelou",
					"category": 4,
					"difficulty": 2,
					"id": 5,
					"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	}],
	'total_questions': 1,
	'currentCategory': None
}
```

#### `DELETE` /questions/{question_id}
- Delete one question
- Requst Arguments: question id is required
- Returns: An Object with deleted question id
```
{
    'success': True,
    'question_id': {question_id}
}
```

#### `POST` /questions
- Post new question
- Requst body: details of new question are required (question, answer, category, difficulty)
- Returns: success

```
{
    'success': True
}
```

#### `POST` /questions
- Search questions which contains the search term
- Requst body: search term
- Returns: an object with total number of questions, questions and current category
```
{
    'success': True,
    'questions': [{
					"answer": "Maya Angelou",
					"category": 4,
					"difficulty": 2,
					"id": 5,
					"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	}],
    'total_questions': 1,
    'current_category': 1
}
```

#### `GET` /categories/{category_id}/questions
- Fetch all questions based on the category
- Requst argument: category id
- Returns: an object with total number of questions, questions and current category
```
{
    'success': True,
    'questions': [{
					"answer": "Maya Angelou",
					"category": 4,
					"difficulty": 2,
					"id": 5,
					"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	}],
    'total_questions': 1,
    'current_category': 1
}
```

#### `POST` /quizzes
- Fetch a random question which is not the same with previous question
- Requst body: previous question id, category id
- Returns: question detail

```
{
    'success': True,
    'question': [{
					"answer": "Maya Angelou",
					"category": 4,
					"difficulty": 2,
					"id": 5,
					"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	}]
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
