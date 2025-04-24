# src/storage/models.py
from sqlalchemy import Column, Integer, Float, DateTime, UniqueConstraint, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BTCPrice(Base):
    __tablename__ = 'btc_prices'

    # Use the sequence for id
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    price_timestamp = Column(DateTime, nullable=False)
    collected_at = Column(DateTime, nullable=False)

    # Let database handle uniqueness
    __table_args__ = (
        UniqueConstraint('price_timestamp', 'currency', name='unique_price_time_currency'),
    )
        
    
    def __repr__(self):
        return f"<BTCPrice(timestamp={self.price_timestamp}, price={self.price})>"
