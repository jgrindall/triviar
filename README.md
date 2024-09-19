# API Development and Documentation Final Project - Triviar


## Introduction

A completed quiz API with simple React front end.

Functionality includes:

1. Display all questions.
2. Display questions by category.
3. Show difficulty ratings.
4. Show/hide the answer
5. Delete a question.
6. Add questions and validate them (eg. they have an answer and a difficulty)
7. Search for questions based on a text query string.
8. Play the quiz game, randomizing either all questions or within a specific category.


## Back end

### Installing dependencies

The important dependencies are:

- [Flask](http://flask.pocoo.org/)

- [SQLAlchemy](https://www.sqlalchemy.org/)

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)

To install the dependencies, ensure you have python 3.7+ installed and run

```
$ pip install -r requirements.txt
```

from inside the backend directory



### Set up the Database

Ensure you have postgres 4.x installed.

Find the setup.sh script in the backend directory.

Change these lines to match your user and password:

```
export PGUSER=postgres
export PGPASSWORD=thisismypassword
```

Run

```
$  ./setup.sh
```

This will drop any database you already have called "trivia", make a new one and import the test data


### Run the Server

1. cd backend
2. Run ./run.sh

This will set appropriate environment variables and run "python -m flask run -p 5000"



## Front end

The frontend app is built using create-react-app.

1. install nodejs [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. install front end dependencies

cd frontend

npm i

npm run start

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.


## Testing

1. cd backend

2. ./test.sh

This will drop any database you already have called "trivia_test", make a new one and import the test data
Then it will run "python -m test_flaskr"


## API Documentation

### Questions
### Categories
### Quiz


`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```






> Only read the below to confirm your notes regarding the expected API endpoint behavior based on reading the frontend codebase.

### Expected endpoints and behaviors

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```



$ flake8 ./
$ flake8 --max-line-length 128 ./
