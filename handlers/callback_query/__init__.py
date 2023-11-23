from aiogram import Router

from .check_classified import router as check_router

router = Router()
router.include_router(check_router)
