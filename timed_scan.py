import sys
import time
from epics import Motor, PV

if __name__ == "__main__":
   if not len(sys.argv) == 3:
      print(">>>>Error!! Call the script as follows: 'python timed_scan.py <DELAY-BETWEEN-SCANS> <NUMBER-OF-SCANS>")
      exit(1)   

   chFNAME=PV("X02DA-SCAN-CAM1:FILPRE")
   ch_scan_go = PV("X02DA-SCAN-SCN1:GO")
   
   """
   (1) Set varsX
   """
   timing = int( sys.argv[1] )  ## in seconds
   n_scans = int( sys.argv[2] ) ## number 
   filename = chFNAME.get(as_string=True)

   """
   (2) Set name
   """
   for kk in range(1,n_scans+1):
      # PREPARE new name
      filename_new = filename + '_T' + str(kk).zfill(3) + '_'
      print(filename_new)
      
      # SET NEW FILENAME
      chFNAME.put(filename_new, wait=True)

      # LAUNCH NEW SCAN
      ch_scan_go.put(1, wait=True)

      # WAIT
      time.sleep(timing)