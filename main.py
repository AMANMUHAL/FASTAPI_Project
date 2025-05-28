from fastapi import FastAPI , Path, HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal , Optional
app = FastAPI()
import json


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", example='P001')]
    name: Annotated[str, Field(..., description="Name of the patient", example='Mohit')]
    city: Annotated[str, Field(..., description="City where patient is living", example='New Delhi')]
    age: Annotated[int, Field(..., gt=0, lt=150, description="Age of the patient", example=25)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient", example='male')]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters", example=1.5)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs", example=60)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <30:
            return 'Normal'
        else:
            return 'Overweight'
        
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=150)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open('patients.json','r') as file:
        data = json.load(file)
    return data

# converts dictinory into JSON file
def save_data(data):
    with open('patients.json','w') as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "Patient management API is running."}

@app.get("/about")
def about():
    return {"message": "This is the about page."}

@app.get("/patients")
def get_patients():
    data = load_data()
    return data

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description="ID of the patient in DB", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        # return {"error":"patient not found"}
        raise HTTPException(status_code=404 , detail="Patient not found")
    
@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of height , weight or BMI"),order_by:str= Query('asc',description="Sort in asc or desc order") ):

    valid_fields =['height', 'weight', 'bmi']

    sort_by = sort_by.lower()
    order_by = order_by.lower()

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid field selected from {valid_fields}")
    
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400, detail=f"invalid field selected from ['asc','desc']")
    
    data = load_data()

    sort_order = True if order_by =='desc' else False
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0) , reverse= sort_order)
    # if reverse True then desc , if false then asc

    return sorted_data


@app.post('/create')
def create_profile(patient:Patient):
    #load existing data in dict format
    data = load_data()

    #check if new data already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # add new data

    # converting pydantic object into dictonary
    # patient.model_dump()
    #       key                  value
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into json file
    save_data(data)

    return JSONResponse(status_code=201 , content ={'message' : 'patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdate):  
# patient_update is a pydantic object
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    # convert pydantic object into dictonary becaouse existing_patient_info is already a dict
    updated_existing_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_existing_info.items():
        existing_patient_info[key]= value
    # existing_patient_info -> create pydantic object -> which gives updated BMI and verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    # then pydantic obj -> dict 
    existing_patient_info= patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Patient Updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=202, content={'message':"Deleted successfully"})



