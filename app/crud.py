from sqlalchemy.orm import Session

from . import models, schemas


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, db_employee: models.Employee, employee_data: schemas.EmployeeUpdate):
    for field, value in employee_data.dict().items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, db_employee: models.Employee):
    db.delete(db_employee)
    db.commit()
    return None


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).offset(skip).limit(limit).all()


def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()


def get_assets_for_employee(db: Session, employee_id: int):
    return db.query(models.Asset).filter(models.Asset.employee_id == employee_id).all()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, db_asset: models.Asset, asset_data: schemas.AssetUpdate):
    for field, value in asset_data.dict(exclude_unset=True).items():
        setattr(db_asset, field, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_asset(db: Session, db_asset: models.Asset):
    db.delete(db_asset)
    db.commit()
    return None
