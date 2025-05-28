from fastapi import APIRouter, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from app.models import Patient, PatientUpdate
from app.utils import load_data, save_data

router = APIRouter()

@router.get("/about")
def about():
    return {"message": "This is the about page."}

@router.get("/patients")
def get_patients():
    return load_data()

@router.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@router.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@router.get('/sort')
def sort_patient(
    sort_by: str = Query(..., description="Sort by height, weight or bmi"),
    order_by: str = Query('asc', description="asc or desc")
):
    valid_fields = ['height', 'weight', 'bmi']
    sort_by = sort_by.lower()
    order_by = order_by.lower()

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field: choose from {valid_fields}")
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

    data = load_data()
    sort_order = order_by == 'desc'
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@router.post('/create')
def create_profile(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@router.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing = data[patient_id]
    updates = patient_update.model_dump(exclude_unset=True)
    existing.update(updates)
    existing['id'] = patient_id
    patient_obj = Patient(**existing)
    data[patient_id] = patient_obj.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient Updated'})

@router.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=202, content={'message': "Deleted successfully"})
