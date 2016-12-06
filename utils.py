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
  return bcolors.OKBLUE + text + bcolors.ENDC

def greenText(text):
  return bcolors.OKGREEN + text + bcolors.ENDC

def redText(text):
  return bcolors.FAIL + text + bcolors.ENDC
