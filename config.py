import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

bind = '0.0.0.0:8000'
 # restart workers when code change, only use in development
#reload = True
preload_app = True
# debug when development and error when production
loglevel = 'error'
logfile = '/root/myproject/private-website/logs/debug.log'
accesslog = '/root/myproject/private-website/logs/access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = '/root/myproject/private-website/logs/error.log'
# process name
proc_name = 'cpblog' 
pidfile = '/root/myproject/private-website/logs/gunicorn.pid'
# set process daemon, not use in default
#daemon = True
# number of processes
workers = multiprocessing.cpu_count() * 2 + 1
# number of threads of per process
threads = multiprocessing.cpu_count() * 2
worker_class = 'gevent'