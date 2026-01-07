from modules.middleware.master import *

router = APIRouter()
@router.post("/metrics/job/gauge/{job_name}")
async def receive_metric(job_name: str, request: Request):
    """
    Parse a Prometheus-style gauge payload, persist or update the metric, and return the operation result.
    
    Parameters:
    	job_name (str): The job identifier path parameter (not used for parsing).
    	request (Request): The incoming HTTP request whose body contains the metric payload.
    
    Description:
    	Parses the raw request body to extract:
    	- counter name: the substring before the first '{' (trimmed).
    	- labels: key="value" pairs found inside the first pair of braces, returned as a dict of strings.
    	- value: the last whitespace-separated token parsed as a float.
    	The function attempts to find an existing gauge metric matching the parsed name and labels; if found, it updates that metric, otherwise it creates a new metric entry.
    
    Returns:
    	The result of the database update or creation operation, or a StreamingResponse that yields JSON-formatted diagnostic messages when an error occurs.
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
        response = []
        db = SessionLocal()
        existing_metric = db.query(GaugeTable).filter_by(metric=counter_name, labels=labels).first()
        if existing_metric:
            response = update_metric(existing_metric, value, db)
        else:
            db.close()
            table_class = GaugeTable
            response = add_metric_counter(table_class, counter_name, value, labels)
        return response
    except Exception as exc:
        error = str(exc)
        raw_body = raw_body.replace('\r', '').replace('\n', '')
        async def error_stream():
            """
            Asynchronously yields diagnostic messages for a failed metric ingestion.
            
            Yields an initial Portuguese notice about the metric failure, then yields an analysis string produced for the failure; if an error occurs while generating the analysis, yields a JSON-formatted error object string with `status` and `detail`.
            
            Returns:
                Async generator that yields `str` values: an initial notice, an analysis message, or a JSON error object string.
            """
            try:
                yield 'Sua Metrica nao funcionou:\nVou usar o Gepeto para tentar entender o problema e propor uma solução...\n\n\n'
                iause = ask_gepeto(error, raw_body)
                yield f'Segue o que conseguimos entender:\n {iause}\n'
            except Exception as err:
                yield f'{{"status": "error", "detail": "{str(err)}"}}\n'
        return StreamingResponse(error_stream(), media_type="text/json")



