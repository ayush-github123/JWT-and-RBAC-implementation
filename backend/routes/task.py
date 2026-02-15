from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from task.service import TaskService
from auth.services import get_current_active_user
from core.database import get_db
from models.user import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task( task_data: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info("Creating task")
    return await TaskService.create_task(db, task_data, current_user)


@router.get("/", response_model=List[TaskResponse])
async def list_tasks( skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info("Getting task")
    return await TaskService.get_tasks(db, current_user, skip, limit)


@router.get("/all", response_model=List[TaskResponse])
async def list_all_tasks( skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info("Getting all tasks")
    if current_user.role == "ADMIN":
        return await TaskService.get_all_tasks(db, current_user, skip, limit)
    
    raise HTTPException(401, {"detail": "You are not authorized to perform this task"})


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task( task_id: str, task_data: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info("Editing tasks")
    return await TaskService.update_task(db, task_id, task_data, current_user)


@router.delete("/{task_id}")
async def delete_task(task_id: str,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    logger.info("Deleting tasks")
    await TaskService.delete_task(db, task_id, current_user)
    return {"message": "Task deleted successfully"}
