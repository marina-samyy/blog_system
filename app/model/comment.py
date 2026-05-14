# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from app.core.database import Base

# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
#     parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

#     author = relationship("User", back_populates="comments")
#     post = relationship("Post", back_populates="comments")
#     parent = relationship("Comment", remote_side=[id], back_populates="replies")
#     replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign Keys
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

    # Relationships (FIXED NAMES MUST MATCH USER/POST MODELS)
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    # Self-referencing replies system
    parent = relationship(
        "Comment",
        remote_side=[id],
        back_populates="replies"
    )

    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan"
    )