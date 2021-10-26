from abc import abstractmethod
from my_utils.Button import Button
from threading import Thread, Lock, Condition
import time

class EdgeDetector:
    def __init__(self, button: Button, lazy=True):
        self.button = button
        self.state = button.get_value()
        self.eLock = Lock()
        self.eCond = Condition()
        self.available_edges = 0
        self._poll_t = None
        self.lazy = lazy
        self.kill = False

        if not lazy:
            t = Thread(target=EdgeDetector._thread_poller, args=(self,))
            self._poll_t = t
            t.start()

    @staticmethod
    def _thread_poller(edge_detector):
        print(f"[not lazy] thread launched watching cap {edge_detector}")
        state = edge_detector.button.get_value()
        while True and not edge_detector.kill:
            cur_val = edge_detector.button.get_value()
            has_edge = not cur_val and state
            state = cur_val
            if has_edge:
                edge_detector.eLock.acquire()
                edge_detector.available_edges += 1
                edge_detector.eCond.acquire()
                edge_detector.eCond.notify_all()
                edge_detector.eCond.release()
                edge_detector.eLock.release()
            time.sleep(0.1)
        print(f"[not lazy] thread exit watching cap {edge_detector}")

    def num_edges(self):
        edges = None
        self.eLock.acquire()
        edges = self.available_edges
        self.eLock.release()
        return edges
    
    def process_edge(self):
        to_ret = False
        self.eLock.acquire()
        if self.available_edges > 0:
            self.available_edges -= 1
            to_ret = True
        self.eLock.release()
        return to_ret

    def reset_edges(self):
        to_ret = False
        self.eLock.acquire()
        self.available_edges = 0
        self.eLock.release()
        return to_ret

    def wait_for_edge(self):
        self.eCond.acquire()
        self.eCond.wait()
        self.eCond.release()

    def lazy_edge(self):
        cur_state = self.button.get_value()
        to_ret = False
        if self.state and not cur_state:
            to_ret = True
        self.state = cur_state
        return to_ret

    def delete(self):
        if not self.lazy:
            print("[not lazy] Cleaning up!")
            self.kill = True
