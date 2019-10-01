from sys import version_info
from os import path
from collections import OrderedDict
from copy import copy
import json
import csv

from .read_xpd_data import read_datafile

if version_info.major < 3:
    raise RuntimeError("Psych_ds requires Python 3 or larger.")


class JSONDataDescription():

    def __init__(self, json_filename="data_description.json",
                 subfolder = None,
                 add_optional=True):
        """PsychDS compliant JSON Data Description File"""

        if subfolder is not None:
            self.json_file = path.join(subfolder, json_filename)
        else:
            self.json_file = json_filename

        try:
            with open(self.json_file) as fl:
                self.description = json.load(fl, object_pairs_hook=OrderedDict)
        except:
            self.description = OrderedDict()

        self.add_optional = add_optional
        self.desc_required = JSONDataDescription._specs(
            "description_required.json")
        self.desc_recommended = JSONDataDescription._specs("description_recommended.json")
        self.desc_optional = JSONDataDescription._specs("description_optional.json")
        self.var_required = JSONDataDescription._specs("variable_required.json")
        self.var_recommended = JSONDataDescription._specs("variable_recommended.json")

        self._make_compliant()


    @staticmethod
    def _specs(flname):
        """reading specs from json file"""
        p = path.split(path.realpath(__file__))[0]
        with open(path.join(p, "specs", flname)) as fl:
            return json.load(fl, object_pairs_hook=OrderedDict)


    def __str__(self):
        """"""

        self._make_compliant()
        return json.dumps(self.description, indent=2)


    def save(self):
        """"""

        with open(self.json_file, 'w') as fl:
            fl.write(str(self))

    def _make_compliant(self):
        # ensures xpd_psych_ds comliant json files with all required and optional
        # fields as well as a good ordering

        compliant = copy(self.desc_required)
        compliant.update(self.desc_recommended)
        if self.add_optional:
            compliant.update(self.desc_optional)

        while len(self.description)>0:
            x = self.description.popitem(last=False)
            compliant[x[0]] = x[1]
        self.description = compliant


    @property
    def creators(self):
        return get_dict_list_values(self.description["creator"], "name")

    @creators.setter
    def creators(self, names):
        arr = []
        for n in names:
            arr.append(OrderedDict([("@type", "Person"), ("name", n)]))
        self.description["creator"] = arr

    @property
    def variables_measured(self):
        return get_dict_list_values(self.description["creator"], "name")

    @variables_measured.setter
    def variables_measured(self, variable_names):
        arr = []
        for n in variable_names:
            d = copy(self.var_required)
            d["name"] = n
            d.update(self.var_recommended)
            arr.append(d)
        self.description["variableMeasured"] = arr


#   helper function
def get_dict_list_values(dict_list, key):
    # returns the values of the key in a list of dicts

    try:
        return list(map(lambda x:x[key], dict_list))
    except:
        return []




def estimated_experiment_name(data_files):
    # estimates the experiment from list of data_files
    common_dict = {}
    for x in range(len(data_files)-1):
        for y in range(x+1, len(data_files)):
            c = common_str_origin(data_files[x], data_files[y])
            if len(c)>1:
                if c in common_dict:
                    common_dict[c] += 1
                else:
                    common_dict[c] = 1

    most_common = max(common_dict.values())
    for experiment_name, v in common_dict.items():
        if v == most_common:
            break

    if experiment_name.endswith("_") or experiment_name.endswith(".") or \
        experiment_name.endswith("-") or experiment_name.endswith(" "):
        experiment_name = experiment_name[:-1]

    return experiment_name


def xpd_to_tsv(xpd_flname, tsv_flname):

    data, varnames, subject_info, comments = read_datafile(xpd_flname)
    with open(tsv_flname, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(varnames)
        writer.writerows(data)

    return varnames


# helper function
def common_str_origin(str_a, str_b):

    for c, s in enumerate(zip(str_a, str_b)):
        if s[0]!=s[1]:
            break
    return str_a[:c]

