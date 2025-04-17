import psutil

class SystemMetrics:
    def __init__(self):
        self.prev_bytes_sent, self.prev_bytes_recv = self.get_network_data()

    def get_cpu(self):
        return psutil.cpu_percent()

    def get_memory(self):
        return psutil.virtual_memory().percent

    def get_disk(self):
        return psutil.disk_usage('/').percent

    def get_network_data(self):
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent, net_io.bytes_recv

    def get_network_speed(self):
        new_sent, new_recv = self.get_network_data()
        upload = (new_sent - self.prev_bytes_sent) / 1024 / 2  # KB/s
        download = (new_recv - self.prev_bytes_recv) / 1024 / 2
        self.prev_bytes_sent, self.prev_bytes_recv = new_sent, new_recv
        return f"{upload:.1f}", f"{download:.1f}"

    def get_all_metrics(self):
        return {
            "cpu": float(self.get_cpu()),
            "memory": float(self.get_memory()),
            "disk": float(self.get_disk()),
            "network": {
                "upload_kbps": float(self.get_network_speed()[0]),
                "download_kbps": float(self.get_network_speed()[1])
            }
        }
