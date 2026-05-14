

# # import enum

# # from sqlalchemy import (
# #     Column,
# #     Integer,
# #     String,
# #     Enum,
# #     Boolean,
# #     DateTime,
# #     func
# # )
# # from sqlalchemy.orm import relationship

# # from app.core.database import Base


# # # ---------------- Role Enum ----------------
# # class Role(str, enum.Enum):
# #     admin = "admin"
# #     author = "author"
# #     reader = "reader"


# # # ---------------- User Model ----------------
# # class User(Base):
# #     __tablename__ = "users"

# #     id = Column(Integer, primary_key=True, index=True)

# #     username = Column(String(100), unique=True, index=True, nullable=False)
# #     email = Column(String(150), unique=True, index=True, nullable=False)

# #     hashed_password = Column(String(255), nullable=False)

# #     role = Column(
# #         Enum(Role, name="user_roles"),
# #         nullable=False,
# #         default=Role.reader,
# #         index=True
# #     )

# #     is_active = Column(Boolean, default=True)

# #     created_at = Column(
# #         DateTime,
# #         server_default=func.now(),
# #         nullable=False
# #     )

# #     updated_at = Column(
# #         DateTime,
# #         server_default=func.now(),
# #         onupdate=func.now(),
# #         nullable=False
# #     )

# #     # 🔥 ONLY ADDITION (DO NOT CHANGE ANYTHING ABOVE)
# #     posts = relationship("Post", back_populates="author")


# import enum

# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Enum,
#     Boolean,
#     DateTime,
#     func
# )
# from sqlalchemy.orm import relationship

# from app.core.database import Base


# class Role(str, enum.Enum):
#     admin = "admin"
#     author = "author"
#     reader = "reader"


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)

#     username = Column(String(100), unique=True, index=True, nullable=False)
#     email = Column(String(150), unique=True, index=True, nullable=False)

#     hashed_password = Column(String(255), nullable=False)

#     role = Column(
#         Enum(Role, name="user_roles"),
#         nullable=False,
#         default=Role.reader,
#         index=True
#     )

#     is_active = Column(Boolean, default=True)

#     created_at = Column(DateTime, server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

#     # العلاقات
#     posts = relationship("Post", back_populates="author")
#     comments = relationship("Comment", back_populates="user")


import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Role(str, enum.Enum):
    admin = "admin"
    author = "author"
    reader = "reader"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        Enum(Role, name="user_roles"),
        nullable=False,
        default=Role.reader,
        index=True
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # =========================
    # Relationships (FIXED)
    # =========================
    posts = relationship("Post", back_populates="author")

    # 🔥 IMPORTANT FIX: must match Comment.author
    comments = relationship("Comment", back_populates="author")