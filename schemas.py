from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    title: str
    author: str
    model_config = ConfigDict(from_attributes=True)

class BookCreate(BookBase):
    pass
    model_config = ConfigDict(from_attributes=True)

class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    content: str
    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(ReviewBase):
    pass
    model_config = ConfigDict(from_attributes=True)


class Review(ReviewBase):
    id: int
    book_id: int
    model_config = ConfigDict(from_attributes=True)
        
class Config:
    from_attributes = True
