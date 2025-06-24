"""Base CRUD operations."""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import TypeVar, Generic, Type, List, Optional
from pydantic import BaseModel

from app.core.logger import logger

# Define generic types for SQLAlchemy models and Pydantic schemas
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with SQLAlchemy model.
        
        Args:
            model: The SQLAlchemy model
        """
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: Database session
            id: ID of the record to get
            
        Returns:
            The record if found, None otherwise
        """
        logger.debug(f"Getting {self.model.__name__} with id {id}")
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get multiple records.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        logger.debug(f"Getting multiple {self.model.__name__} records (skip={skip}, limit={limit})")
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Create schema with the data to create
            
        Returns:
            The created record
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Created {self.model.__name__} with id {getattr(db_obj, 'id', None)}")
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> None:
        """
        Remove a record.
        
        Args:
            db: Database session
            id: ID of the record to remove
            
        Raises:
            HTTPException: If record not found
        """
        obj = db.query(self.model).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        db.delete(obj)
        db.commit()
        logger.info(f"Deleted {self.model.__name__} with id {id}")
        return None
