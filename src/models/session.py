from pydantic import BaseModel

class Session(BaseModel):
    user_id: str
    session_id: str
