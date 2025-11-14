from pydantic import BaseModel

class CompanyListing(BaseModel):
    name: str
    msp: bool
    country: str
    city: str

    categories: list[str]
    products: list[str]

    overview: str

class ProcessedHTML(BaseModel):
    tree: any
    listings: any
    pages: int