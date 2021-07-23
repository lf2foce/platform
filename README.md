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

        cd backend

1. Tạo file `.env` cho config.py  (optional)

        DATABASE_HOSTNAME = localhost  
        DATABASE_CREDENTIALS = 'admin:12345678'  

2. Run webserver

        uvicorn main:app --reload

3. Run celery worker 

        celery -A proj worker  -l info  

     `proj` - folder chứa file celery config  
     `-l info` - option hiển thị log ở command line  
     `-A proj` - submodule named proj.celery (if not attribute named proj.celery or proj.app)


4. Run flower, đổi port --port=5555

        celery -A proj flower --address=127.0.0.1  

5. To start the celery beat service (optional):

        celery -A proj beat

    `-s /path/to/celerybeat-schedule` - option đổi tên db schedule    

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
- `models` -  Model / sql Object of Feature (models của riêng app)  
- `backend/schemas.py` & `backend/models.py` - shared model of whole platform  
- `backend/proj` - Default folder for Celery  

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
- `Session` from  `sqlalchemy.orm` - declare the type of the db parameters  
- `Alembic` module - initialize your database (create tables, etc) & migrations
## References
**Package** 

fastapi - web framework  
https://fastapi.tiangolo.com/tutorial/first-steps/  
https://fastapi.tiangolo.com/tutorial/sql-databases/

sqlAchemy  
https://fastapi.tiangolo.com/tutorial/sql-databases/  

alembic - Module migration
https://alembic.sqlalchemy.org/en/latest/

celery redis flower - task queue  
https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps  

plotly - chart  
https://plotly.com/javascript/  

websocket/server sent event   
(plan to send log messages to client)  
