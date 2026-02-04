from fastapi import APIRouter
from app.api.v1.routers import packages, subscriptions, payments, vouchers, mikrotik_vouchers, connect

api_router = APIRouter()

api_router.include_router(packages.router)
api_router.include_router(subscriptions.router)
api_router.include_router(payments.router)
api_router.include_router(vouchers.router)
api_router.include_router(mikrotik_vouchers.router)
api_router.include_router(connect.router)
