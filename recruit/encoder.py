from datetime import datetime
from django.db.models import Model
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
import time

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, (QuerySet, dict)):
            return tuple(o)
        elif isinstance(o, Model):
            return o.as_json()
        elif isinstance(o, datetime):
            # return o.strftime(DATETIME_FORMAT)
            return time.mktime(o.timetuple())
        else:
            return super(JSONEncoder, self).default(o)
