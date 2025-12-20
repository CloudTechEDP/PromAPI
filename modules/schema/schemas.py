from modules.middleware.master import *


class AggregateSchema(BaseModel):
    metric: str = Field(
        example="simple_counter_total",
        description="Nome da métrica Prometheus"
    )
    labels: Optional[dict[str, str]] = Field(
        default=None,
        example=None,
        description="Labels opcionais da métrica"
    )
    value: float = Field(
        example=1,
        description="Valor da métrica"
    )
    raw_data: str = Field(
        example="simple_counter_total 1",
        description="Métrica no formato Prometheus exposition (text/plain)"
    )
