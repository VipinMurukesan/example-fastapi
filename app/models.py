from sqlalchemy import Column, Integer, String, Boolean, DateTime, sql, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True")
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    owner_id = Column(
        Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "vote"

    post_id = Column(
        Integer, ForeignKey("post.id", ondelete="cascade"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="cascade"), primary_key=True
    )


# id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")
