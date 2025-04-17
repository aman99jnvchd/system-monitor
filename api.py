import os
from fastapi import FastAPI
from modules.metrics import SystemMetrics
import logging

app = FastAPI()
metrics = SystemMetrics()

# create log directory
try: os.mkdir('logs')
except: pass
# Log to a file
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.get("/metrics")
def get_metrics():
    data = metrics.get_all_metrics()
    logging.info(f"API called - Data: {data}")
    return data
