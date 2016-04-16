from __future__ import absolute_import
from celery.task import task, Task
from celery.utils.log import get_task_logger
import subprocess

logger = get_task_logger(__name__)


class DebugTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        print('Task returned: {0!r}'.format(self.request))

@task(base=DebugTask, name="generic")
def generic(apl_keywords, item_api, item_keywords, item_ns, *args):
    logger.info("Search task...")
    keywords = ",".join([apl_keywords, item_keywords])
    cmd = 'search/' + item_api.format(keywords=keywords, suggestions=item_ns)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    result = {
        'output': out,
        'error': err,
    }
    
    return result

