import sys

from numpy import test
from tests import *
from encoding import *
from file_handler import *

def main():

    args = sys.argv

    if len(args) <= 1:
        print("inssuficient arguments\nuse -h or --help for help")
        return

    if args[1] is None:
        print("error argument is not vaild\nuse -h or --help for help")
        return

    match args[1]:
        case "-c":
            destination = args[3] if len(args) > 3 else "./"
            compress_file(args[2], destination)
            print("Your file has been compressed")

        case "-d":
            destination = args[3] if len(args) > 3 else "./"
            decompress_file(args[2], destination)
            print("Your file has been decompressed")        

        case "-t":

            tests()

        case "-h" | "--help":
            print("Commad template: program [mode] [compression target] [compression destination] \n\n-c      Compress arquive \n-d      Decompress arquive \n-t      Run test ")

        case _ :

            print("Invalid commad, use -h or --help for help")


    return



if __name__ == '__main__':
    main()
