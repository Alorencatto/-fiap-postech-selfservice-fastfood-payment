from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer


class BaseModel:
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def before_save(self, *args, **kwargs):
        print("Calling before save....")
        pass
