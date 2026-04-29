from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, order, qr
from app.services.vector_service import create_embeddings
app = FastAPI(title="AI Restaurant Agent")
app.include_router(chat.router)
@app.on_event("startup")
def startup_event():
    #create_embeddings()

# ✅ CORS (important for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(order.router, prefix="/order", tags=["Order"])
app.include_router(qr.router, prefix="/qr", tags=["QR"])


# ✅ Root test
@app.get("/")
def root():
    return {"message": "AI Restaurant Agent Running 🚀"}
