from PyQt5 import QtGui, QtCore, QtWidgets  # Import the PyQt5 modules we'll need
from PyQt5.QtGui import QFont
import sys  # We need sys so that we can pass argv to QApplication

##import table  # This file holds our MainWindow and all table related things
import v1      ## table display routine file
import csv
from pathlib import Path
import winsound
import re
import json
from operator import rshift
from collections import deque   ## pronounced deck
global DEBUG

DEBUG = 0
fntBold = QFont()
fntNorm = QFont()
fntBold.setBold(True)
fntField = QFont()
fntField.setPointSize(40)
fntField.setBold(True)

# it also keeps events etc that we defined in Qt Designer
import os  # For listing directory methods
import time
import io
import glob
import traceback
import threading
from datetime import date, datetime
from random import *
from operator import itemgetter

sys.tracebacklimit = 1000

### interval timing function In a separate thread
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator
     
### handler for intercepting exceptions
def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 8
    logFile = "simple.log"
    notice = "\n"
    breakz = "\n"
    versionInfo="    0.0.1\n"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: %s' % (str(excType), str(excValue))
    sections = [separator, timeString, breakz, separator, errmsg, breakz, separator, tbinfo]
    msg = ''.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    print("\nMessage: %s" % str(notice)+str(msg)+str(versionInfo))

### replacement of system exception handler
sys.excepthook = excepthook   
           

class TableApp(QtWidgets.QMainWindow, QtWidgets.QTableWidget, v1.Ui_MainWindow, v1.tabinfo):  #####
    def __init__(self):
        # super is used here in that it allows us to
        # access variables, methods etc in the v1.py file
        super(self.__class__, self).__init__()
        xx=v1.Ui_MainWindow()  ## also see yy below
                                    ## works here because Hmain and Wmain are class variables?
        self.setupUi(self)          # This is defined in v1.py file automatically
        if (DEBUG == 1): print("main self: %s" % self)
        self.mm = self
        self.xx2 = xx           ## appears xx is only used here
        self.xx2.READIN = 0     ## set to determine if we have read MEMBERS yet
        # It sets up layout and widgets that are defined

        self.pushButton.clicked.connect(self._addSrchr)  # When the ADD button is pressed
        self.pushButton_2.clicked.connect(self._rmSrchr)  # When the REMOVE button is pressed
        self.pushButton_undo.clicked.connect(self._undo)  # When the UNDO button is pressed
        self.pushButton_readMem.clicked.connect(self._readMemb)  # When the READ button is pressed
        self.pushButton_teams.clicked.connect(self.listTeams) # When list teams pushed
        self.num9.clicked.connect(lambda: self.numbers(9)) # put numbers in SAR ID field
        self.num8.clicked.connect(lambda: self.numbers(8)) # put numbers in SAR ID field
        self.num7.clicked.connect(lambda: self.numbers(7)) # put numbers in SAR ID field
        self.num6.clicked.connect(lambda: self.numbers(6)) # put numbers in SAR ID field
        self.num5.clicked.connect(lambda: self.numbers(5)) # put numbers in SAR ID field
        self.num4.clicked.connect(lambda: self.numbers(4)) # put numbers in SAR ID field
        self.num3.clicked.connect(lambda: self.numbers(3)) # put numbers in SAR ID field
        self.num2.clicked.connect(lambda: self.numbers(2)) # put numbers in SAR ID field
        self.num1.clicked.connect(lambda: self.numbers(1)) # put numbers in SAR ID field
        self.num0.clicked.connect(lambda: self.numbers(0)) # put numbers in SAR ID field
        self.numB.clicked.connect(lambda: self.numbers(10)) # put numbers in SAR ID field
        self.numD.clicked.connect(lambda: self.numbers(11)) # put numbers in SAR ID field
        self.numE.clicked.connect(lambda: self.numbers(12)) # put numbers in SAR ID field
        self.numN.clicked.connect(lambda: self.numbers(13)) # put numbers in SAR ID field
        self.numR.clicked.connect(lambda: self.numbers(14)) # put numbers in SAR ID field
        self.numS.clicked.connect(lambda: self.numbers(15)) # put numbers in SAR ID field
        self.numT.clicked.connect(lambda: self.numbers(16)) # put numbers in SAR ID field
        self.numALP.clicked.connect(lambda: self.numbers(17)) # put numbers in SAR ID field       
        self.modex = 0  ## set for select cell  if = 1, then drag and drop
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.tableWidget.cellDoubleClicked.connect(self.cell_was_Dclicked)
        self.tableWidget2.cellClicked.connect(self.dialog_was_clicked)
        self.tableWidget5.cellClicked.connect(self.dialog_was_clicked4)
        self.tableWidget3.cellClicked.connect(self.dialog_was_clicked2)
        self.tableWidget4.cellClicked.connect(self.dialog_was_clicked3)        
        self.selected = 0  ## preset to nothing selected   NOT USED?
        self.setAcceptDrops(True)               ## do not pickup drag/drop if assoc with tableWidget
        self.tableWidget.setDragEnabled(True)   ## needs to refer to tablewWidget

        zz = v1.tabinfo()

