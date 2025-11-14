from pydantic import BaseModel
from typing import Any

class CompanyListing(BaseModel):
    name: str
    msp: bool
    country: str
    city: str

    categories: list[str]
    products: list[str]

    overview: str

class ProcessedHTML(BaseModel):
    tree: Any
    listings: Any
    pages: int

    #class Config:
    #    arbitrary_types_allowed = True