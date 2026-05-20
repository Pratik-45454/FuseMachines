from pydantic import BaseModel, ValidationError, Field, EmailStr, AnyHttpUrl, AnyUrl
from typing import List,Dict, Optional

# step1: definition of ideal schema
class Patient(BaseModel):
    # by default all these model fields are required,
    #  if we want to make them optional, 
    # we can use Optional from typing
    name: Optional[str] = None
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    # inbuilt thing for email validation
    email: EmailStr
    facebook_profile: Optional[AnyHttpUrl] = None
    website: Optional[AnyUrl] = None
    married: Optional[bool] = False
    allergies: List[str]
    contact_details: dict[str,str] #key and value specified


# step2: creating raw instances of the Patient class
patient_info = {'age': 30, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'john.doe@example.com'}}
patient_2_info = {'name': 'Jane', 'age': '20', 'allergies': ['penicillin', 'grass'], 'contact_details': {'email': 'jane@example.com', 'phone': '123-456-7890'}}

# pydantic is smart enough to convert
# the age to int, but if we pass a 
# non-convertible value, it will raise a validation error


# unpacking the dictionary to 
# create an instance of Patient
# step3: validating the data using pydantic
patient1 = Patient(**patient_info)
patient2 = Patient(**patient_2_info)


def validate_patient_info(patient: Patient):
    print(f"""Patient Name: 
              {patient.name},
              Married: {patient.married},
              Age: {patient.age}, 
              Allergies: {patient.allergies}, 
              Contact Details: {patient.contact_details}""")
    
#pass the validated obj to model
validate_patient_info(patient1)
validate_patient_info(patient2)

