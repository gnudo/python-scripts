import os.path
from shutil import copyfile


class StitchingPreparation(object):
    '''
    crappy/dirty script to ease image volume stitching:
    create a nice folder structure, loop through a given "Folder List";
    extract certain slices and sort them into separate folders
    '''
    
    def __init__(self):
    
        self.BASEDIR = '/home/lovric_g/Desktop/X02DA-Data/matteo_high_resolution/'
        self.folder_list = self.BASEDIR + 'stitching_settings/folder_list.txt'
        self.sliceNr = 501
        
        # these are created during program run
        self.all_samples = []
        self.full_samples = []
    
    def read_textfile(self):
        "reads the texfile and creates full pathnames"
        with open(self.folder_list) as f:
            content = f.readlines()
            self.all_samples = [line.strip()[:-1] for line in content]
        return self.all_samples
    
    def groupSamplesAndInitateFolders(self):
        """
        Groups the samples and creates the folders
        """
        self.full_samples = list(set(self.all_samples))
        
        for item in self.full_samples:
            itemfolder = self.BASEDIR + 'stitching_settings/' + item
            if not os.path.exists(itemfolder):
                os.makedirs(itemfolder)
    
    def extractSlice(self):
        "extracts the slice number for a certain volume"
            
        for item in self.full_samples:
            workingdir = os.path.join(self.BASEDIR, item)
            kk=1
            while True:
                """
                1.) search for all subvolumes
                """
                searching = os.path.isdir(workingdir + str(kk))
                if not searching:
                    break

                recfolder = os.path.join(workingdir + str(kk), 'rec_16bit')

                tif_list = [name for name in os.listdir(recfolder)
                    if name.lower().endswith('.tif') and
                    not name.startswith('.')]
                tif_list.sort()
                tomoslice = os.path.join(recfolder,tif_list[self.sliceNr-1])
                
                """
                2.) Copy to correct location and rename
                """
                destination_dir = os.path.join(self.BASEDIR,'stitching_settings')
                destination_dir = os.path.join(destination_dir,item)
                destination_dir = os.path.join(destination_dir,str(kk).zfill(2)+'.tif')
                print destination_dir
                copyfile(tomoslice, destination_dir)
                kk = kk+1
    
    def run_chain(self):
        self.read_textfile()
        self.groupSamplesAndInitateFolders()
        self.extractSlice()


if __name__ == "__main__":
    
    stitch = StitchingPreparation()    
    stitch.run_chain()
