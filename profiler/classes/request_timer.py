import datetime

class RequestTimer:

    def __init__(self):
        start_time = None
        end_time = None
        aggregate_time = datetime.timedelta(seconds=0)
    
    def start_timer(self):
        self.start_time = datetime.datetime.utcnow()
        self.aggregate_time = datetime.timedelta(seconds=0)

    def end_timer(self):
        self.end_time = datetime.datetime.utcnow()

    def get_elapsed_time(self):
        return datetime.datetime.utcnow() - self.start_time

    def get_final_time(self):
        return self.aggregate_time

    def restart_timer(self):
        self.aggregate_time = self.aggregate_time + self.get_elapsed_time()
        self.start_time = datetime.datetime.utcnow()
        self.end_time = None

