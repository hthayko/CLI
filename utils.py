class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def blueText(text):
  return "%s%s%s" % (bcolors.OKBLUE, text, bcolors.ENDC)

def greenText(text):
  return "%s%s%s" % (bcolors.OKGREEN, text, bcolors.ENDC)

def redText(text):
  return "%s%s%s" % (bcolors.FAIL, text, bcolors.ENDC)

def fixedLengthStr(str, n):
  return str + "".join([" " for i in range(n - len(str))])