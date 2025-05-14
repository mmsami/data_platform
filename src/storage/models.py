# src/storage/models.py
from sqlalchemy import Column, Integer, Float, DateTime, UniqueConstraint, String, Text, Index
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
        Index('idx_btc_price_timestamp', price_timestamp),
        Index('idx_btc_price_currency', currency),
        Index('idx_btc_price_composite', currency, price_timestamp.desc())
    )
        
    
    def __repr__(self):
        return f"<BTCPrice(timestamp={self.price_timestamp}, price={self.price})>"
    

class BitcoinNews(Base):
    __tablename__ = 'bitcoin_news'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text)
    link = Column(String)
    published_at = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    collected_at = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('title', 'published_at', name='unique_news'),
        Index('idx_news_published_at', published_at.desc()),
        Index('idx_news_source', source)
    )

