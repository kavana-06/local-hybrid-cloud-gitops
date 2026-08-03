import os
import platform
import shutil
from datetime import datetime

import psutil


LOG_FILE = "logs/system_monitor.log"


def get_system_metrics():
    """Collect current system metrics."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total, used, free = shutil.disk_usage("/")

    return {
        "time": datetime.now(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": os.cpu_count(),
        "cpu_usage": cpu_usage,
        "disk_total": total // (1024**3),
        "disk_used": used // (1024**3),
        "disk_free": free // (1024**3),
        "memory_total": memory.total // (1024**3),
        "memory_used": memory.used // (1024**3),
        "memory_free": memory.available // (1024**3),
        "memory_usage": memory.percent,
    }


def format_metrics(metrics):
    """Format metrics for terminal output and logging."""
    return (
        "=== Local Hybrid-Cloud System Monitor ===\n"
        f"Time: {metrics['time']}\n"
        f"OS: {metrics['os']}\n"
        f"CPU Cores: {metrics['cpu_cores']}\n"
        f"CPU Usage: {metrics['cpu_usage']}%\n"
        f"Disk Total: {metrics['disk_total']} GB\n"
        f"Disk Used: {metrics['disk_used']} GB\n"
        f"Disk Free: {metrics['disk_free']} GB\n"
        f"Memory Total: {metrics['memory_total']} GB\n"
        f"Memory Used: {metrics['memory_used']} GB\n"
        f"Memory Free: {metrics['memory_free']} GB\n"
        f"Memory Usage: {metrics['memory_usage']}%\n"
    )


def save_log(output):
    """Save monitoring output to the log file."""
    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as file:
        file.write(output)
        file.write("\n")


def main():
    metrics = get_system_metrics()
    output = format_metrics(metrics)

    print(output)
    save_log(output)


if __name__ == "__main__":
    main()
