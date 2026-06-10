from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db
from app.api.endpoints import vehicles, maintenance, parts

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Vehicle Fleet Maintenance backend — covering vehicle registry, "
        "maintenance logging, and parts inventory.\n\n"
        "**Telemetry & Analytics** endpoints are implemented separately."
    ),
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(maintenance.router, prefix="/api/v1")
app.include_router(parts.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
