from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    task_name: str
    description: str
    importance: int
    due_date: Optional[datetime] = datetime.now()