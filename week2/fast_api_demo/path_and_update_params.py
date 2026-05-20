from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()


def get_patient_data(patient_id: str):
    with open('patients.json', 'r') as f:
        data = json.load(f)[patient_id]
    return data


def get_all_patients():
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
    return get_all_patients()


@app.get('/patient/{patient_id}')
def get_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P01"
    )
):
    try:
        return get_patient_data(patient_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort by name, dob, or gender"
    ),
    order: str = Query(
        'asc',
        description="ascending or descending"
    )
):
    with open('patients.json', 'r') as f:
        data = json.load(f)

    if sort_by not in ['name', 'DOB', 'gender']:
        raise HTTPException(status_code=400, detail="Invalid query param")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid query param")

    sorted_data = sorted(
        data.values(),
        key=lambda x: x[sort_by],
        reverse=(order == 'desc')
    )

    return sorted_data