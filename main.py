from fastapi import FastAPI
import uvicorn
from database.engine import engine
from database.base import Base
from database.models import User  # noqa

from core.api.user.router import router as user_router


app = FastAPI()
app.include_router(user_router)


Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
