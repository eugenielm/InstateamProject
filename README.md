InstateamProject
=================

Small project containing an app called 'instateam', which is a team-member management application that allows the user to view, edit, add, and delete team members.

The backend is implemented with the Django web framework, the frontend with HTML/CSS. It's using Django's default sqlite3 database.

The root path is redirected to the team-members list page /teammembers.

The project was tested locally with Python 3.7.2.


How it works
------------

1. Make sure you have Python 3+ installed on your computer (it may or may not work with Python versions older than 3.7.2) and pip

2. Fork this repo, and from your terminal go to the InstateamProject/ directory
```sh
cd ~/path/to/InstateamProject/
```

3. Install the dependencies by running the command below (you might want to create a virtual environment before running it):
```sh
pip install requirements.txt
```

4. Launch the dev server (if no port number is specified, it will run on port 8000 by default)
```sh
python manage.py runserver [port_number]
```

5. Load 'localhost:8000' in your web browser, et voilà!


To run the tests
----------------

1. go to ~/path/to/InstateamProject/

2. Then run:
```sh
python manage.py test
```


To be improved
--------------

- change database: sqlite3 is not suitable for production
- allow unicode characters in the team members' first and last names
- allow more flexibility in the phone number formats (currently only the 111-222-3333 format is allowed)
- write more thorough tests (e.g. use Selenium and a web driver to test the templates)
- create nice error403, error404, and Error500 pages/templates to avoid landing on the ugly default ones ;)


More info about the Django web framework here:
https://www.djangoproject.com/start/
https://docs.djangoproject.com/en/2.2/