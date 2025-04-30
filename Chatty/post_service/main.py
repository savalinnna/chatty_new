from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routes import posts, comments, likes

app = FastAPI(openapi_url="/openapi.json")

# Подключаем маршруты
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])

# Swagger поддержка JWT
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Post Service",
        version="1.0.0",
        description="Микросервис для постов, комментариев и лайков",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema
