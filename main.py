from fastapi import FastAPI
import uvicorn
from database.models.user import User  # noqa

from core.api.user.router import router as user_router


app = FastAPI()
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
