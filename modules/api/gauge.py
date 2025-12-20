from modules.middleware.master import *

router = APIRouter()
@router.post("/metrics/job/gauge/{job_name}")
async def receive_metric(job_name: str, request: Request):
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
    except Exception as e:
        return {
            "error": "counter metric error", 
            "SendingFormat": 'counter_name{label1="value1",label2="value2"} value'
            }
    
    response = []
    db = SessionLocal()
    existing_metric = db.query(GaugeTable).filter_by(metric=counter_name, labels=labels).first()
    if existing_metric:
        response = update_metric(existing_metric, value, db)
    else:
        table_class = GaugeTable
        response = add_metric_counter(table_class, counter_name, value, labels)
    return response




