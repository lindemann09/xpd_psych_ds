## This function has been taking from the Expyriment library (v0.9):
## see http://www.expyriment.org

import codecs as _codecs
import re as _re

def read_datafile(filename, only_header_and_variable_names=False, encoding=None,
                  read_variables=None):
    """Read an Expyriment data file.

    Returns the data, the variable names, the subject info & the comments:

    Parameters
    ----------
    filename : str
        name (fullpath) of the Expyriment data file
    only_header_and_variable_names : bool, optional
        if True the function reads only the header and variable names
        (default=False)
    encoding : str, optional
        the encoding with which the contents of the file will be read
    read_variables : array of str, optional
        array of variable names, read only the specified variables

    Returns
    -------
    data : list of list
        data array
    variables : list of str
        variable names list
    subject_info : dict
        dictionary with subject information (incl. date and between
        subject factors)
    comments : str
        string with remaining comments

    """

    delimiter = ","
    variables = None
    subject_info = {}
    comments = ""
    data = []

    if encoding is None:
        with open(filename, 'r') as fl:
            first_line = fl.readline()
            encoding = _re.findall("coding[:=]\s*([-\w.]+)", first_line)
            if encoding == []:
                second_line = fl.readline()
                encoding = _re.findall("coding[:=]\s*([-\w.]+)",
                                       second_line)
                if encoding == []:
                    encoding = [None]
    else:
        encoding = [encoding]

    read_in_columns = None
    fl = _codecs.open(filename, 'rb', encoding[0], errors='replace')
    for ln in fl:
        # parse infos
        ln = ln.strip()
        if not(ln.startswith("#")):
            if variables is None:
                variables = ln.split(delimiter)
                if only_header_and_variable_names:
                    break
                if read_variables is not None:
                    read_in_columns = [variables.index(x) for x in read_variables]
                    variables = [variables[x] for x in read_in_columns]
            else:
                row =ln.split(delimiter)
                if read_in_columns is not None:
                    row = [row[x] for x in read_in_columns]
                data.append(row)
        else:
            if ln.startswith("#s"):
                ln = ln.replace("#s", "")
                tmp = ln.replace("=", ":")
                tmp = tmp.split(":")
                if len(tmp) == 2:
                    subject_info[tmp[0].strip()] = tmp[1].strip()
                else:
                    subject_info["#s{0}".format(len(subject_info))] = ln.strip()
            elif ln.startswith("#date:"):
                ln = ln.replace("#date:", "")
                subject_info["date"] = ln.strip()
            else:
                comments = comments + "\n" + ln
    fl.close()
    # strip variables
    variables = [x.strip() for x in variables]
    return data, variables, subject_info, comments

