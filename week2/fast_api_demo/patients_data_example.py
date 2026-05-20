from fastapi import FastAPI
import json
app = FastAPI()


def get_patient_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {'message': 'this is patient data example'}

@app.get("/about")
def about():
    return {'message': 'This is a FastAPI demo application for patient data'}

@app.get("/view")
def view():
    data = get_patient_data()
    return data