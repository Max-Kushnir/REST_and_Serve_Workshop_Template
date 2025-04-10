import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.models import Application, ApplicationCreate
from backend.crud import (
    add_application, get_all_applications,
    get_application_by_id, update_application_by_id,
    delete_application_by_id
)

app = FastAPI()

# serve static front end 

@app.api_route("/", methods=["GET", "HEAD"])
def serve_frontend(request: Request):
    return FileResponse("frontend/index.html")

# implement POST (creates application)

@app.get("/applications/", response_model=list[Application])
def get_applications():
    return get_all_applications()

@app.get("/applications/count")
def get_application_count():
    return {"application_count": len(get_all_applications())}

@app.get("/applications/{app_id}", response_model=Application)
def get_application(app_id: int):
    app = get_application_by_id(app_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@app.put("/applications/{app_id}", response_model=Application)
def update_application(app_id: int, update_data: ApplicationCreate):
    updated_app = update_application_by_id(app_id, update_data)
    if updated_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_app

# implement DELETE (deletes application)

# serve API using using Uvicorn
