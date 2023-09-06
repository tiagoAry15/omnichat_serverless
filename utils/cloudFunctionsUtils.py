import psutil


def log_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Memory in MB
    print(f"Function used approximately {memory_usage:.2f} MB")
