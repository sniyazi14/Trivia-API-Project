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


## Endpoints

GET '/categories'
GET '/questions'
GET '/categories/<int>/questions'
DELETE '/questions/<int>'
POST '/questions/add'
POST '/questions/search'
POST '/quizzes'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
-Example request:
curl http://127.0.0.1:5000/categories
-Example response:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a dictionary of all questions in the database which contains each question, answer, id, category and difficulty which is paginated with 10 questions per page
- Also returns the categories similar to GET '/categories' endpoint
- Request Arguments: None
- Returns: An object with 5 keys, categories, that contains a object of id: category_string key:value pairs.
-curl http://127.0.0.1:5000/questions
"categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
},
"currentCategory": 1,
"questions": [
  {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  }
],
"success": true,
"totalQuestions": 18
}



GET '/categories/<int>/questions'
- Fetches a dictionary of questions similar to GET '/questions' but filtered according to specified category
- Request Arguments: Category ID (integer)
- Returns: The current category ID and list of questions with answer, category, id, question and difficulty keys.
- Example request: curl http://127.0.0.1:5000/categories/2/questions
- Example response:
  "currentCategory": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}

DELETE '/questions/<int>'
- Deletes a specific question from the database
- Request Arguments: id of question to be deleted (integer)
- Returns: all questions in similar format to GET '/questions'
- Example Request:
curl -X DELETE http://127.0.0.1:5000/questions/31
- Example response:
 "categories": {
   "1": "Science",
   "2": "Art",
   "3": "Geography",
   "4": "History",
   "5": "Entertainment",
   "6": "Sports"
 },
 "currentCategory": 1,
 "questions": [
   {
     "answer": "Tom Cruise",
     "category": 5,
     "difficulty": 4,
     "id": 4,
     "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
   },
   {
     "answer": "Maya Angelou",
     "category": 4,
     "difficulty": 2,
     "id": 5,
     "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
   },
   {
     "answer": "Edward Scissorhands",
     "category": 5,
     "difficulty": 3,
     "id": 6,
     "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
   },
   {
     "answer": "Muhammad Ali",
     "category": 4,
     "difficulty": 1,
     "id": 9,
     "question": "What boxer's original name is Cassius Clay?"
   },
   {
     "answer": "Brazil",
     "category": 6,
     "difficulty": 3,
     "id": 10,
     "question": "Which is the only team to play in every soccer World Cup tournament?"
   },
   {
     "answer": "Uruguay",
     "category": 6,
     "difficulty": 4,
     "id": 11,
     "question": "Which country won the first ever soccer World Cup in 1930?"
   },
   {
     "answer": "George Washington Carver",
     "category": 4,
     "difficulty": 2,
     "id": 12,
     "question": "Who invented Peanut Butter?"
   },
   {
     "answer": "Lake Victoria",
     "category": 3,
     "difficulty": 2,
     "id": 13,
     "question": "What is the largest lake in Africa?"
   },
   {
     "answer": "The Palace of Versailles",
     "category": 3,
     "difficulty": 3,
     "id": 14,
     "question": "In which royal palace would you find the Hall of Mirrors?"
   },
   {
     "answer": "Agra",
     "category": 3,
     "difficulty": 2,
     "id": 15,
     "question": "The Taj Mahal is located in which Indian city?"
   }
 ],
 "success": true,
 "totalQuestions": 26
}


POST '/questions/add'
- Creates new question in the database
- Request Arguments: new question parameters as json object: question(string), answer(string), difficulty(integer), category(string)
- Returns: success: result key value pair
-Example request:
curl -X POST -H "Content-Type: application/json" -d '{"question":"new question", "answer":"this", "difficulty":"1", "category":"1"}' http://127.0.0.1:5000/questions/add
- Example response:
{
  "success": true
}

POST '/questions/search'
-Performs case-insensitive search on questions table in database to find questions that contain given search term
- Request Arguments: search term (string)
- Returns: Response similar to '/questions' with only questions that contain specified search term as substring of the question
- Example request:
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}' http://127.0.0.1:5000/questions/search
- Example response:
  "currentCategory": 1,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}

POST '/quizzes'
- Fetches a question a new question that is in selected category and not one of previous questions
- Request Arguments: previous questions array and quiz category dictionary with type and id
- Return: single question JSON object
- Example request:
curl -d '{"previous_questions": [16],"quiz_category": {"type":"Art","id": "2"}}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/quizzes
- Example response:
{
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}


## Errors

-404: Resource Not Found
-422: Unprocessable Entity

Format example in JSON:
   {
    "success": False,
    "error": 422,
    "message": "Unprocessable entity"
    }

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
