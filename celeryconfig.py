import os
import sys

from kombu import Queue, Exchange

sys.path.insert(0, os.getcwd())

class ScaplRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
	print task
        if task == 'GenericSearch':
	    return {'exchange': 'scapl',
                    'exchange_type': 'topic',
                    'routing_key': 'se.task'}
	if task == 'Sleep':
	    return {'exchange': 'scapl',
                    'exchange_type': 'topic',
                    'routing_key': 'as.task'}
        return None

CELERY_TIMEZONE = 'Europe/Paris'

default_exchange = Exchange('default', type='direct')
scapl_exchange = Exchange('scapl', type='topic')
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default',default_exchange, routing_key='default'),
    Queue('mq_se', scapl_exchange, routing_key='se.#'),
)

CELERY_IGNORE_RESULT = False
BROKER_URL = 'amqp://scapl:scapl@localhost:5672/vScapl'
#BROKER_URL = 'redis://localhost:6379/10'

CELERY_DEFAULT_EXCHANGE = 'scapl'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_ROUTES = (ScaplRouter(), )
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TASK_RESULT_EXPIRES=3600
CELERY_IMPORTS = ('tasks',)
CELERY_RESULT_BACKEND = 'amqp'
#CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/11'
#CELERY_RESULT_BACKEND = 'mongodb://localhost:27017/'
#CELERY_MONGODB_BACKEND_SETTINGS = {
#    'database': 'celery',
#    'taskmeta_collection': 'my_taskmeta_collection',
#}
#CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

