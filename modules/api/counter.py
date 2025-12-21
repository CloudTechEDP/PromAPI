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
        table_class = CounterTable
        response = add_metric_counter(table_class, counter_name, value, labels)
        return response
    except Exception as exc:
        error = str(exc)
        raw_body = (await request.body()).decode().replace('\r', '').replace('\n', '')
        async def error_stream():
            try:
                yield 'Sua Metrica nao funcionou:\nVou usar o Gepeto para tentar entender o problema e propor uma solução...\n\n\n'
                iause = ask_gepeto(error, raw_body)
                yield f'Segue o que conseguimos entender:\n {iause}\n'
            except Exception as err:
                yield f'{{"status": "error", "detail": "{str(err)}"}}\n'
        return StreamingResponse(error_stream(), media_type="text/json")


