import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from typing import Annotated
from sqlalchemy.orm import Session
from keycloak import KeycloakOpenID
from database import database as database
from database.database import TaskDB
from model.task import Task

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/recieve_jwt_token")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/get_tasks")
async def get_tasks(db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        try:
            result = db.query(TaskDB).limit(100).all()
            return result
        except Exception as e:
            return "Cant access database!"
    else:
        return "Wrong JWT Token"

@app.get("/get_task_by_id")
async def get_task_by_id(task_id: int, db: db_dependency):
    try:
        result = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@app.post("/add_task")
async def add_task(task: Task, db: db_dependency):
    try:
        task_db = TaskDB(
            id=task.id,
            task_name=task.task_name,
            due_date=task.due_date,
            description=task.description,
            importance=task.importance
        )
        db.add(task_db)
        db.commit()
        return task_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/delete_task")
async def delete_task(task_id: int, db: db_dependency):
    try:
        task_db = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        db.delete(task_db)
        db.commit()
        return "Success"
    except Exception as e:
        return "Cant find task"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))