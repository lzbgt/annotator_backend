from background_task import background
from document import models as dm
from threading import Lock
from threading import get_ident
from logging import getLogger
from pymongo import MongoClient
from annotator import settings
from background_task.models import Task
from . import MONGO_CLIENT

logger = getLogger(__name__)

# helper func
def get_mongo_conn(pid, uri):
    client = MONGO_CLIENT.get(pid, None)
    lock = Lock()
    if client is None:
        # make a connection and make sure it's valid
        lock.acquire()
        # double checking
        if client is None:
            try:
                client = MongoClient(uri, waitQueueTimeoutMS=100)
                client.admin.command('ismaster')
                MONGO_CLIENT[pid] = client
                print("mongo: new connection")
                lock.release()
                return client
            except Exception as e:
                client = None
                lock.release()
                raise e
        else:
            lock.release()

    # using existing conn
    try:
        client.admin.command('ismaster')
        print("mongo: use existing connection")
        return client
    except:
        lock.acquire()
        try:
            # double check
            client.admin.command('ismaster')
            lock.release()
        except:
            # make new conn
            try:
                print('make new conn')
                del MONGO_CLIENT[pid]
                # may raise exception here
                client = MongoClient(uri, waitQueueTimeoutMS=100)
                client.admin.command('ismaster')
                MONGO_CLIENT[pid] = client
                lock.release()
            except Exception as e:
                client = None
                del MONGO_CLIENT[pid]
                lock.release()
                raise e

@background(schedule=0)
def load_document_from_mongodb(pid, skip, limit):
    project = dm.Project.objects.get(id=pid)
    client = get_mongo_conn(project.id, project.dburi)
    # load documents
    db = project.dburi.rfind('/')
    db = project.dburi[db+1:]
    db = client[db]
    c = project.content_field.find('.')
    f = project.content_field[c+1:]
    c = project.content_field[:c]
    c = db[c]
    r0 = c.find({}, {f:1}).skip(skip).limit(limit)
    cnt = 0
    for r in r0:
        cnt += 1
        try:
            doc = dm.Document(oid = r['_id'], project=project, content=r[f])
            doc.save()
        except Exception as e:
            logger.warn('exception: {}, project:{}, skip: {}, limit: {}, skip invalid record: {}'.format(e, project.id, skip, limit, r))

    #logger.debug('demo_task. message={0}'.format(message))
    if cnt  < limit:
        project.lastid -= limit - cnt
        project.save()


# ( 'name', func, 'description')
class Action:
    LOAD_DB = ('load_db', load_document_from_mongodb, 'load documents from source database')


# task schedular
@background(schedule=0)
def load_db_sche_task(req, repeat=300):
    task_name = __name__ + '.load_db_sche_task'
    print('task_name: {}'.format(task_name))

    action = req.get('action')
    if action == Action.LOAD_DB[0]:
        pid = req.get('pid')
        if pid is not None:
            logger.warn('calling task. action={}, pid={}'.format(Action.LOAD_DB, pid))
            lock = Lock()
            skip = 0
            # lock to modify lastid for race condition
            lock.acquire()
            project = dm.Project.objects.get(id=int(pid))
            limit = project.limit
            if limit == -1:
                try:
                    limit = settings.DB_READ_LIMIT
                except:
                    limit = 1000
            skip = project.lastid
            project.lastid += limit
            project.save()
            lock.release()
            load_document_from_mongodb(pid, skip, limit)

