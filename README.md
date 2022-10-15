## Online Polls And Surveys
![test status](https://github.com/Tanabodee-Yambangyang/ku-polls/actions/workflows/test.yml/badge.svg)

An application for conducting online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

### How to Install

* Clone this repository to your device.
``` 
git clone https://github.com/Tanabodee-Yambangyang/ku-polls.git
```
* Change the directory to `ku-polls`
```
cd ku-polls
```
* Install app dependencies in a virtual environment.

  1. Create the virtual env in "env/"
  
  ```
  python -m venv env 
  ```
  
  2. Start the virtual env in bash or zsh
  
  - For **Mac/Linux**
  ```
  . env/bin/activate
  ```
  
  - For **Window**
  ```
  . .\env\Scripts\activate
  ```
  
* Install all packages on requirements.txt.
``` 
python -m pip install -r requirements.txt
``` 

* Externalize configuration data
 
  1.Create `.env` file inside `ku-polls` directory. 
  
  2.Copy everything in `sample.env` and put it in `.env`.
  
  3.In `.env` replace **secret-key-value-without-quotes** with your secret key.
  
* Importing data from a file

  1. Create a new database by running migrations.
  ```
  python manage.py migrate
  ```
  
  2. Import data using **“loaddata”**.
  ```
  python manage.py loaddata data/polls.json data/users.json
  ```
  
### How to Run

* Run the server by typing this command.
``` 
python manage.py runserver
``` 
* Then access this URL in your browser.
``` 
http://127.0.0.1:8000/
``` 

**Now you can access KU polls and start voting!!!**

To exit the virtualenv, type `deactivate`, or close the terminal window.

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Development%20Plan)
- [Project Backlog](https://github.com/users/Tanabodee-Yambangyang/projects/4/views/1)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Project Task Board](https://github.com/users/Tanabodee-Yambangyang/projects/4/views/2?filterQuery=iteration%3A%22Iteration+1%22)
- [Iteration 2 Plan](https://github.com/Tanabodee-Yambangyang/ku-polls/wiki/Iteration-2-Plan) and [Project Task Board](https://github.com/users/Tanabodee-Yambangyang/projects/4/views/3)
- [Iteration 3 Plan](https://github.com/Tanabodee-Yambangyang/ku-polls/wiki/Iteration-3-Plan) and [Project Task Board](https://github.com/users/Tanabodee-Yambangyang/projects/4/views/4)

[django-tutorial]: https://www.djangoproject.com/

## Demo users 

Demo users used to test the application.
| Username  | Password  |
|-----------|-----------|
|   harry   | hackme22  |
|   john    | johny22   |

## Admin

Admin user for the application
| Username  |   Password   |
|-----------|--------------|
| tanabodee |  title252545 |
