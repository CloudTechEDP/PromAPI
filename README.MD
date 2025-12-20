



clear && echo "simple_counter_total{label1="job", label2="instance"} 1" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/counter/myjob


clear && echo "gauge_metrics{label1="job", label2="instance"} 17" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/gauge/myjob

clear && echo "gauge_increase{label1="job", label2="instance"} 17" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/gauge/myjob

echo "aggregate_total{type="counter", label1="job", label2="instance"} 1" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/aggregate/myjob




####################################################
clear && echo "gauge_metrics{label1="job", label2="instance"} 17" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/gauge/myjob
metrica unica, sobrescreve o valor anterior
util em last, min, max, avg

####################################################


####################################################
clear && echo "simple_counter_total{label1="job", label2="instance"} 1" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/counter/myjob
metricas unicas, a cada metrica é adicionado um datetime pra tornar unica
util em count, sum, avg, min, max

####################################################
echo "aggregate_total{type="counter", label1="job", label2="instance"} 1" | curl --data-binary @- http://172.21.10.15:8001/metrics/job/aggregate/myjob

# aggregate_total
Mostra a soma de todos os valores enviados para a mesma label set.

# increase(aggregate_total[1m]) / 2
precisa de um prometheus scrap intervalo menor que o periodo de tempo usado na query.
Quando usados em timeseries, os contadores irao mostrar picos dentro desse periodo de tempo.
Em intervalos muito curtos, o valor as vezes é duplicado e deve ser dividido por 2.


####################################################


#!/bin/bash

END=$((SECONDS+600))   # 10 minutos (600s)

count=1

while [ $SECONDS -lt $END ]; do
    echo "aggregate_total{type=\"counter\", label1=\"job\", label2=\"instance\"} $count" | \
    curl --silent --data-binary @- http://172.21.10.15:8001/metrics/job/aggregate/myjob

    echo "Enviado valor: $count"
    count=$((count+1))
    sleep 7
done



pip install --no-cache-dir -r requirements.txt


uvicorn main:app --reload --host 0.0.0.0 --port 8001

curl --data-binary @gauge.txt http://localhost:8001/metrics/job/simple_job


echo "simple_counter_total 10" | curl --data-binary @- http://localhost:8001/metrics/job/other_job