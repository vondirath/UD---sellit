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
  * vangrant - https://www.vagrantup.com
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

### License
---------------
Available at https://github.com/vondirath/UD---sellit/blob/master/LICENSE
