import uvicorn
from fastapi import FastAPI
import fastapi.openapi.utils as openapi
from fastapi.middleware.cors import CORSMiddleware
from core import engine, Base
from modules.account.controller import router as auth_router
from modules.report.controller import router as report_router

app = FastAPI()

def custom_swagger():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = openapi.get_openapi(
        title="FAST-API",
        version="1.0.0",
        routes=app.routes,
        openapi_version="3.1.0",
    )
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if "responses" in operation:
                for status_code, response in operation["responses"].items():
                    response["description"] = ""
                if "422" in operation["responses"]:
                    del operation["responses"]["422"]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/", tags=["Root"], operation_id='root')
async def root():
    return {"message": "FAST-API"}

app.openapi = custom_swagger
app.include_router(auth_router)
app.include_router(report_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host='0.0.0.0', port=8000)
