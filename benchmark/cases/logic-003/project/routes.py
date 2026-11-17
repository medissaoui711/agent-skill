from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
profiles = {"u-1": {"delivery_note": "Leave at reception"}}


class ProfilePatch(BaseModel):
    delivery_note: str | None = None


@app.patch("/profiles/{user_id}")
def update_profile(user_id: str, payload: ProfilePatch):
    profile = profiles.get(user_id)
    if profile is None:
        return {"error": "not found"}

    if payload.delivery_note:
        profile["delivery_note"] = payload.delivery_note

    return profile
