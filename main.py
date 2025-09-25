from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from pathlib import Path
from packages.schema import schema
from packages.context.database import db_context

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create FastAPI app
app = FastAPI(title="E-commerce Monorepo API", version="1.0.0")

"""
Configure CORS
- Use env var ALLOW_ORIGINS as a comma-separated list of allowed origins
    e.g. ALLOW_ORIGINS=http://localhost:3000,https://app.example.com
- Set to "*" to allow all origins (development only)
"""
origins_env = os.getenv("ALLOW_ORIGINS", "*")
allow_origins = ["*"] if origins_env == "*" else [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=False,  # JWT is sent via Authorization header; cookies not required
        allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["*"]
)

# Rely on CORSMiddleware for preflight; no manual OPTIONS handlers needed

# Mount GraphQL router with playground at /graphql
graphql_app = GraphQLRouter(
    schema,
    context_getter=db_context.get_context,
    graphql_ide=True  
)

# Mount GraphQL router at /graphql
app.include_router(graphql_app, prefix="/graphql", include_in_schema=True)

# Redirect root to GraphQL Playground
@app.get("/")
async def root():
    return RedirectResponse(url="/graphql")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "E-commerce Monorepo API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
