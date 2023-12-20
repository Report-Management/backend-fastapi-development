import uvicorn
from fastapi import FastAPI
import fastapi.openapi.utils as openapi
from fastapi.middleware.cors import CORSMiddleware
from core import engine, Base
from modules.auth.controller import router as auth_router
from modules.users.controller import router as user_router
from modules.report.controller import router as posts_router
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(
    title="Report Management",
    docs_url=None,
)

def custom_swagger():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = openapi.get_openapi(
        title="Report Management - APIs",
        version="1.2.0",
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

@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

app.openapi = custom_swagger
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)

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
