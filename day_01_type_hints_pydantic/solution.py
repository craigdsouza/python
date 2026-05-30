from typing import Literal, Optional
from pydantic import BaseModel,Field , ConfigDict, EmailStr, ValidationError, computed_field, field_validator, model_validator

class User(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )
    id: int
    email: EmailStr
    age: int = Field(ge=18,le=99)
    role: Literal["admin","user"]
    username: str
    bio: Optional[str]

    @field_validator("username")
    @classmethod
    def strip_whitespace(cls, v:str) -> str:
        v = v.strip().lower()
        len_v = len(v)
        if " " in v:
            raise ValueError("username must not contain spaces")
        elif (len_v<3 or len_v>20):
            raise ValueError("username must be between 3 and 20 characters")
        return v

    # option A, this sets bio before instantiation, but this means username hasn't been validated yet
    # @model_validator(mode="before")
    # @classmethod
    # def set_bio(cls, data: dict) -> dict:
    #     if data.get('bio') is None:
    #         data['bio'] = f"Hi, I'm {data.get('username','')}"
    #     return data

    # option B, this sets bio after instantiation, overriding the frozen config setting
    @model_validator(mode="after")
    def set_bio(self):
        if self.bio is None:
            object.__setattr__(self,"bio",f"Hi, I'm {self.username}")
        return self

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.username} ({self.role})"
    

def validate_user(data: dict) -> tuple[User|None, list[dict]]:
    try:
        user = User(**data)
        print(f"[PASS] {user}")
        return [user,[]]
    except ValidationError as e:
        errors = e.errors()
        print(f"[FAIL] {len(errors)} errors" if len(errors)>1 else f"[FAIL] {len(errors)} error")
        for error in errors:
            field = error["loc"][0]
            message = error["msg"]
            print(f"- {field}: {message}")
        return [None, e.errors()]

def validate_many(rows: list[dict]) -> tuple[list[User],list[dict]]:
    val_results = [[],[]]
    for row in rows:
        result = validate_user(row)
        if result[0] is None:
            val_results[1].append(result[1])
        else:
            val_results[0].append(result[0])
    return val_results[0],val_results[1]



data = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":" ALIce","bio":None}
data3e = {"id":1, "email":"alice@example","age":15,"role":"use","username":"alice","bio":None}
dataue = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":"alice temp","bio":None}
dataefe = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":"alice","bio":None,"extra":None}
# validate_user(data)
# validate_user(data3e)
# validate_user(dataue)
# validate_user(dataefe)

data_list = [data,data3e,dataue,dataefe]
val_results = validate_many(data_list)
print("\n","Users: ",val_results[0])
# print("\n","Errors: ",val_results[1])

