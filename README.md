# Sellit app

### What is it?
---------------
This is a modular app intended to post items for sale allowing  
secure image upload and store creation with
third party authentication and authorization. 

### What do i need to run it?
---------------
* Python 2.7 - https://www.python.org/
* You will need a virtual server:
  * virtualbox - https://www.virtualbox.org/
  * vagrant - https://www.vagrantup.com
* Your favorite command-line tool - https://www.gnu.org/software/bash/bash.html
* latest version of pip (python installation package)
    * can update in CommandLine with: pip install --upgrade pip
* Flask - http://flask.pocoo.org/
* Flask_uploads - can download using command line with: 
    * pip install Flask-Uploads
* a web browser - https://www.google.com/chrome/
* you need a google Client ID and Client Secret and put the clientID into the login.html template.
** ( if its a temporary key it'll last about an hour )
* you need to download the JSON credentials (for offline) and put it in the top app folder. 

### What is being utilized?
---------------
* HTML/CSS/JavaScript
* Python
* Flask framework
    * Flask-uploads
    * flask Blueprints
    * flask-login
    * requests(apache style)
* oauth2client for third party auth (google+, facebook)
* Jinja2 templating
* sqlalchemy database
* Vagrant VM
* Virtualbox

### How do i run it?
---------------
Once everything is installed just move to directory in command line and  
* python runserver.py  
the database will be made automatically as well as any additional folders.
Note: If you are in a virtual server you will need to install necessary components.

### Where is it available?
---------------
* https://github.com/vondirath/UD---sellit

### Production Updates.
---------------
It is not recommended to use sqlite as what this is uploaded with. It is fairly easy to get postgresql running for example.
install 
* libpq-dev. https://pypi.python.org/pypi/libpq-dev/9.0.0
* postgresql, https://www.postgresql.org/
* postgresql-contrib, https://www.postgresql.org/
* psycopg2, http://initd.org/psycopg/
This will let you set up sql in your environment.
for more info on how: 
* https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
* http://killtheyak.com/use-postgresql-with-django-flask/

the only thing i changed in the files were where the engine is defined and created in the database __init__.py and the auth and posts views.py. it looked like: engine = create_engine('postgresql://catalog:Password@localhost/catalog') and the password is your database user when created in psql.
more info on the user setup.
* http://superuser.com/questions/769749/creating-user-with-password-or-changing-password-doesnt-work-in-postgresql

it is recommended to use a virtual environment to keep dependencies required by different projects in seperate places and keeps the global package clean and manageable. 
for installation and running:
* http://docs.python-guide.org/en/latest/dev/virtualenvs/

To get the facebook and google+ logins working in your own environment you need to set up your app with your public ip-address and Host name. see the developers sites for more info. 
* https://console.developers.google.com/iam-admin/projects
* https://developers.facebook.com/apps/

You also need to define where and how you are getting your JSON info for your app's. these are located in the views.py in auth. 

to get flask uploads to work you need to define the OS's absolute location and make sure it is allowed to write.
this is in the __init__.py file in sellit as the default relative location will not work correctly in all 
systems (you can do this howver you want, i included a BASE_DIR helper in the helpers file).

### License
---------------
Available at https://github.com/vondirath/UD---sellit/blob/master/LICENSE
