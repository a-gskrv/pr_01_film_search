from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers.pages import router as pages_router

def create_app() -> FastAPI:
    app = FastAPI()

    app.mount(
        "/static",
        StaticFiles(directory="app/interfaces/fastapi/static"),
        name="static",
    )

    app.include_router(pages_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.interfaces.fastapi.main:app", reload=True)

# uvicorn app.interfaces.fastapi.main:app --reload
# uvicorn app.interfaces.fastapi.main:app --reload --access-log --log-level debug
