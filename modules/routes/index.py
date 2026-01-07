from modules.middleware.master import *

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def read_root():
    # with open("templates/index.html", encoding="utf-8") as f:
    #     html = f.read()
    # return HTMLResponse(content=html, status_code=200)

    """
    Render the application's index page using Jinja2 templates.
    
    Renders the "index.html" template from the "templates" directory with an empty request context.
    
    Returns:
        TemplateResponse: A response object rendering the "index.html" template.
    """
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": {}})

@router.get("/metrics", response_class=PlainTextResponse)
async def get_all_metrics():
    """
    Builds and returns a Prometheus-formatted metrics payload as a newline-separated string.
    
    This inspects stored gauge, aggregate (treated as counter), and counter metrics and emits metric lines and a single `# TYPE <metric> <type>` declaration for each metric name before its samples. Metric values that are whole-number floats are converted to integers. Metric labels stored as JSON strings are deserialized and rendered as `{key="value",...}`; when a counter has no labels, a `ts="<unique_label>"` label is added to the sample. If no metrics are found, the string contains the line `# No metrics available`.
    
    Returns:
        str: Prometheus text-format lines joined by newline characters.
    """
    db = SessionLocal()
    GaugeTable_list = db.query(GaugeTable).all()
    AggregateTable_list = db.query(AggregateTable).all()
    CounterTable_list = db.query(CounterTable).all()
    db.close()
    response = []
    emitted_types = set()
    
    # **Para métricas do tipo Gauge**
    for g in GaugeTable_list:
        val = int(g.value) if isinstance(g.value, float) and g.value.is_integer() else g.value
        labels = json.loads(g.labels) if isinstance(g.labels, str) else g.labels  # Desserializa labels

        if g.metric not in emitted_types:
            response.append(f"# TYPE {g.metric} gauge")
            emitted_types.add(g.metric)

        if labels:
            labels_str = ', '.join([f'{k}="{v}"' for k, v in labels.items()])
            response.append(f'{g.metric}{{{labels_str}}} {val}')
        else:
            response.append(f'{g.metric} {val}')
    
    # **Para métricas do tipo Aggregate (COUNTER)**
    for ag in AggregateTable_list:
        metric_name = ag.metric
        value = ag.value

        if metric_name not in emitted_types:
            response.append(f"# TYPE {metric_name} counter")
            emitted_types.add(metric_name)

        labels = json.loads(ag.labels) if isinstance(ag.labels, str) else ag.labels
        if labels:
            if isinstance(labels, dict):
                labels_str = ", ".join([f'{k}="{v}"' for k, v in labels.items()])
                response.append(f'{metric_name}{{{labels_str}}} {value}')
            else:
                response.append(f"{metric_name} {value}")
        else:
            response.append(f"{metric_name} {value}")

    # **Para métricas do tipo Counter**
    for c in CounterTable_list:
        valc = int(c.value) if isinstance(c.value, float) and c.value.is_integer() else c.value
        labels = json.loads(c.labels) if isinstance(c.labels, str) else c.labels  # Desserializa labels

        if c.metric not in emitted_types:
            response.append(f"# TYPE {c.metric} counter")
            emitted_types.add(c.metric)

        if labels:
            labels_str = ', '.join([f'{k}="{v}"' for k, v in labels.items()])
            response.append(f'{c.metric}{{{labels_str}}} {valc}')
        else:
            response.append(f'{c.metric}{{ts="{unique_label}"}} {valc}')

    if not response:
        response.append("# No metrics available")
    return '\n'.join(response)

@router.get("/error")
async def get_error_logs(request: Request):
    """
    Render the error logs page populated from the database.
    
    Queries the `error_logs` table, orders entries by descending timestamp, and renders the "error.html" template with the retrieved logs.
    
    Parameters:
        request (Request): FastAPI request object used for template rendering.
    
    Returns:
        TemplateResponse: A response rendering "error.html" with context key "error_message" containing a list of log objects. Each log object includes `id`, `error_message`, `raw_body`, `ia_solution`, and `timestamp` (ISO 8601 string).
    """
    db = SessionLocal()
    logs = db.query(error_logs).order_by(error_logs.timestamp.desc()).all()
    db.close()
    response = []
    for log in logs:
        response.append({
            "id": log.id,
            "error_message": log.error_message,
            "raw_body": log.raw_body,
            "ia_solution": log.ia_solution,
            "timestamp": log.timestamp.isoformat()
        })
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("error.html", {"request": request, "error_message": response})



@router.get("/metrics/types")
async def get_metric_types():
    """
    Return a mapping of metric names to their metric type.
    
    Scans the application's metric tables and builds a dict where each key is a metric name and each value is its type (one of "gauge", "counter", "histogram", "summary", "info", "state_set", or "aggregate").
    
    Returns:
        dict: Mapping from metric name (str) to metric type (str).
    """
    db = SessionLocal()
    types = {}
    for m in db.query(GaugeTable).all():
        types[m.metric] = "gauge"
    for m in db.query(CounterTable).all():
        types[m.metric] = "counter"
    for m in db.query(histogram_metrics).all():
        types[m.metric] = "histogram"
    for m in db.query(summary_metrics).all():
        types[m.metric] = "summary"
    for m in db.query(info_metrics).all():
        types[m.metric] = "info"
    for m in db.query(state_set_metrics).all():
        types[m.metric] = "state_set"
    for m in db.query(AggregateTable).all():
        types[m.metric] = "aggregate"
    db.close()
    return types