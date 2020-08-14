import schedule
import threading
import time

class Scheduler:
  def __init__(self, modules):
    for module in modules:
      schedule_config = module.config['schedule']
      schedule_job = schedule.every(schedule_config.get('every', 1))

      for key in schedule_config:
        if key == 'every' or key == 'at':
          continue

        value = schedule_config[key]
        attr = getattr(schedule_job, key)

        if value is None:
          schedule_job = attr
        else:
          schedule_job = attr(value)
        
      if 'at' in schedule_config:
        value = schedule_config['at']
        schedule_job = getattr(schedule_job, 'at')(value)
      
      schedule_job.do(module.execute)

  def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
      @classmethod
      def run(cls):
        while not cease_continuous_run.is_set():
          schedule.run_pending()
          time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    self.cease_continuous_run = cease_continuous_run

  def shutdown(self):
    self.cease_continuous_run.set()