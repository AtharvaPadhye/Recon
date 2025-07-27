from fastapi import APIRouter, HTTPException
from ..models import Task, TaskRequest
from .cases import get_case

router = APIRouter(prefix="/v1/task_recon", tags=["tasks"])

tasks_db = []

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
    tasks_db.append(task)
    return task
