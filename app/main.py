from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Optional rate limit (slowapi) wiring - non-fatal if package missing
try:
    from slowapi import Limiter
    from slowapi.middleware import SlowAPIMiddleware
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
    slowapi_available = True
except Exception:
    limiter = None
    slowapi_available = False

from app.api.enfc_routes import router as enfc_router

app = FastAPI(title="dgii_encf", version="0.1.0")

# CORS: explicit allowed origins (example). Adjust as needed.
origins = [
    "https://enfc.getupsoft.com.do",
    "https://example-client.local",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach slowapi middleware if available
if slowapi_available and limiter:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

app.include_router(enfc_router)
