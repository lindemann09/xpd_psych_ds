import sys
from os import path
import argparse

from . import description, __author__, __version__
from .create import create

def run():
    parser = argparse.ArgumentParser(description=description +
                                        " (v{})".format(__version__),
            epilog="(c) "+__author__)

    if len(sys.argv[1:])==0:
        parser.print_help()
        parser.exit()

    parser.add_argument("DATA",  default=None, nargs='?',
                    help="The path the data folder.")

    parser.add_argument("-f", "--force", dest="force",
                        action="store_true",
                        help="force overriding exsisting target folder",
                        default="")

    parser.add_argument('-d', '--destination', nargs='?', dest="destination",
                        help="Destination folder (default 'xpd_psych_ds')",
                        required=False, default="xpd_psych_ds")

    parser.add_argument('-a', '--add', nargs='+', dest="additional_data",
                        help='Additonal data folder to be added (multiple '
                             'folder are possible)', required=False, default=())

    parser.add_argument('-c', '--creators', nargs='+', dest="creators",
                        help='List of creator names', required=False,
                        default=())

    args = vars(parser.parse_args())

    if args["DATA"] is None:
        print("Use -h for help")
        sys.exit()
    else:
        data_path = path.abspath(args["DATA"])

    if not path.isdir(data_path):
        print("Can't find data folder {0}!".format(args["DATA"]))
        exit()

    create(data_folder=data_path,
           destination_folder=args["destination"],
           creators=args["creators"],
           additional_data_folder=args["additional_data"],
           override_existing_folder=args["force"])

if __name__ == "__main__":
    run()