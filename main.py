#Importing FastAPI
import json
from fastapi.exceptions import HTTPException            
from fastapi import FastAPI,Body


app = FastAPI()

#htts Methods 1 - GET is used to fetch data or read daa.

@app.get('/')
def greet():
    return "Hello World"


@app.get('/about')
def about():
    return "This is about page"

@app.get('/feedback')
def feedback():
    return "This is feedback page"


def load_data():
    with open('data.json','r') as fs:
        data = json.load(fs)
    return data 

#endpoint -> data.json complete data dekhna hai

@app.get('/view')
def view():
    return load_data()

#endpoint -> ek specific id ka data view kar paye

@app.get('/view/{patient_id}')
def view_id(patient_id):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        return "patient not found"
    
def save_data(data):
    with open('data.json','w') as fs:
        json.dump(data,fs)

#creating new patient by using POST


@app.post('/create/{patient_id}')
def create(patient_id:str,patient:dict=Body(...)):
    data = load_data()
    if patient_id in data:
        raise HTTPException(status_code=400,detail="patient already exist")
    data[patient_id] = patient
    save_data(data)

#ebdpoint for updating patient

@app.put('/edit/{patient_id}')
def edit(patient_id:str,update_data:dict=Body(...)):
    data = load_data()

    #check if patient already exist or not 
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="patient not found")

    #existing patient data 
    patient_data = data[patient_id]

    #update only provided data 
    for key,value in updated_data.items():
        patient_data[key] = value
    #save data
    save_data(data)

#endpoint for deleting record
@app.delete('/remove/{patient_id}')
def remove(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400,detail="patient not found")

    del data[patient_id]
    save_data(data)