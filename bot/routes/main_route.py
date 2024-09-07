from aiogram.filters import Command
from aiogram import Router, types
from services.fsm import Registrarion
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard

main_router = Router()