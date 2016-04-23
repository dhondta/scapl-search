# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import os
import shlex
from celery.task import task
from celery.utils.log import get_task_logger
from config.generic_task import GENERIC_TASK_CONFIG, GENERIC_TASK_LOG_LEVEL
from subprocess import Popen, PIPE

logger = get_task_logger(__name__)

PLUGINS_ROOT = 'search'


@task(name=u'generic', bind=True)
def generic(self, cmd):
    if cmd is None:
        logger.debug("Task expiration message received")
        return u'Expiration set to 0'
    logger.info("Search task...")
    plugin = cmd.split('/')[0]
    cmd = os.path.join(PLUGINS_ROOT, cmd)
    logger.debug("Plugin: {}".format(plugin))
    logger.debug("Command: {}".format(cmd))
    options = ['--config', str(GENERIC_TASK_CONFIG), '--task', self.request.id]
    if GENERIC_TASK_LOG_LEVEL > 0:
        options.append('-' + 'v' * GENERIC_TASK_LOG_LEVEL)
    cmd = shlex.split(cmd)
    cmd.extend(options)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return {'output': out, 'error': err}
