# handlers/errors.py
from aiogram import Router
from aiogram.types import ErrorEvent
from bot import logger

router = Router()


@router.errors()
async def error_handler(event: ErrorEvent):
    """Handle errors"""
    logger.error(f"Update {event.update} caused error {event.exception}")
