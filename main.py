from fastapi import FastAPI , Path, HTTPException , Query
app = FastAPI()
import json

def load_data():
    with open('patients.json','r') as file:
        data = json.load(file)
    return data

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
