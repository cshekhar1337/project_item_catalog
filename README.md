# project_item_catalog

## About the project
Item Catalog. [ Developed using Django, deployed on gcloud ]

Registration for new user and login module for registered users

Mantains sessions of logged in user [which uses cookie in the background]

Password hashed using salt and PBKDF2 algorithm

If user has not created the post then he will not see the link to edit

FBlogin for oauth based authentication


## Steps for installation on local system
1. "git clone https://github.com/cshekhar1337/project_item_catalog.git"
2. go to the folder and "cd project_item_catalog/"
3. modify in settings.py Databases config according to the system and start your system mysql server
4. run this command on terminal python manage.py runserver


