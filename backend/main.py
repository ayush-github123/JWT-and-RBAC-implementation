from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import engine, Base
from routes import auth, task
from models.user import User
from models.task import Task
from models.refresh_token import RefreshToken
from core.logging import setup_logging, logging



setup_logging("INFO")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # logger.info("DB initialized successfully.")
    except Exception as e:
        # logger.error(f"DB initialization error: {e}")
        pass

    try:
        yield
        logger.info("Application startup complete.")
    finally:
        pass


app = FastAPI(title="JWT and RBAC implementation", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS automatically
    allow_headers=["*"],   # allows Authorization, Content-Type
)


@app.get("/health")
def check_health():
    health = {
        "health": "healthy",
        "message": "route check success - health check completed..."
    }
    return health



app.include_router(auth.router)
app.include_router(task.router)