## Setup Instructions:

To setup, clone the repository with `git clone https://github.com/ezl/wodeveryday.com.git` then follow the backend setup instructions and then the frontend setup instructions



### Backend
- Copy the `.env` file into the `back` folder in the repository. If you need this, ask Eric.
- Create a postgres db, user, and give the user permissions to access it. Something like:
```
createdb wodeveryday_db
psql wodeveryday_db
CREATE USER wodeveryday_user WITH PASSWORD 'wodeveryday_password';
GRANT ALL ON DATABASE wodeveryday_db TO wodeveryday_user;
```
- Update the `.env` file to reflect the `DB_NAME`, `DB_USER`, `DB_PASSWORD`, etc to reflect the db user/password etc you created
- Create a `local_settings.py` file in the `back` folder and add in this script 
```
DEBUG = True
ALLOWED_HOSTS = []
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
)
```
- Open the `back` folder in the command line

Requirements - use python 3.7+
Create a virtual env (something like virtualenv `env_name` or however you want to do it)
- Enter that virtual env
- pip install requirements.txt into that virtualenv (`pip install -r requirements.txt`)
- run `python manage.py migrate`
- run `python manage.py loaddata fixtures` As Eric if you need the `fixtures.yaml` file.
- Then from the same folder run the command `python manage.py runserver 127.0.0.1:8000`
- This should start the development server so that it can be accessed by the frontend, which you'll build and run in the next step.



### Frontend
- Copy the .env file into the `front` folder in the repository
- Open the `front` folder in the command line
- Ensure that you have yarn installed `yarn --version`
- From that folder run `yarn install` and then  `yarn dev`
- This should start up the website at `http://localhost:3000/`

---

## Deployment Instructions:
- Open up the console and ssh into the server with your username and the address `_______@3.86.178.26`
- After you enter in your passphrase type in `cd /opt/webapps/wodeveryday.com` to navigate to the application `root folder`

## Backend
- To redeploy the backend navigate to its folder from the `root folder` with `cd back`
- To trigger the redeploy simply type `sudo supervisorctl restart be`
- To modify the `.env` file type `vim .env`

## Frontend
- To redeploy the frontend drill drown to it from the `root folder` with `cd front`
- Rebuild the application with `yarn build`
- Once that finishes successfully type in `sudo supervisorctl restart fe` to redeploy
- To modify the `.env` file type `vim .env.save`
