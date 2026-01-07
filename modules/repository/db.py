from modules.middleware.master import *
from modules.model.model import *
os.makedirs("database", exist_ok=True)
engine = create_engine("sqlite:///database/metrics.db", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def add_metric_counter(table_class, counter_name: str, value: float, labels: dict):
    try:
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
    except Exception as e:
        db.close()
        return {
            "status": "error",
            "detail": str(e)
        }

def update_metric(existing_metric, value: float, db):
    try:
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
    except Exception as e:
        db.close()
        return {
            "status": "error",
            "detail": str(e)
        }

def log_error(error_message: str, raw_body: str, ia_solution: str):
    try:
        db = SessionLocal()
        error_log = error_logs(
            error_message=error_message,
            raw_body=raw_body,
            ia_solution=ia_solution
        )
        db.add(error_log)
        db.commit()
        db.refresh(error_log)
        db.close()
        return {
            "status": "logged",
            "id": error_log.id,
            "error_message": error_log.error_message,
            "raw_body": error_log.raw_body,
            "ia_solution": error_log.ia_solution,
            "timestamp": error_log.timestamp
        }
    except Exception as e:
        db.close()
        return {
            "status": "error",
            "detail": str(e)
        }