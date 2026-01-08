from enum import unique
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text, Index
from typing import Optional
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, comment="created time")
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="updated time")


class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="category id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="category name")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, comment="sort order")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"


class News(Base):
    __tablename__ = "news"

    __table_args__ = (
        Index("fk_news_category_idx", "category_id"), # high query situation
        Index("idx_publish_time", "publish_time"), # sort by publish time
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="news id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="news title")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="news description")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="news content")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="news image")
    author: Mapped[Optional[str]] = mapped_column(String(100), comment="news author")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), nullable=False, comment="category id")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="news views")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="news published time")
    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, category_id={self.category_id})>"
