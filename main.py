from fastapi import FastAPI
import uvicorn
from database.models.user import User  # noqa
from database.models.order import Order  # noqa


from core.api.user.router import router as user_router
from core.api.order.router import router as order_router


app = FastAPI()
app.include_router(user_router)
app.include_router(order_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
