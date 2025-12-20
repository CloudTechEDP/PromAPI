from modules.middleware.master import *
from modules.model.model import *

engine = create_engine("sqlite:///database/metrics.db", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def add_metric_counter(table_class, counter_name: str, value: float, labels: dict):
    db = SessionLocal()
    metric = table_class( 
        metric=counter_name,
        value=value,
        labels=labels
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    db.close()

    return {
        "status": "stored",
        "id": metric.id,
        "metric": metric.metric,
        "value": metric.value,
        "labels": metric.labels
    }

def update_metric(existing_metric, value: float, db):
    # db = db
    existing_metric.value = value
    db.commit()
    db.refresh(existing_metric)
    db.close()
    return {
        "status": "updated",
        "id": existing_metric.id,
        "metric": existing_metric.metric,
        "value": existing_metric.value,
        "labels": existing_metric.labels
    }