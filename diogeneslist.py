import os
import sys
import datetime
from os.path import getsize

# global variables definition
appName = "DiogenesList"
appVer = "1.0"
genDate = datetime.datetime.now().strftime("%d/%m/%Y")
genTime = datetime.datetime.now().strftime("%H:%M")
appLink = "http://zapperdj.net"
dirData = ""
numFiles=0 
numDirs=0 
grandTotalSize=0
linkFiles="false" # file linking not yet implemented



# functions definition
def generateDirArray(dirToScan):
    global dirData
    global numFiles
    global numDirs
    global grandTotalSize
    # assing a number identifier to each directory
    i = 1
    dirIDsDictionary = {}
    dirIDsDictionary[dirToScan] = 0
    for currentDir, dirs, files in os.walk(dirToScan):
        for dir in dirs:
            dirIDsDictionary[currentDir+'/'+dir] = i
            i = i + 1

    # initilize array to hold all dir data, dimensioning it to hold the total number of dirs
    allDirArray=[]
    for p in range(i):
        allDirArray.append(p)

    # traverse the directory tree     
    for currentDir, dirs, files in os.walk(dirToScan):
        currentDirId=dirIDsDictionary[currentDir]
        currentDirArray=[]  # array to hold all current dir data
        currentDirModifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(currentDir))
        currentDirModifiedTime = currentDirModifiedTime.strftime("%d/%m/%Y %H:%M:%S")
        currentDirFixed = currentDir.replace("/","\\\\")    # replace / with \\ in the dir path (necessary for javascript functions to work properly
        currentDirArray.append(currentDirFixed+'*0*'+currentDirModifiedTime)   # append directory info to currentDirArray 
        totalSize = 0
        for file in files:
			numFiles = numFiles + 1
			fileSize = getsize(currentDir+'/'+file)
			totalSize = totalSize + fileSize
			grandTotalSize = grandTotalSize + fileSize
			fileModifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(currentDir+'/'+file))
			fileModifiedTime = fileModifiedTime.strftime("%d/%m/%Y %H:%M:%S")
			currentDirArray.append(file+'*'+str(fileSize)+'*'+fileModifiedTime)   # append file info to currentDirArray
        currentDirArray.append(totalSize)   # append total file size to currentDirArray
        # create the list of directory IDs correspondent to the subdirs present on the current directory
        # this acts as a list of links to the subdirectories on the javascript code
        dirLinks = ''
        for dir in dirs:
			numDirs = numDirs + 1
			dirLinks = dirLinks + str(dirIDsDictionary[currentDir+'/'+dir]) + '*'
        dirLinks = dirLinks[:-1]    # remove last *
        currentDirArray.append(dirLinks)
        allDirArray[currentDirId]=currentDirArray   # store currentDirArray on the correspondent position of allDirArray


    # from allDirArray, generate the text to replace [DIR DATA] on HTML file
    #
    # dirData format:
    #
    #   dirs[DIRECTORY_ID] =
    #   "DIRECTORY_PATH*0*MODIFIED_TIME",
    #   "FILENAME*FILESIZE*MODIFIED_TIME",
    #   ...
    #   TOTAL_FILE_SIZE,
    #   "SUBDIRECTORY_ID*SUBDIRECTORY_ID*SUBDIRECTORY_ID*...",
    #   ];

    for d in range(len(allDirArray)):
        dirData=dirData+"dirs["+str(d)+"] = [\n"
        for g in range(len(allDirArray[d])):
            if type(allDirArray[d][g]) == int:
                dirData=dirData+str(allDirArray[d][g])+",\n"
            else:
                dirData=dirData+'"'+allDirArray[d][g]+'",\n'
        dirData=dirData+"];\n"
        dirData=dirData+"\n"

    return 



def generateHTML(dirData,appName,appVer,genDate,genTime,title,appLink,numFiles,numDirs,grandTotalSize,linkFiles):
	templateFile = open('template.html', 'r')
	outputFile = open(title+'.html', 'w')
	for line in templateFile:
		modifiedLine = line
		modifiedLine = modifiedLine.replace('[DIR DATA]', dirData)
		modifiedLine = modifiedLine.replace('[APP NAME]', appName)
		modifiedLine = modifiedLine.replace('[APP VER]', appVer)
		modifiedLine = modifiedLine.replace('[GEN DATE]', genDate)
		modifiedLine = modifiedLine.replace('[GEN TIME]', genTime)
		modifiedLine = modifiedLine.replace('[TITLE]', title)
		modifiedLine = modifiedLine.replace('[APP LINK]', appLink)
		modifiedLine = modifiedLine.replace('[NUM FILES]', str(numFiles))
		modifiedLine = modifiedLine.replace('[NUM DIRS]', str(numDirs))
		modifiedLine = modifiedLine.replace('[TOT SIZE]', str(grandTotalSize))
		modifiedLine = modifiedLine.replace('[LINK FILES]', linkFiles)
		outputFile.write(modifiedLine)
	templateFile.close()
	outputFile.close()
	




# main program start point
if len(sys.argv) < 3:	# check if required arguments are supplied
	print "Missing arguments. This tool should be used as follows:"
	print "	diogeneslist pathToIndex outputFileName"
else:
	pathToIndex = str(sys.argv[1])
	title = str(sys.argv[2])
	if os.path.exists(pathToIndex):	# check if the specified directory exists
		generateDirArray(pathToIndex)
		generateHTML(dirData,appName,appVer,genDate,genTime,title,appLink,numFiles,numDirs,grandTotalSize,linkFiles)
	else:
		print "The specified directory doesn't exist"

    
        
