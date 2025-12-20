from modules.middleware.master import *

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)

@router.get("/metrics", response_class=PlainTextResponse)
async def get_all_metrics():
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
        
        unique_label = datetime.now().strftime("%Y%m%dT%H%M%S_%f")
        if labels:
            labels["ts"] = unique_label
            labels_str = ', '.join([f'{k}="{v}"' for k, v in labels.items()])
            response.append(f'{c.metric}{{{labels_str}}} {valc}')
        else:
            response.append(f'{c.metric}{{ts="{unique_label}"}} {valc}')

    return '\n'.join(response)

@router.get("/metrics/types")
async def get_metric_types():
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