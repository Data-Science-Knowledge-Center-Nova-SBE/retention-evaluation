import time
from apscheduler.schedulers.background import BackgroundScheduler


class Timer():

    def __init__(self, display=True):
        self.display = display

        # start scheduler
        self.sched = BackgroundScheduler()
        if self.display:
            self.sched.add_job(self.display_print, 'interval', seconds=0.5)
        self.sched.start()

        # start chrono
        self.start = time.time()

    def stop(self):
        # stop scheduler
        self.sched.shutdown()

        # final print
        if self.display:
            self.display_print(done=True)

        return self.get_elapsed_time()

    def get_elapsed_time(self):
        # get chrono time
        end = time.time()

        # calc time
        elapsed_time = end - self.start
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        minutes_text = ""
        if minutes > 0:
            minutes_text = "{}m ".format(minutes)

        return "{}{}s".format(minutes_text, round(seconds, 1))

    def display_print(self, done=False):
        time = self.get_elapsed_time()

        # done
        done_text = ""
        end = "\r"
        if done:
            done_text = "done"
            end = "\n"

        # print updatable
        print("{} {}".format(time, done_text), end=end)
