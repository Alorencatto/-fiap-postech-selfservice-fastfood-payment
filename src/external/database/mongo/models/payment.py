from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.domain.enum.payment import PaymentStatusEnum
from src.external.database.sqlalchemy.models.base import BaseModel
from src.external.database.sqlalchemy.orm import Base


class PaymentDetailsModel(Base, BaseModel):
    __tablename__ = "payment_details"

    order_id = Column(Integer, ForeignKey("order_details.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    provider = Column(String(50))
    qr_data = Column(String(250))
    status = Column(Enum(PaymentStatusEnum))
    order = relationship("OrderDetailModel", lazy="joined")
    user = relationship("UserModel", lazy="joined")
