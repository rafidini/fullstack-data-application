from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 


POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres/{POSTGRES_DB}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

BaseSQL = declarative_base()

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class PostModel(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    title: str
    description: Optional[str]
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[datetime, Field(default_factory=lambda: datetime.now())]

    class Config:
        orm_mode = True

class Post(BaseSQL):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())


app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/lol")
def get_date():
    return {"date": str(datetime.now())}

from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime


def get_post_by_id(post_id: str, db: Session) -> PostModel:
    record = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_post(db: Session, post: Post) -> Post:
    record = db.query(Post).filter(Post.id == post.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.id = str(db_post.id)
    return db_post

@app.get("/create_post")
def add_post():
    create_post()
    return {"results":1}
