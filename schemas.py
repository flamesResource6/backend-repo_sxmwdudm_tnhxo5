"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Study Group app schemas

class Group(BaseModel):
    name: str = Field(..., description="Group name")
    subject: str = Field(..., description="Subject or topic")
    description: str = Field(..., description="What the group focuses on")

class Session(BaseModel):
    title: str = Field(..., description="Session title")
    description: Optional[str] = Field(None, description="What will be covered")
    group_id: Optional[str] = Field(None, description="Related group id")
    start_time: datetime = Field(..., description="Start time of the session (UTC)")
    duration_minutes: int = Field(60, ge=15, le=300, description="Duration in minutes")

class Discussion(BaseModel):
    author: str = Field(..., description="Name of the member")
    message: str = Field(..., description="Discussion message")
    group_id: Optional[str] = Field(None, description="Related group id")

class Goal(BaseModel):
    member: str = Field(..., description="Member name")
    content: str = Field(..., description="Goal description")
    target_date: Optional[datetime] = Field(None, description="Optional target date")
    status: str = Field("active", description="active/completed")

class Note(BaseModel):
    title: str = Field(..., description="Note title")
    description: Optional[str] = Field(None, description="Short description")
    download_url: str = Field(..., description="URL to download the note")
    tag_list: List[str] = Field(default_factory=list, description="Tags for filtering")

class Signup(BaseModel):
    name: str
    email: str
    interest: Optional[str] = None
