from aiogram.fsm.state import StatesGroup, State

class Registrarion(StatesGroup):
    await_base_infromation = State()
    await_new_name = State()
    await_organization = State()
    await_organization_password = State()
    name = State()
    user_telegram_id = State()
    
    
class MainUsage(StatesGroup):
    ticket_acsess = State()
    changing_name = State()
    changing_org = State()
    ticket_creation = State()
    ticket_fill = State()
    
class Admin(StatesGroup):
    admin_acsess = State()
    admin_verifying_key = State()
    admin_company_creation_name = State()
    admin_company_creation_password = State()
    admin_company_creation_email = State()
    admin_company_creation_phone = State()
    admin_company_creation_website = State()
    admin_company_creation_additional_info = State()