import time
from modules.metrics import SystemMetrics

def run_cli():
    """ Run system usage monitoring in command line """
    system_metrics = SystemMetrics()
    try:
        while True:
            data = system_metrics.get_all_metrics()
            cpu = data['cpu']
            memory = data['memory']
            disk = data['disk']
            upload_speed = data['network']['upload_kbps']
            download_speed = data['network']['download_kbps']        
            
            # Clear line and print with fixed-width formatting
            output = (
                f"\r\033[KCPU: {cpu:5.1f}% | "
                f"Memory: {memory:5.1f}% | "
                f"Disk: {disk:5.1f}% | "
                f"Upload: {upload_speed:6.1f} KB/s | "
                f"Download: {download_speed:6.1f} KB/s"
            )
            print(output, end='', flush=True)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
