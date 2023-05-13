import subprocess
import getpass
import requests
import json
import time
import argparse


def get_gpu_usage():
    """
    Returns a dict which contains information about memory usage for each GPU.
    In the following output, the GPU with id "0" uses 5774 MB of 16280 MB.
    253 MB are used by other users, which means that we are using 5774 - 253 MB.
    {
        "0": {
            "used": 5774,
            "used_by_others": 253,
            "total": 16280
        },
        "1": {
            "used": 5648,
            "used_by_others": 253,
            "total": 16280
        }
    }
    """

    # Name of current user, e.g. "root"
    current_user = getpass.getuser()

    # Find mapping from process ids to usernames
    command = ["ps", "axo", "pid,user"]
    output = subprocess.check_output(command).decode("utf-8")
    pid_user = dict(row.strip().split() for row in output.strip().split("\n")[1:])

    # Find all GPUs and their total memory
    command = ["nvidia-smi", "--query-gpu=index,memory.total", "--format=csv"]
    output = subprocess.check_output(command).decode("utf-8")
    total_memory = dict(row.replace(",", " ").split()[:2] for row in output.strip().split("\n")[1:])

    # Store GPU usage information for each GPU
    gpu_usage = {f'{gpu_id}': {"used": 0, "used_by_others": 0, "total memory in MB": int(total)}
                 for gpu_id, total in total_memory.items()}

    # Use nvidia-smi to get GPU memory usage of each process
    command = ["nvidia-smi", "pmon", "-s", "m", "-c", "1"]
    output = subprocess.check_output(command).decode("utf-8")
    for row in output.strip().split("\n"):
        if row.startswith("#"):
            continue

        gpu_id, pid, type, mb, command = row.split()

        # Special case to skip weird output when no process is running on GPU
        if pid == "-":
            continue

        gpu_usage[gpu_id]["used"] += int(mb)

        # If the GPU user is different from us
        if pid_user[pid] != current_user:
            gpu_usage[gpu_id]["used_by_others"] += int(mb)

    return gpu_usage


def get_free_gpus(max_usage_by_others_mb=1024):
    """
    Returns the ids of GPUs which are occupied to less than 1 GB by other users.
    """

    return [gpu_id for gpu_id, usage in get_gpu_usage().items()
            if usage["used_by_others"] < max_usage_by_others_mb and usage["used"] < max_usage_by_others_mb]


if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process webhook URL.')

    # Add the webhook URL argument
    parser.add_argument('--webhook_url', help='The URL of the webhook.')

    # Add the monitor interval argument as seconds
    parser.add_argument('--seconds', type=int, help='The number of seconds to wait before sending the next webhook.')

    # Add optional arg for users to choose max usage by others
    parser.add_argument('--max_usage_by_others_gb', type=float, default=1.0, help='The maximum usage by others in MB.')

    # Parse the command-line arguments
    args = parser.parse_args()
    webhook_url = args.webhook_url
    max_usage_by_others_mb = args.max_usage_by_others_gb * 1024

    while True:
        print("GPU memory usage information:")
        print(json.dumps(get_gpu_usage(), indent=4))
        print()
        free_gpus = get_free_gpus(max_usage_by_others_mb)
        print("GPU ids of free GPUs:", free_gpus)

        if free_gpus:
            hostname = subprocess.check_output(['hostname'])
            headers = {
                "content-type": "application/json"
            }
            data = {
                "content": f"""
                ```GPU free: {free_gpus}```
                """,
                "username": hostname.decode()
            }
            res = requests.post(webhook_url, headers=headers, json=data)
            res.raise_for_status()

        time.sleep(args.seconds)
