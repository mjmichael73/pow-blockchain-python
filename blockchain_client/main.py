import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .api.routes import router
from .application.wallet_service import WalletService
from .infrastructure.crypto import CryptoService

def create_app() -> FastAPI:
    app = FastAPI()
    
    # Initialize layers
    crypto_service = CryptoService()
    wallet_service = WalletService(crypto_service)
    
    # Attach to app state for dependency injection
    app.state.wallet_service = wallet_service
    
    # Static and Templates
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.state.templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
    app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

    app.include_router(router)
    
    return app

load_dotenv()
app = create_app()

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=int(os.getenv("BLOCKCHAIN_CLIENT_PORT", 8081)), type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port
    host = os.getenv("BLOCKCHAIN_CLIENT_HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port)
