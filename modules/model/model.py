
from modules.middleware.master import *
Base = declarative_base()

class GaugeTable(Base):
    __tablename__ = "GaugeTable"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CounterTable(Base):
    __tablename__ = "CounterTable"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AggregateTable(Base):
    __tablename__ = "AggregateTable"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    



class histogram_metrics(Base):
    __tablename__ = "histogram_metric"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    buckets = Column(JSON, nullable=False)  # Store buckets as JSON
    sum = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class summary_metrics(Base):
    __tablename__ = "summary_metric"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    quantiles = Column(JSON, nullable=False)  # Store quantiles as JSON
    sum = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class info_metrics(Base):
    __tablename__ = "info_metric"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    info = Column(JSON, nullable=False)  # Store info as JSON
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class state_set_metrics(Base):
    __tablename__ = "state_set_metric"

    id = Column(Integer, primary_key=True)
    metric = Column(String(100), nullable=False)
    states = Column(JSON, nullable=False)  # Store states as JSON
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

