# **PyGram** Social Network

<p>PyGram is a social network that developed with python.
here are the main features of this project:
</p>

1. Home Page
2. Sign Up and Login (and account verification)
3. User Profile (dashboard)
4. Direct messages
5. Chat with others
6. Search users and pages
7. Users single page
8. Sharing new post and delete post
9. Followers and Following pages
10. Like and Comment on posts


# Getting Started

- [Project Structure](#Project-Structure)
- [Dependencies](#Dependencies)
- [Requirements](#Requirements)
- [Site Routes](#Site-Routes)
- [Project Modules](#BluePrints)
- [Data Base Diagram](#Database-Diagram)
- [About redis](#Redis)
- [About sqlalchemy](#SqlAlchemy)
- [About flask-migration](#Flask-Migration)
- [View site pages](#Site-Pages)


# Project-Structure
```bash
PyGram
├───app.py
├───requirements.txt
├───dependencies.txt
├───routes.txt
├───README.md
├───.env
├───.gitignore
├───Documentation
├───migrations
└───PyGram
    ├───__init__.py
    ├───controller.py
    ├───models.py
    ├───config.py
    ├───mod_direct_message
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_follow
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_post
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_profile
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_search
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_setting
    │   ├───__init__.py
    │   └───controller.py
    ├───mod_user_page
    │   ├───__init__.py
    │   └───controller.py
    ├───static
    │   ├───Site-Screen
    │   ├───img
    │   ├───styles
    │   │    └───all of css files..
    │   └───upload
    │       ├───dir_of_user1
    │       ├───dir_of_user2
    │       └───dir_of_user3
    ├───Templates
    │   └───all of html files..
    └───utils
        ├───check_auth.py
        ├───registration.py
        └───upload.py
```


# Dependencies

|   Modules                 | Description                                                     
|---------------------------|-----------------------------------------------
| flask                     | web framework
| python-dotenv             | for read dotenv files
| flask-sqlalchemy          | ORM
| mysqlclient or pymysql    | mysql connector
| flask-migrate             | database migration 
| flask-jwt-extended        | for Authorization (access and refreshh token)
| flask-mail                | for sending email
| redis                     | we use this nosql database for saving users registration token
| flask_whooshalchemy       | search engine


# Requirements

```python
>> pip freeze
alembic==1.4.2
blinker==1.4
click==7.1.2
Flask==1.1.2
Flask-Autodoc==0.1.2
Flask-JWT-Extended==3.24.1
Flask-Mail==0.9.1
Flask-Migrate==2.5.3
Flask-Selfdoc==1.2.3
Flask-SQLAlchemy==2.4.1
itsdangerous==1.1.0
Jinja2==2.11.2
Mako==1.1.2
MarkupSafe==1.1.1
PyJWT==1.7.1
PyMySQL==0.9.3
python-dateutil==2.8.1
python-dotenv==0.13.0
python-editor==1.0.4
redis==3.4.1
six==1.14.0
SQLAlchemy==1.3.16
Werkzeug==1.0.1
Whoosh==2.7.4
```


# Site-Routes
| Endpoint                  | Methods   |  Rule                                       
|---------------------------|-----------|---------------------------------------------
|direct.chat                | GET       | /direct/chat/<string:username>               
|direct.direct_index        | GET       | /direct/<string:username>                       
|direct.send_message        | POST      | /direct/send_message/<string:username>        
|follow.follow_index        | GET       | /follow/<string:username>
|index                      | GET       | /
|login                      | GET, POST | /login/
|post.comment               | POST      | /post/comment/<string:username>/<string:date>
|post.delete_post           | GET       | /post/delete/<string:username>/<string:date>
|post.like                  | GET       | /post/like/<string:username>/<string:date>
|post.new_post              | GET, POST | /post/new/<string:username>
|post.post_index            | GET       | /post/<string:username>
|post.single_post           | GET       | /post/single/<string:username>/<string:date>
|profile.logout             | GET       | /profile/logout/
|profile.profile_index      | GET       | /profile/<string:username>
|search.search              | GET       | /search/search/
|setting.setting_index      | GET, POST | /setting/<string:username>
|signup                     | GET, POST | /signup/
|signup_process             | GET       | /signup-process/
|static                     | GET       | /static/<path:filename>
|user_page.follow_process   | GET       | /user_page/follow-process/<string:username>/
|user_page.unfollow_process | GET       | /user_page/unfollow-process/<string:username>/
|user_page.user_page_index  | GET       | /user_page/<string:username>


# BluePrints
- mod_direct_message
- mod_follow
- mod_post
- mod_profile
- mod_search
- mod_setting
- mod_user_page


# Database-Diagram
![Database Models Diagram](Documentation/PyGramDB.png)


# Redis

Redis => [Key Value DataBse] your data have a key for example => mtaghizadeh_register : 12345 [mtaghizadeh_register is username and mode is register and token is 12345]

- download redis :
https://github.com/antirez/redis/issues/6276

- Check Redis Connection:
1. in cmd(admin) 
```python 
>>> redis-cli
>>> ping
>>> pong
```
2. in services

- install redis in python or venv
```python
>>> pip install redis
```

- add redis key in flask config (.env)
```python
>> REDIS_SERVER_URL=redis://127.0.0.1:6379 # redis default port
```

- import redis in app.py:
```python
>> from redis import Redis
>> redis = Redis.from_url(app.config['REDIS_SERVER_URL'])
```

- test in flask sell:
```python
>>> from app import redis 
>>> redis.ping()
>>> True # if connection is ok.
```

- redis add:
```python
>> redis.set(key, value, expiry_date(s))
```

- redis get value by key:
```python
>> redis.get(name=key)
>>> GET mtaghizadeh_register # (in redis-cli)
```

- redis delete:
```python
>> redis.delete(key)
```


# SQLAlchemy
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

Documentation: https://www.sqlalchemy.org/

- for using SqlAlchemy ORM in flask we should install extension of "flask-sqlalchemy"
```python
>>> pip install flask-sqlalchemy
```

- mysql-connector:
```python
>>> pip install pymysql
or
>>> pip install mysql-client
```

- create models in flask shell:
```python
>>> from app import db
>>> create_all()
```

- create models with flask-migration
```python
>>> flask db init
>>> flask db migrate
>>> flask db upgrade or downgrade
```

- create class as a entity(table) of database
```python
class User(db.Model):
    __tablename__ = "users"

    name = Column(String(32), nullable = False)
    lastname = Column(String(32), nullable = False)
    email = Column(String(256), nullable = False)
    username = Column(String(64), primary_key = True)
    country = Column(String(32), nullable = False)
    password = Column(String(128), nullable = False)
    avatar = Column(String(256), nullable = False, default = "/static/upload/avatar.png")
    active = Column(Boolean, nullable = False, default = False)

    # One To Many:
    # list of posts for create a foreign key we use backreference to list of this mode(Parent) from another model 
    posts = relationship("Post", backref="user")
    
    # and other list for anothers classes
class Post(db.Model):
    __tablename__ = "posts"
    username = Column(String(64), ForeignKey('users.username'), primary_key = True) # Foreign Key is primary key of parent table
    caption = Column(Text(), nullable = True)
    picture = Column(String(256), nullable = False)
    post_date = Column(DateTime(), default = dt.datetime.utcnow, primary_key = True)
```


- select * from table
```python
user = User.query.all()
```

- select from table where 
```python
user = User.query.filter_by(username="mtaghizadeh").first()
or
user = User.query.filter(User.username="mtaghizadeh").first()
```

- delete from table where 
```python
post = Post.query.filter_by(username=username, post_date=date).first()
db.session.delete(post)
db.session.commit()
```

- add or update table
```python
# add user to database:
user = User()
user.name = name
user.lastname = lastname
user.email = email
user.username = username
user.country = country
user.password = password
db.session.add(user)
db.session.commit()
```

- Pagination in sql alchemy and sql or command 
```python
from sqlalchemy import or_ ### by default is and
q = request.args.get("q")
name_cnd = User.name.ilike(f'%{q}%')
lastname_cnd = User.lastname.ilike(f'%{q}%')
username_cnd = User.username.ilike(f'%{q}%')
### using or_ SQLAlchemy : by default is and
# before pagination
# found_users = User.query.filter(or_(
#     name_cnd,
#     lastname_cnd,
#     username_cnd
# )).all()
# pagination
p = request.args.get("p", default=1, type=int)
found_users = User.query.filter(or_(
    name_cnd,
    lastname_cnd,
    username_cnd
)).paginate(p, 5)
```

- join in tables
```python 
# Join Follow and post for get post of followers of this user 
following_cnd = Follow.query.filter_by(follower_username = username).all()
query = db.session.query(
    Follow,
    Post
).filter(
    Follow.follower_username == user.username
).filter(
    Follow.following_username == Post.username
).order_by(Post.post_date.desc()).all()
```


# Flask-Migration

for simple altering in database (tracking all of database changes) :)))
```python 
>> pip install flask-migrate 
>> flask db init ---> create migration folder (just in starting project)
# then by default create migration directory of your project and create alembic table in your database
```

### if you have any change in your model:

```python
>>> flask db migrate # alter your db if you change it...
>> flask db upgrade  # commit the changes(upgrade)
>> flask db downgrade
```


# Site-Pages

### Index Page 
home page of site that contains login and signup functionality
![Database Models Diagram](Documentation/Site-Pages/1-index.png)


### Signup Page 
User can register in this page 
![Database Models Diagram](Documentation/Site-Pages/2-signup.png)

- signup process completed

![Database Models Diagram](Documentation/Site-Pages/3-signup.png)

- user active filed in database is Flase(0) before activation

![Database Models Diagram](Documentation/Site-Pages/4-signup.png)

- we create random token between [00000 , 99999] and save that in redis database 

![Database Models Diagram](Documentation/Site-Pages/5-signup.png)

- after registeration we send an email to user email account with **flask-mail** 
that contains a link like this: 
http://127.0.0.1:5000/signup-process/?username=mtaghizadeh&token=266781

![Database Models Diagram](Documentation/Site-Pages/6-signup.png)

- after activtivation we delete token from redis database

![Database Models Diagram](Documentation/Site-Pages/7-signup.png)

- after activtivation we create directory(with user.username) for upload user avatr and post.pictures

![Database Models Diagram](Documentation/Site-Pages/8-signup.png)


### Login
user can login to pygram 
- user should be activate

![Database Models Diagram](Documentation/Site-Pages/9-login.png)


### Setting Page 
user can change profile picture in this page
- user can **upload** any image for changing profile avatar 

![Database Models Diagram](Documentation/Site-Pages/10-setting.png)


### User Posts Page 

user can share new post in this page and see all of posts published nad manage that (delete or modify)
- in first time this page like this 

![Database Models Diagram](Documentation/Site-Pages/11-post.png)

- after sharing posts 

![Database Models Diagram](Documentation/Site-Pages/12-post.png)

- user can sharing post with picture and caption

![Database Models Diagram](Documentation/Site-Pages/13-new-post.png)

- user can choose any image from his computeer

![Database Models Diagram](Documentation/Site-Pages/14-new-post.png)

- after sharing post, upload post picture in user directory in server and path of file save in database (Post Table)
- any file upload in sever with random name from uuid library
![Database Models Diagram](Documentation/Site-Pages/15-new-post.png)


### Search Page 
user can search any user in this page 
- we paginate all result with **SQLAlchemy paginate() method**

![Database Models Diagram](Documentation/Site-Pages/16-search.png)


### Single User Page 
- after searching user or click on user page link user can see page of single user

![Database Models Diagram](Documentation/Site-Pages/17-single_user_page.png)

- user can follow or unfollow and send direct message to single user

![Database Models Diagram](Documentation/Site-Pages/18-single_user_page.png)


### Single User Post
- all of information of this single post 
- user can **like and comment** this post

![Database Models Diagram](Documentation/Site-Pages/19-single-post.png)


### Follower and Following Page
- in this page user can see all of his followers and following  
- user can click any user and redirect to single user page

![Database Models Diagram](Documentation/Site-Pages/20-follower-following.png)


# Single Direct Message Page(Chat Page)
- user can send message to another user and see message order by sending date

![Database Models Diagram](Documentation/Site-Pages/21-single-direct-message.png)


### User Profile Page
- in this page user can see all of posts that sharing with his following 
- user can like that and can send comment to this post

![Database Models Diagram](Documentation/Site-Pages/22-profile.png)

