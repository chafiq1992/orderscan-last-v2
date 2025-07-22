from pydantic import BaseModel, constr

class ScanIn(BaseModel):
    barcode: constr(min_length=1, max_length=50)

class ScanOut(BaseModel):
    result: str
    order: str | None = None
    tag: str | None = None
