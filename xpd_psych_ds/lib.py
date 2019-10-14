from sys import version_info
import os
from os import path
import json
import csv
import shutil
from collections import OrderedDict

from . import psych_ds

from .read_xpd_data import read_datafile

if version_info.major < 3:
    raise RuntimeError("Psych_ds requires Python 3 or larger.")


def create(data_folder,
           additional_data_folder=(),
           destination_folder = "psych_ds",
           creators = (),
           override_existing_folder=False):
    """Create Psych DS compliant data set from Expyriment data

    Parameter
    ---------
    data_folder : str
        path to the folder with Expyriment (.xpd) and other data
    additional_data_folder: str (optional)
        path the additional data that need to be included in the source folder
    destination_folder : str (optional, default='psych_ds')
        path to the target folder, resulting psych_ds folder
    creators : list of str (optional)
        list of the names of the creators of the data
    override_existing_folder : bool (optional, default=False)
        set True is existing xpd_psych_ds should be delete

    """

    data_folder = path.abspath(data_folder)
    destination_folder = path.abspath(destination_folder)
    DIR_RAW_DATA = path.join(destination_folder, "raw_data")
    DIR_SOURCE_DATA = path.join(DIR_RAW_DATA, "source_data")

    print("XPD-Psych-DS")
    print(" Data: {}".format(data_folder))
    print(" Destination: {}".format(destination_folder))

    # folder data has to exist
    if not path.isdir(data_folder):
        raise RuntimeError("Can't find an Expyriment data folder {}".format(data_folder))

    files = os.listdir(data_folder)
    exp_name = estimated_experiment_name(files)
    print(" Experiment: {}".format(exp_name))

    if override_existing_folder:
        try:
            shutil.rmtree(destination_folder)
        except:
            pass

    # make folder
    try:
        os.mkdir(destination_folder)
    except:
        raise RuntimeError("Can't create target folder {}. ".format(
            destination_folder) +
                           "It probably exists already or set " 
                           "`override_existing_folder=True' ")

    os.makedirs(DIR_SOURCE_DATA)

    # copy data and converting data to tsv
    varnames = []
    cnt = 0
    for fl in files:
        shutil.copy2(path.join(data_folder, fl),
                     path.join(DIR_SOURCE_DATA, fl),
                     follow_symlinks=True)

        fl_name, suffix = path.splitext(fl)
        if suffix == ".xpd":
            vars = xpd_to_tsv(path.join(data_folder, fl),
                              path.join(DIR_RAW_DATA,
                                        "{}{}".format(fl_name, ".tsv")))
            varnames.extend(vars)
        cnt += 1
    print(" Files convered: {}".format(cnt))

    ## copy further data
    for f_data in additional_data_folder:
        f_data = path.abspath(f_data)
        print(" Add. data copied: {}".format(f_data))
        dir_name = path.split(f_data)[1]
        shutil.copytree(f_data, path.join(DIR_SOURCE_DATA, dir_name))

    # PsychDS JSON file
    ds = psych_ds.DataSet(name = exp_name)

    # remove duplicate varnames but remain order and make psych_ds objects
    varnames = list(OrderedDict.fromkeys(varnames))
    varnames = list(map(lambda x:psych_ds.Variable(name=x), varnames))
    ds.update('variableMeasured', varnames)

    creators = list(map(lambda x:psych_ds.Person(name=x), creators))
    ds.add("creator", creators)
    save_dataset_description(ds, subfolder=destination_folder)

    print("\nPlease do not forget to edit the `dataset_descrption.json` "
          "file.")


## helper


def save_dataset_description(data_set, json_filename="dataset_description.json",
                 subfolder = None):
    """ TODO """

    if subfolder is not None:
        json_file = path.join(subfolder, json_filename)
    else:
        json_file = json_filename

    with open(json_file, 'w') as fl:
        fl.write(str(data_set))


def load_dataset_description(json_filename="dataset_description.json",
                 subfolder = None):
    """ TODO """

    if subfolder is not None:
        json_file = path.join(subfolder, json_filename)
    else:
        json_file = json_filename

    try:
        with open(json_file) as fl:
            return json.load(fl, object_pairs_hook=OrderedDict)
    except:
        return None

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
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(varnames)
        writer.writerows(data)

    return varnames

def common_str_origin(str_a, str_b):

    for c, s in enumerate(zip(str_a, str_b)):
        if s[0]!=s[1]:
            break
    return str_a[:c]

