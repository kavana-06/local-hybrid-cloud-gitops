import os
import platform
import shutil
from datetime import datetime

print("=== Local Hybrid-Cloud System Monitor ===")
print(f"Time: {datetime.now()}")
print(f"OS: {platform.system()} {platform.release()}")
print(f"CPU Cores: {os.cpu_count()}")

total, used, free = shutil.disk_usage("/")

print(f"Disk Total: {total // (1024**3)} GB")
print(f"Disk Used: {used // (1024**3)} GB")
print(f"Disk Free: {free // (1024**3)} GB")

import psutil

memory = psutil.virtual_memory()

print(f"Memory Total: {memory.total // (1024**3)} GB")
print(f"Memory Used: {memory.used // (1024**3)} GB")
print(f"Memory Free: {memory.available // (1024**3)} GB")
print(f"Memory Usage: {memory.percent}%")
