from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from ..application.services import BlockchainService

router = APIRouter()

def get_blockchain_service(request: Request) -> BlockchainService:
    return request.app.state.blockchain_service

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return request.app.state.templates.TemplateResponse(request=request, name="index.html")

@router.get("/configure", response_class=HTMLResponse)
async def configure(request: Request):
    return request.app.state.templates.TemplateResponse(request=request, name="configure.html")

@router.get("/transactions/get")
async def get_transactions(service: BlockchainService = Depends(get_blockchain_service)):
    transactions = [t.to_dict() for t in service.transactions]
    return {"transactions": transactions}

@router.get("/chain")
async def get_chain(service: BlockchainService = Depends(get_blockchain_service)):
    chain_data = [b.to_dict() for b in service.chain]
    return {"chain": chain_data, "length": len(chain_data)}

@router.get("/mine")
async def mine(service: BlockchainService = Depends(get_blockchain_service)):
    result = service.mine()
    return {
        "message": "New block created",
        **result
    }

@router.post("/transactions/new")
async def new_transaction(
    confirmation_sender_public_key: str = Form(...),
    confirmation_recipient_public_key: str = Form(...),
    transaction_signature: str = Form(...),
    confirmation_amount: str = Form(...),
    service: BlockchainService = Depends(get_blockchain_service)
):
    result = service.submit_transaction(
        confirmation_sender_public_key,
        confirmation_recipient_public_key,
        transaction_signature,
        confirmation_amount
    )
    if result is None:
        return JSONResponse(status_code=406, content={"message": "Invalid transaction/signature"})
    return JSONResponse(status_code=201, content={"message": f"Transaction will be added to the Block {result}"})

@router.get("/nodes/get")
async def get_nodes(service: BlockchainService = Depends(get_blockchain_service)):
    return {"nodes": list(service.p2p_client.nodes)}

@router.get("/nodes/resolve")
async def consensus(service: BlockchainService = Depends(get_blockchain_service)):
    replaced = service.resolve_conflicts()
    chain_data = [b.to_dict() for b in service.chain]
    if replaced:
        return {"message": "Our chain was replaced", "new_chain": chain_data}
    return {"message": "Our chain is authoritative", "chain": chain_data}

@router.post("/nodes/register")
async def register_node(nodes: str = Form(...), service: BlockchainService = Depends(get_blockchain_service)):
    node_list = nodes.replace(" ", "").split(",")
    if not node_list:
        return JSONResponse(status_code=400, content={"message": "Error: Please supply a valid list of nodes"})
    
    for node in node_list:
        service.p2p_client.register_node(node)

    return {
        "message": "Nodes have been added",
        "total_nodes": list(service.p2p_client.nodes),
    }
