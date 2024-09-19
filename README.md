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
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [psycopg2](https://pypi.org/project/psycopg2/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)

To install the dependencies, ensure you have python 3.7+ installed and run

```
$ pip install -r requirements.txt
```

from inside the backend directory


### Setting up secrets

Create a .env file in the backend directory with the contents:

```
PGPASSWORD=<your password>
PGUSER=postgres
```

If your user is not called "postgres" you will need to edit the trivia.psql file (see below)

### Set up the Database

Ensure you have postgres 4.x installed with the above user and password.

Run

```
$ ./setup.sh
```

This will drop any database you already have called "trivia", make a new one and import the test data from the trivia.psql file.



### Run the server

Run 

```
$ ./run.sh
```

This will set appropriate environment variables and execute "python -m flask run -p 5000", running the backend API server on port 5000.



### Code quality

Run flake8 from the backend directory.

```
$ flake8 --max-line-length 128 ./
```



### Testing

Run

```
$ ./test.sh
```

From the backend folder.

This will drop any database you already have called "trivia_test", make a new one and import the test data.

Then it will run "python -m test_flaskr" and run all tests in that file.




## Front end

The frontend app is built using create-react-app.


1. Install nodejs [https://nodejs.com/en/download](https://nodejs.org/en/download/).

The project has been tested on node v16.20.2

2. Install front end dependencies

```
$ npm i
$ npm run start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.





# API Documentation

## Questions

### GET /questions

- Fetches all questions 
- Example ```curl -X GET "http://localhost:5000/questions"```
- Returns
  - available categories
  - list of questions
  - success: boolean
  - total_questions: number

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    ...
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 26
}
```

----

### GET /questions?page=i

- Fetches all questions - paginated
- Request parameter 'i' must be an integer
- Example ```curl -X GET "http://localhost:5000/questions?page=2"```
- Returns
  - available categories
  - list of questions in that page (max 10)
  - success: boolean
  - total_questions: number

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    ...
  },
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },

    ...
  ],
  "success": true,
  "total_questions": 26
}
```


----

### DELETE /questions/id

- Delete a question
- Example ```curl -X DELETE "http://localhost:5000/questions/1"```
- Returns
  - success: boolean
  

```
{
  "success": true,
}
```

- Possible error codes:

  - 404 - if the specified question was not found

```

curl -X DELETE "http://localhost:5000/questions/1000000"

{
  "error": 404,
  "message": "Resource not found",
  "success": false
}

```



----



### POST  /questions

- Create a question
- Example
```
curl -X POST "http://localhost:5000/questions" -H "Content-Type: application/json" -d '{
    "question": "What is the capital of France?",
    "answer": "Paris",
    "category": 1,
    "difficulty": 2
}'

```
- Returns
  - success: boolean
  - question_id - the id that was created
  

```
{
  "question_id": 31,
  "success": true
}
```


- Possible error codes:

  - 422 - if the specified question was not valid (eg. answer missing, category does not exist, difficulty not specified in the range 1-5)

```

curl -X POST "http://localhost:5000/questions" -H "Content-Type: application/json" -d '{
    "question": "What is the capital of France?",
    "category": 1,
    "difficulty": -1
}'
```

```
{
   "error": 422,
   "message": "Badly formatted request",
   "success": false

}

```

----


### POST /questions/search

- Search for matching questions

- POST body contains:
    - searchTerm (string)

- Performs case insensitive search across all questions. Does not support pagination.

```
curl -X POST "http://localhost:5000/questions/search" -H "Content-Type: application/json" -d '{
    "searchTerm": "capital"
}'
```
- Returns:
  - success boolean
  - questions - a list of matching questions

```
"questions": [
    {
      "answer": "Paris",
      "category": 1,
      "difficulty": 2,
      "id": 31,
      "question": "What is the capital of France?"
    }
    ... etc
  ],
  "success": true

```



- Possible error codes:

  - 422 - if the specified searchTerm was not valid

```
curl -X POST "http://localhost:5000/questions/search" -H "Content-Type: application/json" -d '{
    "search_term": ""
}'
```

```
{
   "error": 422,
   "message": "Badly formatted request",
   "success": false

}

```




## Categories



### GET /categories

- Get all categories

Example


```
curl -X GET "http://localhost:5000/categories"
```
Returns
- success boolean
- categories, in the form {id, name}

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

----


### GET /categories/id/questions



- Get questions in the specified category
- Example:


```
curl -X GET "http://localhost:5000/categories/2/questions"
```

Returns

- success boolean
- a list of questions in the specified category


```
{
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    ...etc
  ],
  "success": true
}

```




- Possible error codes:

  - 404 - if the specified category does not exist

```
curl -X GET "http://localhost:5000/categories/100000/questions"
```

```
{
    "error": 404,
    "message": "Resource not found",
    "success": false
}

```



## Quiz


### POST /quiz

- Generate the next (random) question in a quiz
- POST body contains:
   - previous_questions - int[] - an array of question ids that have been answered already (to avoid returning one you have already done) (optional)
   - quiz_category_id - what category do you want to use (optional)

- If previous_questions is missing then any question will be returned 
- If quiz_category_id is missing then any category could be chosen

Example:


```
curl -X POST "http://localhost:5000/quiz" -H "Content-Type: application/json" -d '{
    "previous_questions": [2, 5],
    "quiz_category_id": 1
}'

```
- Returns:
  - success boolean
  - question - the next question generated, or null if none was found

```
{
  "question": {
    "answer": "Paris",
    "category": 1,
    "difficulty": 2,
    "id": 31,
    "question": "What is the capital of France?"
  },
  "success": true
}

or

{
  "question": null,
  "success": true
}

```

## Other errors

### 405

Example:

```
curl -X DELETE "http://localhost:5000/quiz"
```

```
{
  "success": False,
  "error": 405,
  "message": "Method Not Allowed"
}
```



### 500

Example:

Triggered by unhandled exceptions or server-side failures.

```
{
  "success": False,
  "error": 500,
  "message": "Server error"
}
```

