import os
import platform
import shutil
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import psutil


LOG_FILE = "logs/system_monitor.log"
CHECK_INTERVAL = 30
HEALTH_PORT = 8080

CPU_WARNING = 80
MEMORY_WARNING = 80
DISK_WARNING = 80


class HealthHandler(BaseHTTPRequestHandler):
    """Provide a simple Kubernetes health endpoint."""

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK\n")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Disable HTTP request logging."""
        return


def start_health_server():
    """Start the HTTP health server."""
    server = HTTPServer(("0.0.0.0", HEALTH_PORT), HealthHandler)
    server.serve_forever()


def get_system_metrics():
    """Collect current system metrics."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    disk_usage = (disk.used / disk.total) * 100

    return {
        "time": datetime.now(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": os.cpu_count(),
        "cpu_usage": cpu_usage,
        "disk_total": disk.total // (1024**3),
        "disk_used": disk.used // (1024**3),
        "disk_free": disk.free // (1024**3),
        "disk_usage": disk_usage,
        "memory_total": memory.total // (1024**3),
        "memory_used": memory.used // (1024**3),
        "memory_free": memory.available // (1024**3),
        "memory_usage": memory.percent,
    }


def format_metrics(metrics):
    """Format metrics and generate health alerts."""

    alerts = []

    if metrics["cpu_usage"] >= CPU_WARNING:
        cpu_status = "WARNING"
        alerts.append(f"High CPU usage: {metrics['cpu_usage']:.1f}%")
    else:
        cpu_status = "OK"

    if metrics["memory_usage"] >= MEMORY_WARNING:
        memory_status = "WARNING"
        alerts.append(f"High memory usage: {metrics['memory_usage']:.1f}%")
    else:
        memory_status = "OK"

    if metrics["disk_usage"] >= DISK_WARNING:
        disk_status = "WARNING"
        alerts.append(f"High disk usage: {metrics['disk_usage']:.1f}%")
    else:
        disk_status = "OK"

    overall_status = "WARNING" if alerts else "OK"

    output = (
        "=== Local Hybrid-Cloud System Monitor ===\n"
        f"Time: {metrics['time']}\n"
        f"OS: {metrics['os']}\n"
        f"CPU Cores: {metrics['cpu_cores']}\n"
        f"CPU Usage: {metrics['cpu_usage']:.1f}% [{cpu_status}]\n"
        f"Disk Total: {metrics['disk_total']} GB\n"
        f"Disk Used: {metrics['disk_used']} GB\n"
        f"Disk Free: {metrics['disk_free']} GB\n"
        f"Disk Usage: {metrics['disk_usage']:.1f}% [{disk_status}]\n"
        f"Memory Total: {metrics['memory_total']} GB\n"
        f"Memory Used: {metrics['memory_used']} GB\n"
        f"Memory Free: {metrics['memory_free']} GB\n"
        f"Memory Usage: {metrics['memory_usage']:.1f}% [{memory_status}]\n"
        f"Overall Health: {overall_status}\n"
        "Alerts:\n"
    )

    if alerts:
        for alert in alerts:
            output += f"- {alert}\n"
    else:
        output += "- No active alerts.\n"

    return output


def save_log(output):
    """Save monitoring output to the log file."""
    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as file:
        file.write(output)
        file.write("\n")


def main():
    """Start health server and continuously monitor the system."""

    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True,
    )
    health_thread.start()

    while True:
        metrics = get_system_metrics()
        output = format_metrics(metrics)

        print(output, flush=True)
        save_log(output)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
