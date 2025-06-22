from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from src.user.routers.admin import router as admin_router
from src.user.routers.auth import router as auth_router
from src.user.routers.user import router as user_router
from src.weather.router import router as weather_router


app = FastAPI(
    title="Weather App",
)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(weather_router)


@app.get("/")
def home_page():
    # Redirect to /docs for easy access to API documentation
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Service is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        reload=True,
    )
