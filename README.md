<p align="center">
  <a href="#" target="_blank" rel="noopener noreferrer">
    <img src="/backend/storage/assets/image/task.jpg" width="300">
  </a>
</p>
<!-- ![image info](./backend/storage/assets/image/task.jpg) -->

# Welcome to OA Platform

## Intall API server

1. Install redis

    `windows` https://dev.to/divshekhar/how-to-install-redis-on-windows-10-3e99  
    `macos`

        brew install redis 
    
    to run redis server
        
        redis-server

    open command line to test redis 

        redis-cli  
        127.0.0.1:6379> ping  
        > PONG (it worked)  

2. Clone package 

        git clone <source>   
        cd platform

3. Install package

        pip install -r requirements.txt
        
## Run development server 


1. Tạo file `backend/.env` cho config.py  (optional)

        DATABASE_HOSTNAME = localhost  
        DATABASE_CREDENTIALS = 'admin:12345678'  

2. Run webserver

        uvicorn backend.main:app --reload

3. Run celery worker 

        celery -A backend.proj worker  -l info -E  

     `proj` - folder chứa file celery config  
     `-l info` - option hiển thị log ở command line  
     `-A proj` - submodule named proj.celery (if not attribute named proj.celery or proj.app)


4. Run flower, đổi port --port=5555

        celery -A backend.proj flower --broker= --address=127.0.0.1 --port=5555 
 

## Open web page
Home page
http://localhost:8000

OpenAPI 
http://localhost:8000/docs

Realtime monitor worker
http://127.0.0.1:5555

## Usage

**Config DB**
- `/database/core.py`
- `/database/models.py` Models quan trọng của platform lưu tập trung
- `/database/revisions/` alembic folder about migration - <plan>

**Add new projects at**
- `/team_projects/`

**Add new features**
- `/backend`

**App structure**
- `views.py` - Routes  
- `service` - API Function  
- `database/models` -  Model / sql Object of Feature (models của riêng app)  
- `backend/schemas` - All schemas (data validation) here
- `backend/proj` - Default folder for Celery & Projects structure
- `backend/scheduler` - Config type of schedule here 

**Monolithic views**
- `/static` - for Style, javascript  
- `/templates/` - html views  
- `/main.py` - routes  

## Explaination 

**Notes**:

- Pydantic model (data validation) khác với sqlAlchemy model (class & intanstant interact with database)
- Pydantic model trong schemas.py, SQLAlchemy model trong models.py của từng Feature/Project
- Mỗi tính năng sẽ có model/database.py riêng, DB chung ở database/core.py    
- `#database/core.py`  Create SQLAlchemy models from the `Base` class and import to  models.py of each Project  
- `orm_mode = True` - Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict  
- `SessionLocal` - instant class of database session  
- `Session` from  `sqlalchemy.orm` - The session is an SQLAlchemy object used to communicate with SQLite in the Python example programs
- `Alembic` module - initialize your database (create tables, etc) & migrations

- Flow: Add job schedule, đến thời điểm triggle (`cron`, `interval`) sẽ vào hàng đợi của Celery
- Mỗi lần thay đổi logic ở `@task` của celery phải reset lại worker
- Không cần phải restart server khi hẹn giờ cho task
## References
**Package** 

fastapi - web framework  
https://fastapi.tiangolo.com/tutorial/first-steps/  
https://fastapi.tiangolo.com/tutorial/sql-databases/

sqlAchemy  
https://docs.sqlalchemy.org/en/14/dialects/mysql.html
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#what-does-the-session-do  
https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference

Python scheduler
https://apscheduler.readthedocs.io/en/stable/

celery redis flower - task queue  
https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps  

alembic - Database migration (optional)
https://alembic.sqlalchemy.org/en/latest/

plotly - chart  
https://plotly.com/javascript/  

websocket/server sent event   
(plan to send log messages to client)  
