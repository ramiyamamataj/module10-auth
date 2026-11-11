from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.security import create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure FastAPI User Auth Application")

@app.get("/")
def read_root():
    return {"message": "User Auth and Database Service Running"}

@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = User.register(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not user.check_password(user_in.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}
