import psutil



log_file_path = log_file_path = "venv/test.log" #path of log file







def collect_system_metric():
    metrics = {
        "cpu_percent" : psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

    return metrics

def parse_log_errors(log_file_path):
    error_count = 0

    try:
        with open(log_file_path,'r') as log_file:
            for line in log_file:
                if 'error' in line.lower():
                    error_count += 1
    except FileNotFoundError:
        error_count -= 1
    return error_count 

def collect_all_metrics(log_file_path):
    metrics = collect_system_metric()
    metrics["log_error_count"]  = parse_log_errors(log_file_path)
    return metrics

metrics = collect_all_metrics(log_file_path)
print(metrics)



