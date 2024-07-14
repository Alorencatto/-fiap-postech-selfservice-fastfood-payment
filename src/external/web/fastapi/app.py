from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.communication.controller.payment import PaymentController
from src.external.web.fastapi.api_v2.endpoints.payment import HTTPAPIAdapter
from src.external.database.mongo.repositories.payment import PaymentRepository
from src.config import get_config

# V1
from src.external.web.fastapi.api_v1.api import router as api_router

from src.external.web.fastapi.exception_handlers import register_exceptions

config = get_config()

app = FastAPI(
    title=config.TITLE,
    version=config.VERSION,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
    openapi_url=config.OPENAPI_URL,
    root_path=config.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# V1
# app.include_router(api_router, prefix="/api/v1")

register_exceptions(app)


# V2
@app.on_event("startup")
async def startup_event():
    payment_repository = PaymentRepository()
    payment_controller = PaymentController(payment_repository)
    http_api_adapter = HTTPAPIAdapter(payment_controller=payment_controller)
    app.include_router(http_api_adapter.router)
