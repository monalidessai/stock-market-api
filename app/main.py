from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models, auth, services

app = FastAPI(title="Advanced Stock API 🚀")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed = auth.hash_password(password)
    user = models.User(username=username, password=hashed)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token}


@app.get("/price/{symbol}")
def stock_price(symbol: str):
    price = services.get_current_price(symbol)

    if price is None:
        raise HTTPException(status_code=404, detail="Invalid stock symbol")

    return {"symbol": symbol.upper(), "price": price}