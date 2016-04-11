import logging
from satnogsclient.observer.observer import Observer
from satnogsclient.observer.worker import Worker

class Infogetter:

    _observer = Observer()
    _worker = Worker()
    
    def set_observer(self,observer):
        self._observer = observer
        
    def set_worker(self,worker):
        self._worker = worker
        
    def get_az(self):
        if self._worker:
            return self._worker.get_az()
        else:
            return -1
    
    