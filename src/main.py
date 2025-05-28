from fastapi import FastAPI

from src.user.router import router


app = FastAPI(
    title="Some Simple App"
)

app.include_router(
    router
)

@app.get("/")
def home_page():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
            app="src.main:app",
            reload=True,
        )
