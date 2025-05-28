from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID", example='P001')]
    name: Annotated[str, Field(..., example='Mohit')]
    city: Annotated[str, Field(..., example='New Delhi')]
    age: Annotated[int, Field(..., gt=0, lt=150, example=25)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(...)]
    height: Annotated[float, Field(..., gt=0)]
    weight: Annotated[float, Field(..., gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 30:
            return "Normal"
        return "Overweight"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=150)
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
