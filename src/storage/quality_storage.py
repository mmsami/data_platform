# src/storage/quality_storage.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Index
from .database import Base

class QualityCheckResult(Base):
    __tablename__ = "quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    check_name = Column(String, nullable=False)
    passed = Column(Boolean, nullable=False)
    message = Column(JSON)
    details = Column(JSON)

    __table_args__ = (
        Index('idx_quality_timestamp', timestamp.desc()),
        Index('idx_quality_source', source),
        Index('idx_quality_check_name', check_name)
    )