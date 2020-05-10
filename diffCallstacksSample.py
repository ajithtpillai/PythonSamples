# To generate the different callstacks in 2 log files containing callstacks
# To be modified according to variations in your log files

import sys

#Global strings
callstackfilter = "load addr"           # to select lines containing a callstack function, if there is no such tag, modify 'filter for callstack lines' accordingly
interestedlines = "Shredding "          # other lines we are interested in

## Callstack Data structure
##callstackSummary = [
##        {
##            'callstack':stack,
##            'blocktype':block,
##            'count': 1
##          }
##    ]

def doesCallstackMatch(callstack1, callstack2):
    if(len(callstack1) != len(callstack2)):
        return False

    i = 0
    while i<len(callstack1):
        if callstack1[i] != callstack2[i]:
            return False
        i = i+1
    return True

def saveOrIncrCallstack(callstackSummary, stack, block):
    entry={
            'callstack':stack,
            'blocktype':block,
            'count': 1
          }
##    print(entry['callstack'])
##    print(entry['blocktype'])
##    print(entry['count'])
    i = 0
##    print(len(callstackSummary))
    while i< len(callstackSummary):
        if(doesCallstackMatch(callstackSummary[i]['callstack'],stack)):
           callstackSummary[i]['count'] = callstackSummary[i]['count'] + 1
           type = callstackSummary[i]['blocktype']
           if type.find(block) == -1:
               callstackSummary[i]['blocktype'] = type+","+block
           return
        i=i+1

#    print('before adding to callstackSummary')
#    print(entry)
    callstackSummary.append(entry)
#    print('after adding to callstackSummary')
#    print(callstackSummary)

def printStack(stack):
    for item in stack:
                print(item)
    print('\n\n')

def printCallstackSummary(callstackSummaryData, summaryOnly=False):
    verifycount = 0
    for each in callstackSummaryData:
        verifycount = verifycount + each['count']
        if summaryOnly == False:
            print("blocktype = " + each['blocktype'])
            print("count = "+ str(each['count']))
            printStack(each['callstack'])
    print('\n')
    print('unique stacks = ' +str(len(callstackSummaryData)))
    print("total stacks = " + str(verifycount))    
    print('\n\n')

    
def storeCallstacks(callstackSummaryData, filepath):    
    file = open(filepath,'r')

    callstack=[]
    savingcallstack = False
    blocktype=""
    #printCallstackSummary()

    for each in file:
        # if line contains 'load addr'
        #               save line in callstack
        #               if callstack save not on, turn it on
        # else
        #               if callstack save was on
        #                                   save callstack to current entry
        #                                   turn off callstack save
        #                                   init callstack to blank

        lineItems = []
        if each.find(callstackfilter) != -1:            #filter for callstack lines, change if you have a different way to filter
            lineItems = each.split(']')                 #split callstack line based on suitable delimiter
            callstack.append((lineItems[2].rstrip()))   #get the function call from the split list
            if savingcallstack != True:
                savingcallstack = True
        else:
            if savingcallstack:
                savingcallstack = False
##              print("blocktype = "+blocktype)
##              for item in callstack:
##                  print(item)
                saveOrIncrCallstack(callstackSummaryData, callstack, blocktype)
##              print("after saveorincr")
##              print(callstackSummary)
                callstack=[]
                blocktype=""
            if each.find(interestedlines) != -1:           #filter for non-callstack lines interested in
                lineItems = each.split(' ')
    ##          print(lineItems)
                blocktype=lineItems[-2]
    ##          print("blocktype = "+blocktype)

    if savingcallstack:
        saveOrIncrCallstack(callstackSummaryData, callstack, blocktype)

def printStackList(stacklist):
    for each in stacklist:
        printStack(each)
    
def diffCallstackSummaryData(callstackSummaryData1, callstackSummaryData2, diffcount=False):
    diffstacks=[]
    for entry in callstackSummaryData1:
        matchNotFound = True
        for check in callstackSummaryData2:
            if doesCallstackMatch(entry['callstack'],check['callstack']):
                matchNotFound=False
                break
        if matchNotFound:
            diffstacks.append(entry['callstack'])
    
    printStackList(diffstacks)
    print("Num of diff stacks = "+str(len(diffstacks)))

####main code ####

if(len(sys.argv) < 3):
    print("Syntax: diffCallstacks <log file 1> <log file 2>")
    exit()

callstackSummaryData1 = []
callstackSummaryData2 = []

storeCallstacks(callstackSummaryData1,sys.argv[1])
print(sys.argv[1])
printCallstackSummary(callstackSummaryData1, True)

storeCallstacks(callstackSummaryData2,sys.argv[2])
print(sys.argv[2])
printCallstackSummary(callstackSummaryData2, True)

strx = "In '{0}' but not in '{1}'".format(sys.argv[1], sys.argv[2])
print("####################################")
print(strx)
print("####################################\n\n")
diffCallstackSummaryData(callstackSummaryData1, callstackSummaryData2, False)

strx = "In '{0}' but not in '{1}'\n\n".format(sys.argv[2], sys.argv[1])
print("####################################")
print(strx)
print("####################################\n\n")
diffCallstackSummaryData(callstackSummaryData2, callstackSummaryData1, False)
