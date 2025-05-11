from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, nullable=False)
    commission = Column(Text)
    type = Column(CHAR(1))
    shippingConditionId = Column(Integer)
    
    # Relationship with OrderItems
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'OrderItems'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'), nullable=False)
    sku = Column(Text)
    name = Column(Text)
    text = Column(Text)
    quantity = Column(Float)
    quantityUnit = Column(Text)
    price = Column(Float)
    priceUnit = Column(Text)
    purchasePrice = Column(Float)
    commission = Column(Text)

    # Relationship with Order
    order = relationship("Order", back_populates="items") 