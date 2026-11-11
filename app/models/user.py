import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.security import hash_password, verify_password

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str):
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    @classmethod
    def register(cls, db, user_create_schema):
        existing_user = db.query(cls).filter(
            (cls.username == user_create_schema.username) | 
            (cls.email == user_create_schema.email)
        ).first()
        if existing_user:
            raise ValueError("Username or email already registered")
        
        user = cls(
            username=user_create_schema.username,
            email=user_create_schema.email
        )
        user.set_password(user_create_schema.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
