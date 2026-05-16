from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home():
    return RedirectResponse(url="/employees")


@router.get("/employees")
def list_employees(request: Request, db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    return templates.TemplateResponse("employees.html", {"request": request, "employees": employees})


@router.get("/employees/create")
def create_employee_form(request: Request):
    return templates.TemplateResponse("employee_form.html", {"request": request, "employee": None})


@router.post("/employees/create")
def create_employee(
    request: Request,
    name: str = Form(...),
    department: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    employee_in = schemas.EmployeeCreate(name=name, department=department, email=email)
    crud.create_employee(db, employee_in)
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/employees/{employee_id}")
def employee_detail(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    return templates.TemplateResponse("employee_detail.html", {"request": request, "employee": employee})


@router.get("/employees/{employee_id}/edit")
def edit_employee_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    return templates.TemplateResponse("employee_form.html", {"request": request, "employee": employee})


@router.post("/employees/{employee_id}/edit")
def edit_employee(
    request: Request,
    employee_id: int,
    name: str = Form(...),
    department: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    employee_data = schemas.EmployeeUpdate(name=name, department=department, email=email)
    crud.update_employee(db, employee, employee_data)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.post("/employees/{employee_id}/delete")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    crud.delete_employee(db, employee)
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/assets")
def list_assets(request: Request, db: Session = Depends(get_db)):
    assets = crud.get_assets(db)
    return templates.TemplateResponse("assets.html", {"request": request, "assets": assets})


@router.get("/employees/{employee_id}/assets/create")
def create_asset_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    return templates.TemplateResponse("asset_form.html", {"request": request, "asset": None, "employee": employee})


@router.post("/employees/{employee_id}/assets/create")
def create_asset(
    request: Request,
    employee_id: int,
    name: str = Form(...),
    serial_number: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employée non trouvée")
    asset_in = schemas.AssetCreate(name=name, serial_number=serial_number, description=description, employee_id=employee_id)
    crud.create_asset(db, asset_in)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.get("/assets/{asset_id}/edit")
def edit_asset_form(request: Request, asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset non trouvé")
    return templates.TemplateResponse("asset_form.html", {"request": request, "asset": asset, "employee": asset.employee})


@router.post("/assets/{asset_id}/edit")
def edit_asset(
    request: Request,
    asset_id: int,
    name: str = Form(...),
    serial_number: str = Form(...),
    description: str = Form(None),
    employee_id: int = Form(...),
    db: Session = Depends(get_db),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset non trouvé")
    asset_data = schemas.AssetUpdate(name=name, serial_number=serial_number, description=description, employee_id=employee_id)
    crud.update_asset(db, asset, asset_data)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.post("/assets/{asset_id}/delete")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset non trouvé")
    employee_id = asset.employee_id
    crud.delete_asset(db, asset)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)
