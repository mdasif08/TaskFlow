"""
API routes for TaskFlow
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from .database import get_db
from .models import Task, User, TaskStatus, TaskPriority
from .schemas import (
    TaskCreate, TaskUpdate, Task as TaskSchema, 
    UserCreate, UserLogin, Token, User as UserSchema,
    TaskListResponse
)
from .auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from datetime import timedelta

# Constants
TASK_NOT_FOUND_MSG = "Task not found"

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Authentication routes
@router.post("/auth/signup", response_model=UserSchema)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        logger.info("Attempting to create user: %s", user.username)
        
        # Check if user already exists
        db_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        if db_user:
            logger.warning("User already exists: %s", user.username)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info("User created successfully: %s", user.username)
        return db_user
        
    except IntegrityError as e:
        logger.error("Database integrity error during signup: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        ) from e
    except Exception as e:
        logger.error("Unexpected error during signup: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        ) from e

@router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User routes
@router.get("/users/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Task routes
@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    task_status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks with optional filtering"""
    query = db.query(Task).filter(Task.assigned_user_id == current_user.id)
    
    # Apply filters
    if task_status:
        query = query.filter(Task.status == task_status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    
    return TaskListResponse(
        tasks=[TaskSchema.from_orm(task) for task in tasks],
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.post("/tasks", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    try:
        logger.info("Creating task for user: %s", current_user.username)
        
        # Automatically assign task to current user
        task_data = task.dict()
        task_data['assigned_user_id'] = current_user.id
        
        db_task = Task(**task_data)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        logger.info("Task created successfully: %s", db_task.id)
        return db_task
        
    except Exception as e:
        logger.error("Error creating task: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        ) from e

@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TASK_NOT_FOUND_MSG
        )
    return task

@router.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TASK_NOT_FOUND_MSG
        )
    
    # Update only provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TASK_NOT_FOUND_MSG
        )
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
