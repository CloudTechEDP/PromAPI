from modules.middleware.master import *
from modules.schema.schemas import AggregateSchema

router = APIRouter()

@router.post("/metrics/job/aggregate/{job_name}")
async def increase_aggregate_metric(job_name: str, request: Request):
    """
    Handle an incoming aggregate metric line for the given job and update or create the corresponding metric record.
    
    Parses a Prometheus-style metric text from the request body (name, optional labels, and numeric value), then increments an existing aggregate metric by the parsed value or creates a new aggregate metric record if none exists. On error, returns a StreamingResponse that yields a JSON-formatted diagnostic narrative produced by an analysis helper.
    
    Parameters:
        job_name (str): The job name path parameter associated with the metric.
        request (Request): The incoming HTTP request whose body contains the metric line.
    
    Returns:
        The updated or newly created aggregate metric result (database model or API response), or a StreamingResponse that yields JSON diagnostics when parsing or processing fails.
    """
    raw_body = (await request.body()).decode()
    try:
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
        response = []
        db = SessionLocal()
        existing_metric = db.query(AggregateTable).filter_by(metric=counter_name, labels=labels).first()

        if existing_metric:
            current_value = existing_metric.value
            new_value = current_value + value
            value = new_value
            response = update_metric(existing_metric, value, db)
        else:
            db.close()
            table_class = AggregateTable
            response = add_metric_counter(table_class, counter_name, value, labels)
        return response
    except Exception as exc:
        error = str(exc)
        raw_body = raw_body.replace('\r', '').replace('\n', '')
        async def error_stream():
            """
            Produce streamed textual messages describing a metric failure and an attempted Gepeto analysis.
            
            Yields:
                str: A sequence of text chunks for a streaming HTTP response:
                    - An initial Portuguese message stating the metric failed and that Gepeto will be used.
                    - Gepeto's analysis or proposal based on the provided error and raw_body.
                    - If an exception occurs while obtaining the analysis, a JSON-formatted error detail string.
            """
            try:
                yield 'Sua Metrica nao funcionou:\nVou usar o Gepeto para tentar entender o problema e propor uma solução...\n\n\n'
                iause = ask_gepeto(error, raw_body)
                yield f'Segue o que conseguimos entender:\n {iause}\n'
            except Exception as err:
                yield f'{{"status": "error", "detail": "{str(err)}"}}\n'
        return StreamingResponse(error_stream(), media_type="text/json")

