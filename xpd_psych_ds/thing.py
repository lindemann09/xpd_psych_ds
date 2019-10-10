from collections import OrderedDict
from copy import copy
import json

class Thing():

    def __init__(self, type):

        self._info = [OrderedDict()] * 3 # optional, recommended, required
        self.add_required("@type", type)


    def has_field(self, field):
        return field in self._info[0] or field in self._info[1] or \
            field in self._info[2]

    def _add(self, field, value, requirement_level):
        # add a property field and value
        if self.has_field(field):
            raise ValueError("{} is already defined. Please use update for "
                             "changes.".format(field))

        self._info[requirement_level][field] = value

    def add_required(self, field, value):
        return self._add(field, value, requirement_level=2)

    def add_multiple_required(self, list_of_tuples):
        # add multiple required properties (field and values)
        for k,v in list_of_tuples:
            self._add(k, v, requirement_level=2)

    def add_recommended(self, field, value):
        return self._add(field, value, requirement_level=1)

    def add_multiple_recommended(self, list_of_tuples):
        # add multiple recommended properties (field and values)
        for k,v in list_of_tuples:
            self._add(k, v, requirement_level=1)

    def add(self, field, value):
        # add an optional field
        return self._add(field, value, requirement_level=0)

    def add_multiple_optional(self, list_of_tuples):
        # add multiple recommended properties (field and values)
        for k,v in list_of_tuples:
            self._add(k, v, requirement_level=1)

    def _get_dict(self, requirement_level):
        # returns serialized dict
        rtn = copy(self._info[requirement_level])
        for k, v in rtn.items():
            rtn[k] = _serialize(v)
        return rtn

    def get_all(self):

        d = self.get_required()
        d.update(self.get_recommended())
        d.update(self.get_optional())
        return d

    def get_required(self):
        return self._get_dict(requirement_level=2)

    def get_recommended(self):
        return self._get_dict(requirement_level=1)

    def get_optional(self):
        return self._get_dict(requirement_level=0)

    def __str__(self):
        return json.dumps(self.get_all(), indent=2)


    def update(self, field, value):

        for x in range(3):
            if field in self._info[x]:
                self._info[x][field] = value
                return

        raise RuntimeError("{} is not defined. Please use add for "
                               "new entries".format(field))

def _serialize(value):

    if isinstance(value, Thing):
        return value.get_all()
    elif isinstance(value, (list, tuple)):
        new_value = []
        for x in value:
            new_value.append(_serialize(x))
        return new_value
    else:
        return value

