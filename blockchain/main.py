import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .application.services import BlockchainService
from .infrastructure.crypto import CryptoService
from .infrastructure.p2p import P2PClient

def create_app() -> FastAPI:
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize layers
    crypto_service = CryptoService()
    p2p_client = P2PClient()
    blockchain_service = BlockchainService(crypto_service, p2p_client)

    # Attach to app state for dependency injection
    app.state.blockchain_service = blockchain_service
    
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
    parser.add_argument("-p", "--port", default=int(os.getenv("BLOCKCHAIN_PORT", 5001)), type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port
    host = os.getenv("BLOCKCHAIN_HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port)
