from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func

class Base(DeclarativeBase):
    pass

class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order: Mapped[str] = mapped_column(String(20), index=True)
    tag: Mapped[str | None] = mapped_column(String(20))
    result: Mapped[str] = mapped_column(String(50))
    scanned_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
