from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="ACIS Enterprise Backend")

# Include our Jinja2 rendering routes (No prefix!)
app.include_router(router)