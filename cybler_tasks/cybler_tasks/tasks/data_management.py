"""
Denotes tasks for data management and manipulation tasks
"""

from cybler_tasks.data.cybler_api import CyblerAPI
from celery import task

import httplib2

@task
def duplicate_remove():
    start = 0
    data = CyblerAPI().get("listing", rows=40, start=start)
    ids = []
    urls = []
    dupes = []
    while(len(data) != 0):
        for entry in data:
            if data["_id"] in ids or data["url"] in urls:
                dupes.append(data["_id"])
            else:
                ids.append(data["_id"])
                urls.append(data["url"])
        start += 40
        data = CyblerAPI().get("listing", rows=40, start=start)

    #Now delete them
    for dupe in dupes:
        print "Deleting %s" % str(dupe)
        CyblerAPI().delete("listing", dupe)        
        
