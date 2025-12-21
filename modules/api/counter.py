from modules.middleware.master import *

router = APIRouter()
@router.post("/metrics/job/counter/{job_name}")
async def receive_counter_metric(job_name: str, request: Request):
    try:
        raw_body = (await request.body()).decode()
        counter_name = raw_body.strip().split('{')[0]
        labels_part = re.search(r'\{(.*)\}', raw_body)
        unique_label = datetime.now().strftime("%Y%m%dT%H%M%S_%f")
        labels = {}
        labels["timestamp"] = unique_label

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

    table_class = CounterTable
    response = add_metric_counter(table_class, counter_name, value, labels)
    return response
