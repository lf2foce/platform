## Intall API server

### install python3.7+, redis
(windows) https://dev.to/divshekhar/how-to-install-redis-on-windows-10-3e99  
(macos) 
> brew install redis 
#### run redis
> redis-server
#### test redis
open command line:   
> redis-cli  
> 127.0.0.1:6379> ping  
>> PONG (it worked)  

### Clone package 
> git clone <source>   
> cd backend  

### install package
> pip install -r requirements.txt

### run development server
#### tạo file <.env> cho config.py  (optional)
DATABASE_HOSTNAME = localhost  
DATABASE_CREDENTIALS = 'admin:12345678'  

#### run webserver
> uvicorn main:app --reload

#### run celery worker 
> celery -A proj worker  -l info

Note:   
"proj" - folder chứa file celery config  
"-l info" - option hiển thị log ở command line  

#### run flower, đổi port --port=5555
> celery -A proj flower --address=127.0.0.1  

## Open web page
### Home page
http://localhost:8000

### realtime monitor worker
http://127.0.0.1:5555

## Usage
### Notes
Chú ý Pydantic model khác với sqlAlchemy model  
Mỗi tính năng sẽ có model/database riêng, DB chung ở database/core.py   
### Config DB 
/database/core.py

### Add new project at
/team_projects/

### Add new features
/backend
#### App structure
views.py - Routes  
service - API Function  
models -  Model / sql Object of Feature (notification, auth, report)  

### Monolithic views
/static - for Style, javascript  
/templates/ - html views  
/main.py - routes  

### Package
fastapi - web framework  
https://fastapi.tiangolo.com/tutorial/first-steps/  

sqlAchemy  
https://fastapi.tiangolo.com/tutorial/sql-databases/  

celery redis flower - task queue  
https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps  

plotly - chart  
https://plotly.com/javascript/  

websocket/server sent event   
(plan to send log messages to client)  
