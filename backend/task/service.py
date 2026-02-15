from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from models.task import Task
from models.user import User
from schemas.task import TaskCreate, TaskUpdate
import logging

logger = logging.getLogger(__name__)


class TaskService:
    @staticmethod
    async def create_task( db: AsyncSession, task_data: TaskCreate, current_user: User) -> Task:

        task = Task(
            title=task_data.title,
            description=task_data.description,
            owner_id=current_user.id
        )
        logger.info("Creating task")
        db.add(task)
        await db.commit()
        await db.refresh(task)
        logger.info("Task Created")

        return task


    @staticmethod
    async def get_tasks( db: AsyncSession, current_user: User, skip: int = 0, limit: int = 10):
        result = await db.execute(select(Task).where(Task.owner_id == current_user.id).offset(skip).limit(limit))
        return result.scalars().all()


    @staticmethod
    async def get_all_tasks( db: AsyncSession, current_user: User, skip: int = 0, limit: int = 10):
        # if current_user.role == "ADMIN":
        result = await db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()
        # else:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Not authorized"
        #     )            


    @staticmethod
    async def update_task(db: AsyncSession,task_id: str,task_data: TaskUpdate,current_user: User) -> Task:
        logger.info("Updating Task")
        result = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()

        if not task:
            logger.error("Task not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        if task.owner_id != current_user.id and current_user.role != "ADMIN":
            logger.error("Not authorized")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)
        logger.info("Task created")
        return task


    @staticmethod
    async def delete_task( db: AsyncSession, task_id: str, current_user: User):
        result = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()

        if not task:
            logger.error("Task not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        if task.owner_id != current_user.id and current_user.role != "ADMIN":
            logger.error("Not authorized")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

        await db.delete(task)
        await db.commit()
