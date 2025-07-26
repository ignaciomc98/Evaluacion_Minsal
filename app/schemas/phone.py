from pydantic import BaseModel, Field

class PhoneSchema(BaseModel):
    number: str = Field(..., alias="number")
    citycode: str = Field(..., alias="citycode")
    countrycode: str = Field(..., alias="countrycode")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "populate_by_alias": True,  
}
