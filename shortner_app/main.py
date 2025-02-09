import validators, qrcode
from fastapi import Depends, HTTPException, FastAPI, Request
from fastapi.responses import Response, RedirectResponse
from fastapi.params import Param
from sqlalchemy.orm import Session
from key import create_db_url, get_db_url_by_key
from table import Base
from structure import URLBase
from database import SessionLocal, engine

app = FastAPI(
    title="Short URL Generator",
    description=(
        "For generating short URLs with QR codes"
    ),
    docs_url="/",
    version="0.1"
)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=500, detail=message)
def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/create", tags=["Urlshortner"],
    summary="Generate a short url",
    response_description="Generated URL",)

async def create_url(db: Session = Depends(get_db),
        url: URLBase = Param(
            ...,
            description="Url to be encoded in QR code",
        )
)-> Response:
    """
    Generate short URL with QR code.

    """
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = create_db_url(db=db, url=url)
    db_url.url = db_url.key
    img = qrcode.make("http://127.0.0.1:8000/"+db_url.key)
    img.save('qrcode.png')
    return "http://127.0.0.1:8000/"+db_url.key

@app.get("/{url_key}", tags=["Use it"],
    summary="Get the final url",
    response_description="Target URL",)
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    if db_url := get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)