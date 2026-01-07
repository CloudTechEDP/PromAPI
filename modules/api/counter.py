from modules.middleware.master import *

router = APIRouter()
@router.post("/metrics/job/counter/{job_name}")
async def receive_counter_metric(job_name: str, request: Request):
    """
    Parse a Prometheus-style counter metric from the request body, add it to the counter table, and return the insertion result.
    
    The request body must contain a metric line like:
        metric_name{key="value",other="v"} 123
    This function extracts the metric name, optional labels, and numeric value, adds a generated "timestamp" label, and calls the metric storage routine. On error, returns a StreamingResponse that streams a diagnostic message (including an automated analysis) instead of the normal result.
    
    Parameters:
        job_name (str): Job identifier from the request path; used to associate the metric with a job.
        request (Request): Incoming HTTP request whose body contains the metric line described above.
    
    Returns:
        The value returned by add_metric_counter (typically an insertion/acknowledgement response), or a StreamingResponse that yields diagnostic information when parsing or storage fails.
    """
    raw_body = (await request.body()).decode()
    try:
        
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
        raw_body = raw_body.replace('\r', '').replace('\n', '')
        async def error_stream():
            """
            Yield diagnostic text chunks describing why the metric failed and a Gepeto analysis.
            
            This async generator produces a sequence of text fragments intended for streaming back to the client:
            - First yields a Portuguese status message indicating the metric failed and Gepeto will be consulted.
            - Then yields the analysis returned by ask_gepeto(error, raw_body).
            - If an exception occurs while producing the analysis, yields a JSON-formatted error string with a "status" of "error" and a "detail" message.
            
            Returns:
                str: Successive string chunks to stream to the client (status message, analysis, or error JSON).
            """
            try:
                yield 'Sua Metrica nao funcionou:\nVou usar o Gepeto para tentar entender o problema e propor uma solução...\n\n\n'
                iause = ask_gepeto(error, raw_body)
                yield f'Segue o que conseguimos entender:\n {iause}\n'
            except Exception as err:
                yield f'{{"status": "error", "detail": "{str(err)}"}}\n'
        return StreamingResponse(error_stream(), media_type="text/json")

