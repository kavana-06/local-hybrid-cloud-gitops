import os
import platform
import shutil
from datetime import datetime

import psutil


LOG_FILE = "logs/system_monitor.log"

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80


def get_system_metrics():
    """Collect current system metrics."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    total, used, free = shutil.disk_usage("/")

    disk_usage = (used / total) * 100

    return {
        "time": datetime.now(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": os.cpu_count(),
        "cpu_usage": cpu_usage,
        "disk_total": total // (1024**3),
        "disk_used": used // (1024**3),
        "disk_free": free // (1024**3),
        "disk_usage": disk_usage,
        "memory_total": memory.total // (1024**3),
        "memory_used": memory.used // (1024**3),
        "memory_free": memory.available // (1024**3),
        "memory_usage": memory.percent,
    }


def get_health_status(value, threshold):
    """Return health status based on a threshold."""
    if value >= threshold:
        return "WARNING"
    return "OK"


def get_alerts(metrics):
    """Generate alerts for resources exceeding thresholds."""
    alerts = []

    if metrics["cpu_usage"] >= CPU_THRESHOLD:
        alerts.append(
            f"ALERT: CPU usage is {metrics['cpu_usage']}%"
        )

    if metrics["memory_usage"] >= MEMORY_THRESHOLD:
        alerts.append(
            f"ALERT: Memory usage is {metrics['memory_usage']}%"
        )

    if metrics["disk_usage"] >= DISK_THRESHOLD:
        alerts.append(
            f"ALERT: Disk usage is {metrics['disk_usage']:.1f}%"
        )

    if not alerts:
        alerts.append("No active alerts.")

    return alerts


def format_metrics(metrics):
    """Format monitoring metrics and health status."""
    cpu_status = get_health_status(
        metrics["cpu_usage"], CPU_THRESHOLD
    )

    memory_status = get_health_status(
        metrics["memory_usage"], MEMORY_THRESHOLD
    )

    disk_status = get_health_status(
        metrics["disk_usage"], DISK_THRESHOLD
    )

    overall_status = (
        "WARNING"
        if "WARNING" in (cpu_status, memory_status, disk_status)
        else "OK"
    )

    alerts = get_alerts(metrics)

    output = (
        "=== Local Hybrid-Cloud System Monitor ===\n"
        f"Time: {metrics['time']}\n"
        f"OS: {metrics['os']}\n"
        f"CPU Cores: {metrics['cpu_cores']}\n"
        f"CPU Usage: {metrics['cpu_usage']}% [{cpu_status}]\n"
        f"Disk Total: {metrics['disk_total']} GB\n"
        f"Disk Used: {metrics['disk_used']} GB\n"
        f"Disk Free: {metrics['disk_free']} GB\n"
        f"Disk Usage: {metrics['disk_usage']:.1f}% [{disk_status}]\n"
        f"Memory Total: {metrics['memory_total']} GB\n"
        f"Memory Used: {metrics['memory_used']} GB\n"
        f"Memory Free: {metrics['memory_free']} GB\n"
        f"Memory Usage: {metrics['memory_usage']}% [{memory_status}]\n"
        f"Overall Health: {overall_status}\n"
        "Alerts:\n"
    )

    for alert in alerts:
        output += f"- {alert}\n"

    return output


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
