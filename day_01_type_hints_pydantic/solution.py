from typing import Literal, Optional
from pydantic import BaseModel,Field , ConfigDict, EmailStr, ValidationError, field_validator, model_validator

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
        elif len_v is any([len_v<3,len_v>20]):
            raise ValueError("username must be between 3 and 20 characters")
        return v
    

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

data = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":"alice","bio":None}
data3e = {"id":1, "email":"alice@example","age":15,"role":"use","username":"alice","bio":None}
dataue = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":"alice temp","bio":None}
dataefe = {"id":1, "email":"alice@example.com","age":25,"role":"user","username":"alice","bio":None,"extra":None}
validate_user(data)
validate_user(data3e)
validate_user(dataue)
validate_user(dataefe)