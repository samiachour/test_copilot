from pydantic import BaseModel, EmailStr
from typing import Optional, List


class AssetBase(BaseModel):
    name: str
    serial_number: str
    description: Optional[str] = None


class AssetCreate(AssetBase):
    employee_id: int


class AssetUpdate(AssetBase):
    employee_id: Optional[int] = None


class AssetOut(AssetBase):
    id: int
    employee_id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    department: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int
    assets: List[AssetOut] = []

    class Config:
        orm_mode = True
