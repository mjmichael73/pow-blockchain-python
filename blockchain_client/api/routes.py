from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from ..application.wallet_service import WalletService

router = APIRouter()

def get_wallet_service(request: Request) -> WalletService:
    return request.app.state.wallet_service

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return request.app.state.templates.TemplateResponse(request=request, name="index.html")

@router.post("/generate/transaction")
async def generate_transaction(
    sender_public_key: str = Form(...),
    sender_private_key: str = Form(...),
    recipient_public_key: str = Form(...),
    amount: float = Form(...),
    service: WalletService = Depends(get_wallet_service)
):
    result = service.create_and_sign_transaction(
        sender_public_key, sender_private_key, recipient_public_key, amount
    )
    return result

@router.get("/make/transaction", response_class=HTMLResponse)
async def make_transaction(request: Request):
    return request.app.state.templates.TemplateResponse(request=request, name="make_transaction.html")

@router.get("/view/transactions", response_class=HTMLResponse)
async def view_transactions(request: Request):
    return request.app.state.templates.TemplateResponse(request=request, name="view_transactions.html")

@router.get("/wallet/new")
async def new_wallet(service: WalletService = Depends(get_wallet_service)):
    return service.create_wallet()
