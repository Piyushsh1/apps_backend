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
    allow_origins=[
      "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add comprehensive OPTIONS handlers for CORS preflight requests
@app.options("/graphql")
async def graphql_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, X-Requested-With",
            "Access-Control-Max-Age": "86400"
        }
    )

@app.options("/")
async def root_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, X-Requested-With",
            "Access-Control-Max-Age": "86400"
        }
    )

# Catch-all OPTIONS handler for any other preflight requests
@app.options("/{full_path:path}")
async def options_handler():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, X-Requested-With",
            "Access-Control-Max-Age": "86400"
        }
    )

# Mount GraphQL router with playground at /graphql
graphql_app = GraphQLRouter(
    schema,
    context_getter=db_context.get_context,
    graphql_ide=True  # Enable GraphQL Playground
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
