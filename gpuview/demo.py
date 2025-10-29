"""
Generates fake data for demoing the gpuview dashboard.
"""

import random
import uuid
from datetime import datetime
from typing import Any, Dict, List


def generate_fake_gpustat(hostname: str, gpu_name: str, num_gpus: int) -> Dict[str, Any]:
    """Generates a fake gpustat dictionary for a single host."""
    gpus = []
    for i in range(num_gpus):
        temp = random.randint(10, 90)
        if temp > 75:
            flag = "bg-danger"
        elif temp > 50:
            flag = "bg-warning"
        else:
            flag = "bg-success"

        mem_used = random.randint(1000, 24000)
        mem_total = 24576
        user_processes = ""
        for j in range(random.randint(1, 2)):
            process_type = random.choice(["python", "torch", "cuda", "nvprof"])
            process_memory = random.randint(1000, 24000)
            user_processes += f"user{j}({process_type}, {process_memory}M) "
        gpu = {
            "index": f"{i}",
            "uuid": str(uuid.uuid4()),
            "name": gpu_name,
            "temperature.gpu": temp,
            "utilization.gpu": random.randint(0, 100),
            "power.draw": random.randint(50, 350),
            "enforced.power.limit": 350,
            "memory.used": mem_used,
            "memory.total": mem_total,
            "memory": round(mem_used / mem_total * 100),
            "flag": flag,
            "users": random.randint(0, 3),
            "user_processes": user_processes,
        }
        gpus.append(gpu)

    return {
        "hostname": hostname,
        "gpus": gpus,
        "query_time": datetime.now().isoformat(),
    }


def get_demo_gpustats() -> List[Dict[str, Any]]:
    """Returns fresh demo data for all hosts - called each time for live refresh."""
    return [
        generate_fake_gpustat(hostname="demo-node-1", gpu_name="NVIDIA A100", num_gpus=4),
        generate_fake_gpustat(hostname="demo-node-2", gpu_name="NVIDIA H100", num_gpus=4),
        generate_fake_gpustat(hostname="demo-node-3", gpu_name="NVIDIA H200", num_gpus=4),
        generate_fake_gpustat(hostname="demo-node-4", gpu_name="NVIDIA L40S", num_gpus=4),
    ]


def get_demo_local_gpustat() -> Dict[str, Any]:
    """Returns fresh demo data for local host."""
    return generate_fake_gpustat(hostname="demo-node-1", gpu_name="NVIDIA A100", num_gpus=4)
