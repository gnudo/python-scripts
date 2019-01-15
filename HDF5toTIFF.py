import h5py
from PIL import Image
import glob
import os.path
import os
import fileinput
import sys
from shutil import copyfile


def checkpath(filepath):
    filepath = os.path.join(str(filepath), '')
    return os.path.dirname(filepath)


def deleteHDF5file(filepath):
    H5name = os.path.basename(filepath)
    full_h5_path = os.path.join(filepath, H5name + ".h5")
    
    print("...deleting original HDF5 file")
    os.remove(full_h5_path)


def openHDF5andSaveTIF(filepath):
    H5name = os.path.basename(filepath)
    full_h5_path = os.path.join(filepath, H5name + ".h5")
    print(full_h5_path)
    
    h5_open = h5py.File(full_h5_path, 'r')
 
    data = h5_open['exchange/data']
    darks = h5_open['exchange/data_dark']
    flats = h5_open['exchange/data_white']

    path_to_save = os.path.join(filepath, 'tif')
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    else:
        if os.listdir(path_to_save):
            print("...TIF-directory NOT empty...SKIPPING!")
            return
        else:
            print("...TIF-directory empty...proceeding...")
                    
    print(path_to_save)

    print("...writing darks")
    for i in range(len(darks)):
        im = Image.fromarray(darks[i])
        im.save('%s/%s%04d.tif' % (path_to_save, H5name, i + 1))
    
    print("...writing pre-flats")
    for i in range(len(flats)):
        im = Image.fromarray(flats[i])
        im.save('%s/%s%04d.tif' % (path_to_save, H5name, i + len(darks) + 1))

    print("...writing projection images")
    for i in range(len(data)):
        im = Image.fromarray(data[i])
        im.save('%s/%s%04d.tif' % (path_to_save, H5name, i + len(darks) + len(flats) + 1))

    print("...writing post-flats")
    for i in range(len(flats)):
        im = Image.fromarray(flats[i])
        im.save('%s/%s%04d.tif' % (path_to_save, H5name, i + len(darks) + len(data) + len(flats) + 1))


def copyAndAdaptLOG(filepath):
    logfile_name = os.path.basename(filepath)
    full_logfile_path = os.path.join(filepath, logfile_name + ".log")
    new_logfile_path = os.path.join( os.path.join(filepath, 'tif'), logfile_name + ".log" )
    
    print(full_logfile_path)
    print(new_logfile_path)
    
    copyfile(full_logfile_path, new_logfile_path)
    searchExp = "Rotation axis position      : Standard"
    replaceExp = "Rotation axis position      : Right"

    for line in fileinput.input(new_logfile_path, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print(">>>>Error!! Call the script as follows: 'python HDF52TIF.py <FOLDER-where-HDF5-is-located>' ")
        exit(1)
    
    filename = checkpath( sys.argv[1] )
    
    openHDF5andSaveTIF(filename)
    
    copyAndAdaptLOG(filename)
    
    deleteHDF5file(filename)
    