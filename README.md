# Sellit app

### What is it?
---------------
This is a modular app intended to post items for sale based on location allowing  
secure image upload if a non production setting, comments between two people,  
posting by category and location.  

### What do i need to run it?
---------------
* Python 2.7 - https://www.python.org/
* You will need a virtual server:
  * virtualbox - https://www.virtualbox.org/
  * vangrant - https://www.vagrantup.com
  * note: this is not 100% necessary but recommended you can run: python runserver.py
* Your favorite command-line tool - https://www.gnu.org/software/bash/bash.html
* latest version of pip (python installation package)
    * can update in CommandLine with: pip install --upgrade pip
* Flask - http://flask.pocoo.org/
* Flask_uploads - can download using command line with: pip install Flask-Uploads
* a web browser - https://www.google.com/chrome/

### What is being utilized?
---------------
* HTML/CSS/JavaScript
* Python
* Flask framework
    * Flask-uploads
    * flask Blueprints
* Jinja2 templating
* sqlalchemy database
* Vagrant VM
* Virtualbox
* a third party authorization and authentication

### How do i run it?
---------------
Once everything is installed just move to directory in command line and  
python runserver.py  
the database will be made automatically as well as any additional folders.
Note: If you are in a virtual server you will need to install necessary components.

### Where is it available?
---------------
* https://github.com/vondirath/UD---sellit

### License
---------------
Available at https://github.com/vondirath/UD---sellit/blob/master/LICENSE
