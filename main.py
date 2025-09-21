from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
from dotenv import load_dotenv
import os
from pathlib import Path
from packages.schema import schema
from packages.context.database import db_context

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create FastAPI app
app = FastAPI(title="E-commerce Monorepo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add OPTIONS handler for GraphQL endpoint before mounting the router
@app.options("/")
async def graphql_options():
    return Response(status_code=200)

# Mount GraphQL router with playground at /graphql
graphql_app = GraphQLRouter(
    schema,
    context_getter=db_context.get_context,
    graphql_ide=True  # Enable GraphQL Playground
)

# Mount GraphQL router at /graphql
app.include_router(graphql_app, prefix="/graphql")

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
    uvicorn.run(app, host="0.0.0.0", port=8001)
