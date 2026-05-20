from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse

import json
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated, Optional
from datetime import date

app = FastAPI()


class Patient(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the patient",
        example="P01"
    )

    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]

    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description="Gender of the patient")]

    DOB: Annotated[date, Field(..., description="Date of birth of the patient")]

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()

        age = today.year - self.DOB.year

        if today < date(today.year, self.DOB.month, self.DOB.day):
            age -= 1

        return age

    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
    

class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Full name of the patient", example="John Doe")]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Other']], Field(None, description="Gender of the patient")]
    DOB: Annotated[Optional[date], Field(None, description="Date of birth of the patient")]


def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient with this ID already exists"
        )

    data[patient.id] = patient.model_dump(
        mode='json',
        exclude=['id']
    )
    save_data(data)

    return JSONResponse(
        content={
            "message": "Patient created successfully",
            "patient_id": patient.id
        }
    )


@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: UpdatePatient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing_patient = Patient(id=patient_id, **data[patient_id])
    updated_patient = existing_patient.model_copy(update=patient_update.model_dump(exclude_unset=True))

    data[patient_id] = updated_patient.model_dump(mode='json', exclude=['id'])
    save_data(data)

    return JSONResponse(
        content={
            "message": "Patient updated successfully",
            "patient_id": patient_id
        }
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str = Path(..., description="ID of the patient to delete", example="P01")):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail = "patient not found"
        )
    del data[patient_id]
    save_data(data)
    return JSONResponse(
        content={
            "message": "Patient deleted successfully",
            "patient_id": patient_id
        }
    )
