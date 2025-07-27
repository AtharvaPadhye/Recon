from fastapi import APIRouter, HTTPException
from ..models import Task, TaskRequest
from .cases import get_case

router = APIRouter(prefix="/v1/task_recon", tags=["tasks"])

# Store tasks in-memory keyed by task ID
tasks_db: dict[str, Task] = {}

@router.post("", response_model=Task)
def create_task(task_req: TaskRequest):
    if not get_case(task_req.case_id):
        raise HTTPException(status_code=404, detail="case_id not found")
    task = Task(
        case_id=task_req.case_id,
        sensor_types=task_req.sensor_types,
        urgency=task_req.urgency,
        preferred_assets=task_req.preferred_assets,
    )
    tasks_db[task.id] = task
    return task

@router.get("", response_model=list[Task])
def list_tasks():
    return list(tasks_db.values())

def get_task(task_id: str) -> Task | None:
    return tasks_db.get(task_id)

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, update: Task):
    if not get_case(update.case_id):
        raise HTTPException(status_code=404, detail="case_id not found")
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="task not found")
    update.id = task_id
    tasks_db[task_id] = update
    return update

@router.delete("/{task_id}")
def delete_task(task_id: str):
    task = tasks_db.pop(task_id, None)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {"detail": "deleted"}
