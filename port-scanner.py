import socket
import threading
from queue import Queue
import time

# اسکنر پورت ساده
class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, max_threads=100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.max_threads = max_threads
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()
    
    def scan_port(self, port):
        """اسکن یک پورت خاص"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f" port{port} is open")
            
            sock.close()
            
        except Exception as e:
            pass
    
    def worker(self):
        """تابع کارگر برای تردها"""
        while True:
            port = self.queue.get()
            self.scan_port(port)
            self.queue.task_done()
    
    def run_scan(self):
        """اجرای اسکن کامل"""
        print(f"start scanning ports for:{self.target}")
        start_time = time.time()
        
        # ایجاد تردهای کارگر
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
        
        # اضافه کردن پورتها به صف
        for port in range(self.start_port, self.end_port + 1):
            self.queue.put(port)
        
        # منتظر ماندن برای اتمام همه کارها
        self.queue.join()
        
        end_time = time.time()
        print(f"\ scan completed successfully : {end_time - start_time:.2f} sec")
        print(f" open ports:{sorted(self.open_ports)}")

# استفاده از اسکنر
if __name__ == "__main__":
    target = input(" Enter the address:(defoult: example.com or 192.168.1.1): ")
    start_port = int(input(" port start:(defoult: 1): ") or "1")
    end_port = int(input(" port end:(defoult: 1024): ") or "1024")
    threads = int(input(" terd number:(defoult: 100): ") or "100")
    
    scanner = PortScanner(target, start_port, end_port, threads)
    scanner.run_scan()

