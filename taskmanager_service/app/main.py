import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

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


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_tasks")
async def get_tasks(db: db_dependency):
    try:
        result = db.query(TaskDB).limit(100).all()
        return result
    except Exception as e:
        return "Cant access database!"


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