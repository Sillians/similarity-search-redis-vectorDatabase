from typing import Optional
from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """
    pass


# Model for the input query
class QueryModel(BaseModel):
    query: Optional[str]