### call to timing function
        @setInterval(20)  ## decorator to call timing thread (seconds)
        def datetime_update(xxx):
          today = date.today()
          tod = today.strftime('%b %d, %Y')
          time  = datetime.now().time()
          xxx.dateTime.setText(str(tod)+" @ "+str(time)[0:5])  ## updates the date/time stamp on mainWindow
          ##print("Call to func")
        ##self.num = 1
        self.stop = datetime_update(self)  ## start timer
        ###self.num = 0
        #####self.stop.set()        ## will stop timer
        ###
        ###@setInterval(30)         ## 30 seconds to recheck members file update  CHECK??
        ###def chk_new_srchr(xxx):  ## checks for update of searchers new/remove
        ###    self.num = self.num+1
        ###    self.mm.infox.setText("30 sec timer count: "+str(self.num))
        ####
        #####self.stop2 = setInterval(chk_new_srchr(self))   # start timer2
        #

        ###  The following does not appear to have an affect
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.tableWidget.setSizePolicy( sizePolicy )


#
#  list TEAMS : [Name, xloc, yloc, #srchrs, type, location, timeout]
#
#  list SRCHR : [Name, agency, idnumb, xloc, yloc, xteam, yteam, leader (bit), medical (bit), Blink, Cell#, Resources]
#
#  list MEMBERS:[Name, IDval, Agncy, leader, medical, TimeIN, TimeOUT, Cell#, Resources, CumTime]  (use TimeIn != "-1" ? as checked-in)
#                                         Want to add total time field for multiple time segments
#
# preset values  for each type
#       TEAMS : sheriff -> [Sheriff Coord, 0,0,0,IC,IC,0.0]
#               ops     -> [OPS, 0,8,0,IC, IC, 0.0]
#               unas    -> [UnAssigned, Nunas_col,0,UNAS, IC, 0,0]
#     SEARCHERS: SRCHR  -> [Namex1, NC, #1, 6, 1, ->UNAS(x,y) (team), 0, 0]
#                          [Namexz, NC, #2, 6, z, ->UNAS(x,y) (team), 0, 0]

######
     
