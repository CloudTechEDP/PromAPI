from modules.middleware.master import *
from modules.model.model import *
os.makedirs("database", exist_ok=True)
engine = create_engine("sqlite:///database/metrics.db", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def add_metric_counter(table_class, counter_name: str, value: float, labels: dict):
    """
    Persist a metric record using the provided ORM table class and return the operation result.
    
    Parameters:
        table_class: ORM model class used to create the metric record (must accept `metric`, `value`, and `labels`).
        counter_name (str): Name of the metric.
        value (float): Numeric value to store for the metric.
        labels (dict): Labels or metadata associated with the metric.
    
    Returns:
        dict: On success, a dictionary with keys:
            - "status": "stored"
            - "id": the new record's primary key
            - "metric": stored metric name
            - "value": stored metric value
            - "labels": stored labels
        On failure, a dictionary with keys:
            - "status": "error"
            - "detail": string describing the error
    """
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
    """
    Update the stored value of a metric record and persist the change.
    
    Parameters:
        existing_metric: ORM model instance representing the metric record to update.
        value (float): New numeric value to assign to the metric.
    
    Returns:
        dict: On success, a dictionary with keys "status" (value "updated"), "id", "metric", "value", and "labels".
              On failure, a dictionary with "status" set to "error" and "detail" containing the exception message.
    """
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
    """
    Persist an error log record to the database and return the stored entry's details.
    
    Parameters:
        error_message (str): A descriptive message for the error.
        raw_body (str): The raw request or payload associated with the error.
        ia_solution (str): The automated/AI-proposed solution or remediation for the error.
    
    Returns:
        dict: On success, a dictionary with `status` set to `"logged"` and keys `id`, `error_message`, `raw_body`, `ia_solution`, and `timestamp` containing the persisted record's values. On failure, a dictionary with `status` set to `"error"` and a `detail` string describing the exception.
    """
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