from django.db.models import Model
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return tuple(o)
        elif isinstance(o, Model):
            return o.as_json()
        else:
            return super(JSONEncoder, self).default(o)
