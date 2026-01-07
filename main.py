from importlib import reload
from modules.middleware.master import *
SHOW_DOCS = os.getenv("SHOW_DOCS", "false").lower()
app = FastAPI(
    docs_url=None if SHOW_DOCS != "true" else "/docs",
    redoc_url=None if SHOW_DOCS != "true" else "/redoc",
    openapi_url=None if SHOW_DOCS != "true" else "/openapi.json",
)

app.include_router(index_router)
app.include_router(gauge_router)
app.include_router(counter_router)
app.include_router(aggregate_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)