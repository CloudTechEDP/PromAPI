from modules.middleware.master import *
from modules.schema.schemas import AggregateSchema

router = APIRouter()

@router.post("/metrics/job/aggregate/{job_name}")
async def increase_aggregate_metric(job_name: str, request: Request):
    try:
        raw_body = (await request.body()).decode()
        counter_name = raw_body.strip().split('{')[0]
        labels_part = re.search(r'\{(.*)\}', raw_body)
        labels = {}
        if labels_part:
            labels_str = labels_part.group(1)
            label_pairs = labels_str.split(',')
            for pair in label_pairs:
                key, value = pair.split('=')
                labels[key.strip()] = value.strip().strip('"')
        value = raw_body.strip().split()[-1]
        value = float(value)
        print_response(f"Parsed counter metric: name={counter_name}, labels={labels}, value={value}")
    except Exception as e:
        print_response(f"Error parsing counter metric: {e}")
        return {
            "error": "counter metric error", 
            "SendingFormat": 'counter_name{label1="value1",label2="value2"} value'
            }

    response = []
    db = SessionLocal()
    existing_metric = db.query(AggregateTable).filter_by(metric=counter_name, labels=labels).first()

    if existing_metric:
        current_value = existing_metric.value
        new_value = current_value + value
        value = new_value
        response = update_metric(existing_metric, value, db)
    else:
        table_class = AggregateTable
        response = add_metric_counter(table_class, counter_name, value, labels)
    return response
