from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from background_task.models import Task
import json

from .tasks import *
from threading import Lock
from datetime import datetime, timedelta

logger = getLogger(__name__)

SCHED_TASK_NAME = 'annotator.tasks.load_db_sche_task'
DEFAULT_REPEAT_SEC = 60

@csrf_exempt
def tasks(request):
    if request.method == 'POST':
        return _post_tasks(request)
    else:
        return JsonResponse({'code': 400, 'msg': 'only supports http POST'}, status=400)

def _post_tasks(request):
    try:
        req = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'error: {}, data:{}'.format(e.msg, e.doc)})
    action = req.get('action')
    if action == 'load_db':
        repeat = req.get('interval', -1)
        if repeat == -1:
            try:
                repeat = settings.BACKGROUND_TASK_LOAD_DB_REPEAT
            except:
                repeat = DEFAULT_REPEAT_SEC

        # delete duplicated task
        qs = Task.objects.filter(task_name=SCHED_TASK_NAME).order_by('-id')
        for q in qs:
            print('load_db_sche_task: duplicated instances, cleaning id:', q.id)
            q.delete()

        load_db_sche_task(req, repeat=repeat)
        return JsonResponse({'code': 200, 'msg': 'task submitted'}, status=200)
    elif action == 'status_load_db':
        delta = datetime.now() - timedelta(hours=1)
        qs = Task.objects.filter(task_name=SCHED_TASK_NAME, run_at__gt=delta, )
        if qs.count() > 0:
            params = json.loads(qs[0].task_params)
            pid = req.get("pid")
            if params[0][0]["pid"] == pid and pid is not None:
                return JsonResponse({'code': 200, 'running': True, 'msg': 'task running'}, status=200)
        else:
            return JsonResponse({'code': 200, 'running': False ,'msg': 'task is not running'}, status=200)
    return JsonResponse({'code': 400, 'msg': 'unknown operation'}, status=400)

