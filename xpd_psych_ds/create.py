import os
from os import path
import shutil
from collections import OrderedDict

from . import lib

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

    DIR_RAW_DATA = path.join(destination_folder, "raw_data")
    DIR_SOURCE_DATA = path.join(DIR_RAW_DATA, "source_data")

    # folder data has to exist
    if not path.isdir(data_folder):
        raise RuntimeError("Can't find an Expyriment data folder {}")

    files = os.listdir(data_folder)
    exp_name = lib.estimated_experiment_name(files)
    print("Experiment: {}".format(exp_name))
    print("Destination folder: {}".format(destination_folder))

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
    for fl in files:
        shutil.copy2(path.join(data_folder, fl),
                     path.join(DIR_SOURCE_DATA, fl),
                     follow_symlinks=True)

        fl_name, suffix = path.splitext(fl)
        if suffix == ".xpd":
            vars = lib.xpd_to_tsv(path.join(data_folder, fl),
                              path.join(DIR_RAW_DATA,
                                        "{}{}".format(fl_name, ".tsv")))
            varnames.extend(vars)

    ## copy further data
    for f_data in additional_data_folder:
        dir_name = path.split(f_data)[1]
        shutil.copytree(f_data, path.join(DIR_SOURCE_DATA, dir_name))

    # PsychDS JSON file
    dd = lib.JSONDataDescription(subfolder=destination_folder, add_optional=True)
    dd.description["name"] = exp_name
    # remove duplicate varnames but remain order and add to json
    dd.variables_measured = list(OrderedDict.fromkeys(varnames))
    if len(creators)>0:
        dd.creators = creators
    dd.save()

