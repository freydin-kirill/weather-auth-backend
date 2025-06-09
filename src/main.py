from fastapi import FastAPI

from src.user.routers.admin import router as admin_router
from src.user.routers.auth import router as auth_router
from src.user.routers.user import router as user_router


app = FastAPI(
    title="Weather App",
)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def home_page():
    return {"message": "Hello World!"}


@app.get("/health")
def health():
    return {"status": "ok", "message": "Service is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        reload=True,
    )
