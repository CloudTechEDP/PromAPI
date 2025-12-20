# PromAPI – Métricas via HTTP (Push)

API simples para envio de métricas no formato Prometheus via HTTP, com suporte a **Gauge**, **Counter** e **Aggregate**.

---

## Subir a API

```bash
pip install --no-cache-dir -r requirements.txt
mkdir database/
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
ou via Docker

```bash
docker-compose up -d --build
```


---

## Gauge

### Características

* Métrica **única**
* **Sobrescreve** o valor anterior
* Representa estado atual

### Envio da métrica

```bash
echo 'gauge_metrics{label1="job",label2="instance"} 17' \
| curl --data-binary @- http://localhost:8001/metrics/job/gauge/myjob
```

### PromQL

```promql
gauge_metrics
```

### Gráficos recomendados (Grafana)

* Gauge
* Stat
* Time series (Last value)

### Casos de uso

* Uso de CPU
* Memória atual
* Status numérico
* Valores instantâneos

---

## Counter

### Características

* Sempre **incrementa**
* Nunca diminui
* Cada envio gera um novo ponto no tempo

### Envio da métrica

```bash
echo 'simple_counter_total{label1="job",label2="instance"} 1' \
| curl --data-binary @- http://localhost:8001/metrics/job/counter/myjob
```

### PromQL

```promql
increase(simple_counter_total[5m])
```

ou

```promql
rate(simple_counter_total[5m])
```

### Gráficos recomendados (Grafana)

* Time series
* Bar chart
* Stat (total acumulado)

### Casos de uso

* Número de requisições
* Erros
* Eventos
* Acessos

---

## Aggregate

### Características

* Soma todos os valores enviados para o mesmo conjunto de labels
* Funciona como acumulador customizado
* Ideal para agregações via push

### Envio da métrica

```bash
echo 'aggregate_total{type="counter",label1="job",label2="instance"} 1' \
| curl --data-binary @- http://localhost:8001/metrics/job/aggregate/myjob
```

### PromQL

```promql
increase(aggregate_total[1m])
```

ou (total acumulado)

```promql
aggregate_total
```

### Gráficos recomendados (Grafana)

* Time series
* Bar chart
* Table (múltiplas labels)

### Observações

* O `scrape_interval` do Prometheus deve ser **menor** que o intervalo usado no `increase`
* Em janelas muito curtas, picos podem aparentar duplicação

---

## Resumo rápido

| Tipo      | PromQL principal                | Gráfico recomendado       |
| --------- | ------------------------------- | ------------------------- |
| Gauge     | `gauge_metrics`                 | Gauge / Stat              |
| Counter   | `increase(counter[5m])`         | Time series               |
| Aggregate | `increase(aggregate_total[1m])` | Time series / Bar / Table |
