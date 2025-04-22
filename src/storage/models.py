# src/storage/models.py
from sqlalchemy import Column, Integer, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BTCPrice(Base):
    __tablename__ = 'btc_prices'

    # Use the sequence for id
    id = Column(Integer, primary_key=True)
    price_eur = Column(Float, nullable=False)
    price_timestamp = Column(DateTime, nullable=False) # When the price was recorded
    collected_at = Column(DateTime, nullable=False) # When we collected the data

    # Let database handle uniqueness
    __table_args__ = (
        UniqueConstraint('price_timestamp', name='unique_price_timestamp'),
    )
        
    
    def __repr__(self):
        return f"<BTCPrice(timestamp={self.price_timestamp}, price_eur={self.price_eur})>"
