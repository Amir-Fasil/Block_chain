from fastapi import FastAPI, Request
from Block_Chain import Block_chain
from queue import Queue
from Functions import mine_block, create_transaction, create_block

async def lifespan(app: FastAPI):
    app.block_chain = Block_chain()
    app.transaction_queue = Queue()
    app.numTransacInBlock = 2
    app.verified_transaction = []
    yield
    app.verified_transaction.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/chain")
async def return_block_chain(request: Request):
    return request.app.block_chain.get_header()
@app.post("/mine-block")
async def mine_block(request: Request, miner_pubKey: str, amount: float):
    mine_block(request, miner_pubKey, amount)
@app.post("/new-transaction")
async def create_new_transaction(request, input_Privkey: str, input_PubKey: str, output_PubKey: str, needed_amount: float):
    create_transaction(request, input_Privkey, input_PubKey, output_PubKey, needed_amount)
@app.post("/add-block")
async def add_block(request: Request):
    create_block(request)
