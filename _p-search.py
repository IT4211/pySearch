import argparse
import os
import logging

log = logging.getLogger('main._psearch')

MIN_WORD = 5
MAX_WORD = 15
PREDECESSOR_SIZE = 32
WINDOW_SIZE = 128

def ParseCommandLine():
    parser = argparse.ArgumentParser('Python Search')

    parser.add_argument('-v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('-k', '--keyWords', type= ValidateFileRead, required=True,
                        help="specify the file containing search words")
    parser.add_argument('-t', '--srchTarget', type= ValidateFileRead, required=True,
                        help="specify the target file to search")
    parser.add_argument('-m', '--theMatrix', type= ValidateFileRead, required=True,
                        help="specify the weighted matrix file")

    global gl_args

    gl_args = parser.parse_args()

    DisplayMessage("Command line processed: Successfully")

    return

def ValidateFileRead(theFile):

    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')


def DisplayMessage(msg):

    if gl_args.verbose:
        print(msg)

    return

def SearchWords():

    searchWords = set()

    try:
        fileWords = open(gl_args.keyWords)
        for line in fileWords:
            searchWords.add(line.strip())
    except:
        log.error('Keyword File Failure:' + gl_args.keyWords)
        sys.exit()
    finally:
        fileWords.close()

    log.info('Search Words')
    log.info('Input File:' + gl_args.keyWords)
    log.info(searchWords)

    try:
        targetFile = open(gl_args.srchTarget, 'rb')
        baTarget = bytearray(targetFile.read())
    except:
        log.error('Target File Failure:' + gl_args.srchTarget)
        sys.exit()
    finally:
        targetFile.close()

    sizeOfTarget = len(baTarget)

    log.info('Target of Search:' + gl_args.srchTarget)
    log.info('File Size:' + str(sizeOfTarget))

    baTargetCopy = baTarget

    wordCheck = class_Matrix()

    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if not character.isalpha():
            baTarget[i] = 0

    indexOfWords = []

    cnt = 0
    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if character.isalpha():
            cnt += 1
        else:
            if(cnt>=MIN_WORD and cnt<=MAX_WORD):
                newWord = ""
                for z in range(i-cnt, i):
                    newWord = newWord + chr(baTarget[z])
                newWord = newWord.lower()
                if(newWord in searchWords):
                    PrintBuffer(newWord, i-cnt, baTargetCopy, i-PREDECESSOR_SIZE, WINDOW_SIZE)
                    indexOfWords.append([newWord, i-cnt])
                    cnt = 0
                    print
                else:
                    if wordCheck.isWordProbable(newWord):
                        indexOfWords.append([newWord, i-cnt])
                    cnt = 0
            else:
                cnt = 0

    PrintAllWordsFound(indexOfWords)

    return

def PrintHeading():

    print("Offset 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F   ASCII")
    print("--------------------------------------------------------------")

    return

def PrintBuffer(word, directOffset, buff, offset, hexSize):

    print "Found: " + word + " At Address: ",
    print "%08x     " % (directOffset)

    PrintHeading()

    for i in range(offset, offset + hexSize, 16):
        for j in range(0, 16):
            if (j == 0):
                print "%08x " % i
            else:
                byteValue = buff[i+j]
                print "%02x " % byteValue,
        print " ",
        for j in range(0, 16):
            byteValue = buff[i+j]
            if(byteValue >= 0x20 and byteValue <= 0x7f):
                print "%c" % byteValue,
            else:
                print '.',
        print
    return

def PrintAllWordsFound(wordList):

    print "Index of All Words"
    print "--------------------"

    wordList.sort()

    for entry in wordList:
        print entry

    print "--------------------"
    print

    return

class class_Matrix:

    weightedMatrix = set()

    def __init__(self):
        try:
            fileTheMatirx = open(gl_args.theMatrix, 'rb')
            for line in fileTheMatirx:
                value = line.strip()
                self.weightedMatrix.add(int(value,16))

        except:
            log.error('Matrix File Error:' + gl_args.theMatrix)
            sys.exit()

        finally:
            fileTheMatirx.close()

        return

    def isWordProbable(self, theWord):

        if(len(theWord) < MIN_WORD):
            return False
        else:
            BASE = 96
            wordWeight = 0

            for i in range(4,0,-1):
                charValue = (ord(theWord[i]) - BASE)
                shiftValue = (i-1)*8
                charWeight = charValue << shiftValue
                wordWeight = (wordWeight | charWeight)

            if(wordWeight in self.weightedMatrix):
                return True
            else:
                return False