## the following is writing to tabinfo.info
        i=0   ## entry #
        j=0    ## cnt of members
        m = 0  ## ID's
        savei = 0
        savej = 0
        clr_order = "RGBYMC "  ## team #
        self.zz2 = zz
        ##print("TOP: %s:%s"%(zz,self.zz2))
        zz.TEAM_NUM = 0
        ## place headers for Search MGMT in column 0

        ##  Name, xloc, yloc, #srchrs, Type, Location, Time Deployed
        zz.TEAMS.append(["Sheriff Coord", 0, 1, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Search Mngr", 0, 5, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Operations", 0, 10, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Planning", 0, 15, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Logistics", 0, 20, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Comms", 0, 25, 0, "IC", "IC", 0.0])
        xunas = 6 ## location of Unassigned header
        yunas = 1
        team_unas = 6   ## after the are defined
        zz.TEAMS.append(["UnAssigned", xunas, yunas, 0, "UNAS", "IC", 0.0])
        zz.TEAMS.append(["END"])
        if (DEBUG == 1): print(zz.TEAMS[team_unas])

        iw = 0     ## initialization
        zz.TEAMS[team_unas][3] = iw  ## set number of searchers in unassigned    
        zz.SRCHR.append(["END"])   
        zz.tabload(self,0)         ## load display table
        if (DEBUG == 1): print("At init\n")
        ####  end of __init__


    def _addSrchr(self): ## Button ADD SEARCHER
        ##zz = v1.tabinfo()
        team_unas = 6                    ####   This is the number of the entry for the Unassigned Team
                                         ##         This may change as default or over time
        yy = self.mm  ##v1.Ui_MainWindow()  
        zz = self.zz2
        yy.saveLastIDentry = ""        
        ##print("TOP: %s"%zz.SRCHR)
        if (DEBUG == 1): print("At mode %i\n" % self.modex)
        self.modex = 1 - self.modex    ## change state
        xmodel(self.modex)   # call routine outside of class
        ## read the sarID field
        sarINFOval = yy.sarID.text()
        if (len(sarINFOval) == 0): return
        sarINFOsplit = sarINFOval.split()   ## SAR ID field can be "ID" or "ID AGENCY"
        sarIDval = sarINFOsplit[0].upper()
        sarAGENCY = "NC"                      ## default AGENCY
        if (len(sarINFOsplit) > 1):         ## then agency arg was entered
            sarAGENCY = sarINFOsplit[1].upper()
        if (DEBUG == 1): print("ADD: %s"% zz)
        memPtr = -1
        for xx in range(0,len(zz.MEMBERS)):
          if (zz.MEMBERS[xx][1] == sarIDval and zz.MEMBERS[xx][2] == sarAGENCY):
            memPtr = xx
            break
        if (memPtr == -1):                  ## ID not found
            winsound.Beep(2500, 1200)       ## BEEP, 2500Hz for 1 second, needs to be empty
            return
        elif (zz.MEMBERS[memPtr][5] != -1):    ## member already checked-in, ignore
            winsound.Beep(2500, 300)           ## BEEP, short 2500Hz, needs to be empty
            winsound.Beep(2500, 300)           ## double
            yy.sarID.setText("")
            return
        if (DEBUG == 1): print("PTR  %s"%memPtr)
        ## find vacancy in UNAS_USED
        ##  MEMBERS csv file: name, id, agency, leader, medical (add local fields: checked-in flag and ptr-to-srchr)
        ##print("UNAS list %s"%zz.UNAS_USED)
        for ixx in range(2,len(zz.UNAS_USED)):
            if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
            if (zz.UNAS_USED[ixx] == 0):           ## found available location
                zz.UNAS_USED[ixx] = 1
                ##print("ENTRY %i"%ixx)
                break
        if (DEBUG == 1): print("ptr %i"% ixx)
        colu = int(ixx/yy.Nrows)
        rowu = ixx - colu * yy.Nrows
        colu = colu + yy.Nunas_col
        TimeIN = time.time()    ## time since epoch
        tx = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("%f:%s"%(TimeIN,tx))
        if (DEBUG == 1): print("TimeIN %i"% TimeIN)  ## If the srchr comes back how to accum time? In members
        zz.SRCHR.insert(-1,[zz.MEMBERS[memPtr][0],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][1],  \
                        colu, rowu, yy.Nunas_col, 1, zz.MEMBERS[memPtr][3], zz.MEMBERS[memPtr][4], 5, \
                        zz.MEMBERS[memPtr][7], zz.MEMBERS[memPtr][8]]) # set blink to 5 sec
                                    ## Team is Unas at (Nunas_col,1) place before "END"
        zz.MEMBERS[memPtr][6] = -1                      ## time-out initialize to -1
        zz.MEMBERS[memPtr][5] = TimeIN                  ##  set as time-in
###
###  Need to construct correct entry
###       ALSO, check that SAR has not already been loaded
###             AND, when removing check that it was there        
###
##   SRCHR :        Name, agency, IdNumb, xloc, yloc, TeamX, TeamY, Leader(bit), Med(bit), Blink vs TimeIN, TimeOUT    ???
## put these \/ in some initialization place
##   incase searchers are added after movement has occurred, need to skip locations already used        

        zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
        yy.saveLastIDentry = yy.sarID.text()
        yy.sarID.setText("")  ## clear sarID field
        if (DEBUG == 1): print("PTR2 %s"%yy)
        zz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec
        zz.time_chk()            ## start blinker clock
        ##print("SRCHR chk2: %s"%zz.SRCHR)  
        zz.tabload(yy,0)         ## load display table


    def _rmSrchr(self): ## button REMOVE SEARCHER
        zz = self.zz2
        yy = self.mm
        #
        ## Can send a bit back to sign-in that the member is associated with a Team (vs Unassigned)
        ##   to indicate that the member cannot be removed.  To create this bit check the SRCHR
        ##   team location [5] and [6] to see if = Nunas_col, 1 (Unassigned)
        #

        memPtr = -1
        sarIDval = yy.sarID.text()
        if (sarIDval == ""):   ## blank entry means to remove previous ADD searcher (probably incorrect member chosen)
          sarIDval = yy.saveLastIDentry       ####  NEED to get agency, too  PARSE ID and agency from entry

        sarINFOsplit = sarIDval.split()       ## SAR ID field can be "ID" or "ID AGENCY"
        sarIDval = sarINFOsplit[0].upper()
        sarAGENCY = "NC"                      ## default AGENCY
        if (len(sarINFOsplit) > 1):           ## then agency arg was entered
          sarAGENCY = sarINFOsplit[1].upper()
          
        for xx in range(0,len(zz.MEMBERS)):
          if (zz.MEMBERS[xx][1] == sarIDval and zz.MEMBERS[xx][2] == sarAGENCY):
            memPtr = xx
            break
        if (memPtr == -1):
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, member not found
            return
        if (DEBUG == 1): print("PTR  %s"%memPtr)        
        fnd = -1
        for ptr in range(0, len(zz.SRCHR)-1):  ## do not test the lst element (END)
          ## match ID and agency  
          if (zz.SRCHR[ptr][2] == sarIDval and zz.SRCHR[ptr][1] == sarAGENCY):
            fnd = 1
            if (DEBUG == 1): print("ID, Cnty %s %s"%(zz.SRCHR[ptr][2],zz.SRCHR[ptr][1]))
            break
        if (fnd == -1 or (zz.SRCHR[ptr][5] != yy.Nunas_col and zz.SRCHR[ptr][6] != 1 )): ## TEAM of SRCHR must be UNASSIGNED
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, searcher not found
            return          
        TimeOUT = time.time()                         ## add to MEMBERS record
        zz.MEMBERS[memPtr][6] = TimeOUT               ##  set as checked-out
        zz.MEMBERS[memPtr][9] = zz.MEMBERS[memPtr][9] + zz.MEMBERS[memPtr][6] - zz.MEMBERS[memPtr][5]  ## cum time
        zz.MEMBERS[memPtr][5] = -1                    ## reset for next checkin
        rowy = zz.SRCHR[ptr][4]
        colx = zz.SRCHR[ptr][3]
        npt = rowy + (colx - yy.Nunas_col)*yy.Nrows
        zz.UNAS_USED[npt] = 0
        del zz.SRCHR[ptr]                     ## we are deleting the record and marking MEMBERS entry with TimeOUT
### Will only remove if in Unassigned.  THEN, also put the space as available again  
        yy.sarID.setText("")
        zz.tabload(yy,0)                      ## update table


    def _undo(self): ## Button UNDO - put status/display back one change, saving MEMBERS, too
        zz = self.zz2
        yy = self.mm
        if (DEBUG == 1): print("At undo %i \n" % self.modex)
        ## call undo_table (single deep)

        #print("POP1: %s"%zz.saveTeam)
        zz.saveTeam.pop()
        try:
          zz.TEAMS = zz.saveTeam.pop()      
        except:
          print("End of queue")
          winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty          
          return
        zz.saveSrchr.pop()
        zz.SRCHR = zz.saveSrchr.pop()
        zz.saveUnUsed.pop()
        zz.UNAS_USED = zz.saveUnUsed.pop()
        zz.saveMembers.pop()                ## these are double pop's because of intervening append
        zz.MEMBERS = zz.saveMembers.pop()
        zz.tabload(yy,0)
        

        
    def _readMemb(self): ## Button READ MEMBERS from CVS files
        ###  nominally the ncssar members.csv and OTHERS.csv files are read to get member info.
        ####### FOR the case when the INFOX box starts with JSON, instead this is a recovery and
        #######   the latest JSON files are read and populate TEAMS, SRCHR, UNAS_USED and MEMBERS
        
        caps = ["EMT", "PA"]  ##  capabilities for Medical type - probably temporary?
        yy = self.mm
        zz = self.zz2
        if (DEBUG == 1): print("At readmemb %i\n" % self.modex)
        self.modex = 1 - self.modex    ## change state  test
        xmodel(self.modex)             # call routine outside of class test
        test_info = yy.infox.text()
        if (test_info[0:4].upper() != "JSON" and test_info[0:4].upper() != "REMO" ):
            ## if INFOX has "JSON" means recovery; if REMOTE means get info from sign-in program output
          if (zz.READIN == 0):  ## otherwise skip MEMBERS read-in, but do OTHERS read-in
             zz.MEMBERS = []          ## reset list
             zz.READIN = 1      ## set as having been read
                   
             my_file = Path("MEMBERS2.csv")       #############  NCSSAR member database
             if my_file.is_file():
               with open(my_file,'rt') as csvIN:
                 csvPtr = csv.reader(csvIN, dialect='excel')
                 regShrf = r"[0-9][A-Z].*"        ## reg ex to find sheriff IDs
                 for row in csvPtr:
                   make = ["0", "0", "NC", "0", "0", -1, -1, " ", " ", 0]  ## MEMBERS: need to re-initalize make here for some reason
                   if (row[0].isdigit()):        ## has to be all digits (searcher)
                     make[1] = row[0]   # SAR ID
                     make[0] = row[1]   # name
                     make[7] = row[3]   # cell number
                     make[8] = row[5]   # resources
                     for cx in caps:
                       regcap = r"[ ,]" + cx + r"[ ,]"
                       fnd = re.search(regcap, row[5])
                       if (fnd != None):     ## found a match
                         make[4] = "1"   
                     if (row[6] == "1"):       ## type 1 searcher; used for now to choose LEADER (temporary)
                       make[3] = "1"        
                   elif (re.search(regShrf, row[0]) != None):    ## numb/letter... found sheriff coord
                     make[1] = row[0]
                     make[0] = row[1]
                     make[7] = row[3]   # cell number
                     make[8] = row[5]   # resources
                   else:
                     continue                   ## valid entry not located - go to next line
      #
      ## For remote sign-in do we want to check if member has already been loaded?
      ## For pickup from sign-in do we want to assign time-in and then time-out to MEMBERS db?
      ##     Or when using sign-in program, we do not use MEMBERS db??
      ## From sign-in need: Name, ID#, Agency, leader, medical, time-in, time-out, capabilities? (Carda, OHV, Nordic...)
      ##      if done, any need for Members db? could save info for searcher, while eliminating from SRCHR db when they leave
      #              
                   zz.MEMBERS.append(make)        ## load MEMBERS if valid entry
               if (DEBUG == 1): print("\n\n")
               if (DEBUG == 1): print("READ: %s:%s"%(zz,self.zz2))
             else:
               winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty
               return
                 
             zz.SRCHR.clear()             ##  reset for now only first time thru
             zz.SRCHR.append(["END"])     ## preset the first time thru
            
          my_file = Path("OTHERS.csv")

##### Could check for existing ID and agency and replace upon readin

          ###  format of others is "Member,ID,agency,Leader,Medical,(add CheckedIn)(maybe add time-out?)" 
          if my_file.is_file():
            if (DEBUG == 1): print("In other")  
            with open('OTHERS.csv','rt') as csvIN2:
              csvPtr = csv.reader(csvIN2, dialect='excel')
              for row in csvPtr:
                ## name, ID, Agency
                row = [row[0],row[1],row[2],row[3],row[4],-1, -1, " ", " ", 0]      ## will map to srchr
                ifnd = 0  
                for ix in range(len(zz.MEMBERS)):          
                  if (row[1] == zz.MEMBERS[ix][1] and row[2] == zz.MEMBERS[ix][2]): ## match: ID,agency
                    del zz.MEMBERS[ix]         ##    update entry
                    zz.MEMBERS.insert(ix,row)
                    ifnd = 1                   ## mark event
                    break                      ## done, so skip the rest
                if (ifnd == 0):                ##    add
                  zz.MEMBERS.append(row)       ## possibly change # and order of cells
                  if (DEBUG == 1): print("new row: %s" % row)  
          ### ignore otherwise
          if (DEBUG == 1): print("READ: %s"%zz.SRCHR)
          
        elif (test_info[0:4].upper() == "JSON"): ## read json files to load MEMBERS, TEAMS, SRCHR, UNAS_USED for recovery
            if (DEBUG == 1): print("JSON found")
            mt1 = 0
            for m in range(0,5):    # find most recent saved state file
              mtime = os.path.getmtime("DATA\saveAll"+zz.saveNames[m]+".json")  ## file modified time
              if (mtime > mt1):
                  mt1 = mtime
                  mpnt = m
            setName = zz.saveNames[mpnt]
               ##   Newest save time.  If corrupted, then delete
               ##   the set and use the other one
            print("Set: %s"%setName)
            zz.READIN = 1   ## set as having read members in
            try:
              with open("DATA\saveAll" + setName + ".json", 'r') as infile:  ## opens, reads, closes
                [zz.TEAMS, zz.SRCHR, zz.MEMBERS, zz.UNAS_USED, zz.TEAM_NUM, \
                    zz.RemoteSignInMode] = json.load(infile)   
              print("Doing recovery reload...")    
              zz.tabload(yy,0)
            except:
              print("Bad JSON save file, try other version")
              winsound.Beep(2500, 1200)       ## BEEP, 2500Hz for 1 second, needs to be empty
        else:   # MUST be REMOTE  will check every so many seconds and see if file time-modified is updated
                #  So need timer to call routine to check if interface file modify time has changed.
            pass
            zz.RemoteSignInMode = 1
            self.priorRead = []
            print("AT remote: %s %s %s"%(self,yy,zz))
            zz.srchr_chk(yy)           ## start checking for remote entry updates

            
    def rmtInProcess(self):    
            ########### PUT the following in a routine called by timer
            ###   Start timer above
            ##  Enable check remote sign-in timer above; In timer routine check time modified and if so, do...
 
        ##*SARID, "NAME(LAST,FIRST)", AGENCY, RESOURCES, TIME-IN(HUMAN), TIME-OUT, TIME-DELTA, TIME-IN(EPOCH FLOAT),
        ##         TIME-OUT, TIME-DELTA, CELL#, "STATUS(SignIn, SignOut, OnTcard, RmTcard)"
        
        ##     Status exchange: SignIn from Sign-in program, acknowledge by OnTcard from Tcard
        ##                      then, RmTcard from Tcard enabling SignOut at Sign-Out
        ##     When Tcard sees Sign-In checks for a MEMBERS entry from a previous participation, if found update
        ##          sign-in and sign-out times. Delta will accumulate. Also, create a SRCHR entry
        ##          Then update the remote file status to OnTcard and write file.  Also change priorRead db status, too     
        ##     When a member tells Tcard they are leaving, Tcard removes the SRCHR entry, updates the MEMBERS entry to
        ##          set the time-out and delta times.  Then the status is changed to RmTcard in the current and priorRead
        ##          db's and the remote file is written.
            yy = self.mm
            zz = self.zz2
            team_unas = 6                    ####   This is the number of the entry for the Unassigned Team
                                             ##         This may change as default or over time

            print("At Remote sign-in")
            server = "c:\\signin_files\\"
            lenPrior = len(self.priorRead)
            rows = []
            update = 0     # only reading remote file
            deltaTime = 10 # number of seconds old is time stamp - must be rogue
            
## first scan members for searchers removed from Tcards
      ## add code to check MEMBERS db for new Time-out (previous T/O # are negative)
      ## If any found, change record status to RmTcard for each
      ##  negate Time-out value in MEMBERS db
            print('b4 look for rm members')
            ifnd = 0         # indicates found at least one sign-out
            rem = []
            for ix in range(len(zz.MEMBERS)):
                if (float(zz.MEMBERS[ix][6]) > 0):      # timeout set, so removed from Tcard
                    rem.append(ix)               # create list of members to remove
                    ifnd = ifnd + 1
                    print("RM %i"%ix)
            
            print('b4 lock')
    ### create file LOCK
            while (1):                    
                    curT = time.time()               # current time
                    while (1):
                        files = glob.glob(server + 'rmt_lock_*')
                        if (len(files) == 0): break  # no lock files found
                        for fi in files:
                            strt = fi.find('#')+1
                            fi_time = int(float(fi[strt:len(fi)]))
                            if ((curT - fi_time) > deltaTime):         ## lock around too long
                                #print("remove %f"%deltaTime)
                                os.remove(fi)
                    strCurT = str(curT)
                    rand = int(strCurT[-1])          # use to get different delays
                    time.sleep(rshift(rand,7))       # delay by rand/128 
                    cname = os.environ['COMPUTERNAME']
                    fx = open(server + 'rmt_lock_' + cname + '#' + strCurT, 'w+')  ## create lock
                    fx.close()
                    files = glob.glob(server + 'rmt_lock_*')   # find all lock files
                    if (len(files) > 1):             # something else created a lock too
                        os.remove(server + 'rmt_lock_' + cname + '#' + strCurT)  # back off
                    else: break                      # only our lock; continue on    
                 #  loop back
   ###  end file lock
            print('aftr lock')
            print('List of removes %s'%rem)
            irow = 0            
            with open(server + 'REMOTE_SIGN_IN.csv','rt') as csvIN2:
              csvPtr = csv.reader(csvIN2, dialect='excel', skipinitialspace=True)
              print('open remote signin file')
              for row in csvPtr:
                  rows.append(row)   ## create rows list by combining each row
                  irow = irow + 1    ### always read entire file comparing lines
                  ##print('rowlong %s'%row)
                  print("RMT row%i: %s, %s: lenP %i"% (irow,row[0],row[1],lenPrior))
                  if (row[0][0] == "*"):
                      continue             ## skip comment lines
                  if (irow <= lenPrior):   # for existing lines, first compare to prior
                      print("At compare")
                      if (self.priorRead[irow-1] != row):
                          print("Difference\n   %s\n   %s"%(self.priorRead[irow-1],row))    ## check for differences if name, sarid -> give error
                          if (row[0] != self.priorRead[0] or row[2] != self.priorRead[2]):
                              print("Error in remote file at %s"% row)
                              winsound.Beep(2500, 300)           ## BEEP, short 2500Hz
                              winsound.Beep(1000, 1200)          ## double
                              winsound.Beep(2500, 300)
                              break


######check what should be the preset value for timeIn and Out a 0 or -1 from SignIn program ??
                            
                          ## check for change: timeout times, delta time and status s/b SignOut
                          ##   if other changes issue warning
                          # find MEMBERS entry
                      else:  # indent fixer    
                          memPtr = -1
                          for ix in range(0,len(zz.MEMBERS)):
                              print('ix=%i'%ix)
                              if (row[0] == zz.MEMBERS[ix][1] and row[2] == zz.MEMBERS[ix][2]): ## match: ID, agency
                                  memPtr = ix
                                  print('MeM ptr %i'%memPtr)
                                  break
                          if (memPtr == -1):
                              print("Record not found in MEMBERS: %s"% row)
                              winsound.Beep(2500, 300)
                              return                      ## record not found
                          elif (memPtr in rem):           # did we find a member to be removed?
                              rows[irow-1][11] = "RmTcard"
                              zz.MEMBERS[memPtr][6] = -zz.MEMBERS[memPtr][6]     # negate as flag that sign-out has processed
                              print("Update MEM for RM %i, irow %i"%(memPtr, irow))
                          if (row[11] == "SignOut"):      ## completed signOut
                              pass                        # should already have updated the following:
                              #zz.MEMBERS[memPtr][6] = row[8]                           # timeout
                              #zz.MEMBERS[memPtr][9] = zz.MEMBERS[memPtr][9] + row[9]   # delta time cum
                          elif (row[11] == "SignIn"):     ## re-signIn    
                              zz.MEMBERS[memPtr][5] = row[7]                           # timein
                              zz.MEMBERS[memPtr][6] = -1                               # timeout
                              #### create SRCHR entry
                              ## find vacancy in UNAS_USED
                              for ixx in range(2,len(zz.UNAS_USED)):
                                  if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
                                  if (zz.UNAS_USED[ixx] == 0):           ## found available location
                                      zz.UNAS_USED[ixx] = 1
                                      break
                              colu = int(ixx/yy.Nrows)
                              rowu = ixx - colu * yy.Nrows
                              colu = colu + yy.Nunas_col
                              zz.SRCHR.insert(-1,[zz.MEMBERS[memPtr][0],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][1],  \
                                 colu, rowu, yy.Nunas_col, 1, zz.MEMBERS[memPtr][3], zz.MEMBERS[memPtr][4], 5, \
                                 zz.MEMBERS[memPtr][7], zz.MEMBERS[memPtr][8]]) # set blink to 5 sec
                              zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
                              rows[irow-1][11] = "OnTcard"
                          elif (row[11] == "OnTcard" or row[11] == "RmTcard"):  ## Already Signed-In and on Tcard
                              pass    # just continue on
                          else:
                              print("Unexpected changes in record: %s"% row)
                              winsound.Beep(2500, 300)
                  else:
                      print("New entry")
                      ## should be for new sign_in only, so only time-in set and status s/b set as SignIn
                      print('stat :%s:'%row[11])
                      if (row[11][0:6] == "SignIn"):
                          ## check resources row[3] for LD and MED and set logic 0 or 1
                          lead = row[3].find("LD") > 0
                          med = row[3].find("MED") > 0
                          rownu = [row[1], row[0], row[2], lead, med, row[7], row[8], row[10],row[3], row[9]] # watch for numeric vs string
                          zz.MEMBERS.append(rownu)
                          #### create SRCHR entry
                          ## find vacancy in UNAS_USED
                          for ixx in range(2,len(zz.UNAS_USED)):
                              if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
                              if (zz.UNAS_USED[ixx] == 0):           ## found available location
                                  zz.UNAS_USED[ixx] = 1
                                  break         
                          colu = int(ixx/yy.Nrows)
                          rowu = ixx - colu * yy.Nrows
                          colu = colu + yy.Nunas_col
                          zz.SRCHR.insert(-1,[row[1], row[2], row[0], colu, rowu, yy.Nunas_col, 1, str(lead), \
                                          str(med), 5, row[10], row[3]]) # set blink to 5 sec
                          zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
                          rows[irow-1][11] = "OnTcard"
                      else:
                          print("Unexpected Status: %s"%row)
                          winsound.Beep(2500, 300)
                          
            print('prior to tmp open')
            with open(server + 'remote_tmp.csv', 'w+', newline='') as csvOUT:      ##  create a tmp updated interface file
                csvPtr = csv.writer(csvOUT, dialect='excel', skipinitialspace=True)            
                csvPtr.writerows(rows)
                
            print('opened and wrote tmp file')
            os.remove(server + 'REMOTE_SIGN_IN.csv')     ## remove pre-existing file
            os.rename(server + 'remote_tmp.csv', server + 'REMOTE_SIGN_IN.csv')  ## put tmp file into normal file
            os.remove(server + 'rmt_lock_' + cname + '#' + strCurT)    ## remove lock file
            print('changed files')
            yy.saveLastIDentry = yy.sarID.text()
            yy.sarID.setText("")  ## clear sarID field
            if (DEBUG == 1): print("PTR2 %s"%yy)
            zz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec
            zz.time_chk()            ## start blinker clock
            ##print("SRCHR chk: %s"%zz.SRCHR)
            zz.tabload(yy,0)
            
            ## At end save current input to priorRead
            ## print("Rows: %s"% rows)
            self.priorRead = rows
            ##print("PriorRead: %s"% self.priorRead)


    def numbers(self,n):  ## take the number buttons and fill SAR ID field
        strg1 = ["D", "E", "N", "P", "S", "T"]
        strg2 = [["H", " ", "R", "G", "M", "A", "U", "Y", "B", "L"], \
                 ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]
        yy = self.mm
        if (DEBUG == 1): print("Button %i : %i\n"%(n, yy.keyBrd))
        ## if "B" num=10 delete a character
        if (n == 17):
          yy.keyBrd = 1 - yy.keyBrd   ## toggle
          yy.setKeys(yy.keyBrd)
          return
        strg = yy.sarID.text()
        if (n == 10):  ## backspace
          yy.sarID.setText(strg[0:-1])
        elif (n > 10):  
          yy.sarID.setText(strg+strg1[n-11])
        else:  # n < 10
          yy.sarID.setText(strg+strg2[yy.keyBrd][n]) 
        

    def listTeams(self):
        if (DEBUG == 1): print("In List Teams")
        fts = open("teams.txt","wt+")  ## possibly delete file first (above)
        yy = self.mm
        zz = self.zz2

        Tsort = sorted(zz.TEAMS[0:-1],key=itemgetter(0))  ## ignore "end"        
        Ssort = sorted(zz.SRCHR[0:-1],key=itemgetter(3,4))
        tsStrt = 0
        ssStrt = 0
        ## write header
        fts.write("%s   %s\n" % ("Search", yy.dateTime.text()))
        while 1:
         for ts in range(tsStrt,len(Tsort)):  ## possibly use while
          ifnd = 0  
          if (Tsort[ts][0][0:4] == "TEAM" and Tsort[ts][1] < yy.Nunas_col):
            fts.write("\n%-10.10s %-10.10s\n" % (Tsort[ts][0], Tsort[ts][4]))
            scnt = Tsort[ts][3]  ## numb of srchr's in team
            sloc = Tsort[ts][1]*yy.Nrows + Tsort[ts][2] + 1   ## addr of first srchr in team
            tsStrt = ts + 1
            ifnd = 1
            break
         ccnt = 0
         ssStrt = 0  ## have to restart search for srchr due to possible ordering
         if (ifnd == 1):
          for ss in range(ssStrt,len(Ssort)):
           cloc = Ssort[ss][3]*yy.Nrows + Ssort[ss][4]  
           if (cloc == sloc):
             lead = ""
             med = ""
             if (DEBUG == 1): print(Ssort[ss][7])
             if (Ssort[ss][7]=="1"):
               lead = "LEAD"
             if (Ssort[ss][8]=="1"):
               med = "MED"
             fts.write("%-20.20s %-4.4s %-4.4s %-3.3s\n" % (Ssort[ss][0], Ssort[ss][1], lead , med))  
             ccnt = ccnt + 1
             sloc = sloc + 1
             ssStrt = ss + 1
             if (ccnt == scnt):
               break      ## got all of team
         else:
          if (DEBUG == 1): print("End")
          break           ##  output all teams
        fts.close()

    def cell_was_clicked(self, row, column):
        ##
        if self.selected :
            self.selected = 0  # reset after 1 more click
            return
        if (QtWidgets.qApp.mouseButtons() & QtCore.Qt.LeftButton):
            if (DEBUG == 1): print("LMB")
        self.selected = 1
        if (DEBUG == 1): print("Row %d and Column %d was clicked" % (row+1, column+1))
        item = self.tableWidget.item(row, column)  
        if (DEBUG == 1):
          if (item != None): print("Item is #%s#\n" % item.text())
          else: print("*** Item was None ***")
        self.ID = item.text()
        self.lrow = row  ## previous row/column
        self.lcolumn = column
        self.repaint()
        if (DEBUG == 1): print(".....repaint click.....")        
        
    def cell_was_Dclicked(self, row, column):
        ## Does a double click always also create a single click?
        ## appears default item change is by double click; can this be turned-off? yes
        if (DEBUG == 1): print("Row %d and Column %d was Dclicked" % (row+1, column+1))
        text = self.ID

        ##  currentRow or currentColumn  itemAt gives item, not contents
        ##      using .text() will give the contents

    def dialog_was_clicked(self, row, column): ## tableWidget2  RMB for Team (settable)
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0  # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget2.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG HIDE: Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 3): item = self.tableWidget2.item(row, column) 
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 3):
          self.tableWidget2.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display)  (otherwise leave them alone)
              if (DEBUG == 1): print("FOUND: %s %s"% (self.tableWidget.fnd_team,self.tableWidget2.item(0,1).text()))
              self.zz2.TEAMS[self.tableWidget.fnd_team][0] = self.tableWidget2.item(0,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][4] = self.tableWidget2.item(1,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][5] = self.tableWidget2.item(2,1).text()                    
              self.zz2.tabload(self.mm,0)

    def dialog_was_clicked4(self, row, column): ## tableWidget2  RMB for Searcher Detail (view only, except remove)
        ##
        yy = self.mm
        zz = self.zz2
        
        if self.selected :         ## PROBABLY not used??
            self.selected = 0      # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget5.item(4, 1)   ## info at Remove?
        if (item.text().upper() == "Y"):      ## Yes remove
            if (row == 5 and column == 0):
               ptr = self.tableWidget.fnd_srchr
               if (self.zz2.SRCHR[ptr][5] != yy.Nunas_col and zz.SRCHR[ptr][6] != 1 ): ## TEAM of SRCHR must be UNASSIGNED
                  winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, searcher not found
                  return          
               TimeOUT = time.time()          ## add to MEMBERS record
               memPtr = -1
               for xx in range(0,len(zz.MEMBERS)):           ## find the MEMBERS record
                   if (zz.MEMBERS[xx][1] == zz.SRCHR[ptr][2] and zz.MEMBERS[xx][2] == zz.SRCHR[ptr][1]): # match Id, Agency
                       memPtr = xx
                       break               
               zz.MEMBERS[memPtr][6] = TimeOUT         ##  set as checked-out (AT some point want to add total time field
               zz.MEMBERS[memPtr][9] = float(zz.MEMBERS[memPtr][9]) + zz.MEMBERS[memPtr][6] - float(zz.MEMBERS[memPtr][5])  ## cum time
               zz.MEMBERS[memPtr][5] = -1              ## reset for next checkin               
               rowy = zz.SRCHR[ptr][4]
               colx = zz.SRCHR[ptr][3]
               npt = rowy + (colx - yy.Nunas_col)*yy.Nrows
               zz.UNAS_USED[npt] = 0
               del zz.SRCHR[ptr]                       ## we are deleting the record and marking MEMBERS entry with TimeOUT
        if (DEBUG == 1): print("DIALOG HIDE: Row %d and Column %d was clicked" % (row+1, column+1))
        if (row == 5):
          self.tableWidget5.hide()
        zz.tabload(yy,0)
        ##   really no need to update the table unless remove is happening                   


    def dialog_was_clicked2(self, row, column): ## tableWidget3  RMB last column groups
        ##
        if (DEBUG == 1): print("Dialog3 GROUPS row: %i, column: %i"%(row, column))
        item = self.tableWidget3.item(row,column).text()
        if (row == 4): return    # set choice value
        if (row == 5):           ## This is OK.  Need to set group name for choice first 
            item = self.tableWidget3.item(4,0).text()
            if (item == "<create>"):      ## not set so skip
                self.tableWidget3.hide()
                return    
            self.tableWidget3.setItem(4,0,QtWidgets.QTableWidgetItem("<create>"))  # reset to default 
        self.tableWidget3.hide()
        self.zz2.TEAMS.insert(self.zz2.TEAMS.index(["END"]),[item, \
                    self.tableWidget.ccm, self.tableWidget.rrm, 0, item, "--", 0.0]) # insert prior to END                    
        self.zz2.tabload(self.mm,0)

    def dialog_was_clicked3(self, row, column): ## tableWidget4  RMB out-of-bounds FIND
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0      # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget4.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG4 OUT-OF-Bounds Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 5): item = self.tableWidget4.item(row, column)  
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 5):
          self.tableWidget4.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display)  (otherwise leave them alone)
              if (DEBUG == 1): print("Looking for SrchrId %s and Agency %s"%(findSrchrId,findAgncy))
              self.zz2.findSrchrId = self.tableWidget4.item(1,1).text()
              self.zz2.findAgncy = self.tableWidget4.item(3,1).text()
              self.zz2.findName = self.tableWidget4.item(2,1).text()
              self.zz2.findResource = self.tableWidget4.item(4,1).text()
              if (self.zz2.findResource == " " or len(self.zz2.findResource) == 0):
                  self.zz2.findResource = "xxx"     # set to value that will not match
              if (self.zz2.findName == " " or len(self.zz2.findName) == 0):
                  self.zz2.findName = "xxx"         # set to value that will not match
  ### ?  Add info for resource type             
              if (self.zz2.findAgncy == " "): self.zz2.findAgncy = "NC"   ## the default
          else:              ## cancel
              self.zz2.findSrchrId = "0"
              self.zz2.findAgncy = " "
              self.zz2.findName = "xxx"
              self.zz2.findResource = "xxx"  # set to not match 'blank'
          self.zz2.tabload(self.mm,0)        ## for Ok or Cancel update the maintable           

#### end of TableApp class



def xmodel(mdx) :
    ## routine outside of class TableApp
    
    if (DEBUG == 1): print("In xmodel %i\n" % mdx)  ##TableApp.modex
    return

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    if (DEBUG == 1): print("B4 form define\n")
    form = TableApp()  # We set the form to be our ExampleApp (table)
    if (DEBUG == 1): print("B4 form show\n")
    form.show()  # Show the form
    if (DEBUG == 1): print("Call app\n")
    app.exec_()  # and execute the app
    


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
