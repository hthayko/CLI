import os
import sys
from utils import *
import commands
import traceback
import cmd

class CLI(cmd.Cmd):
  """Simple command processor example."""
  # def __init__(self):
  #   # self.prompt = "CLI"
  #   a = 1
  def precmd(self, line):
    self.cmdTokens = [t.strip() for t in line.rsplit(" ") if t.strip() != ""]
    self.nArgs = len(self.cmdTokens) - 1
    return line

  def do_inf(self, line):
    if(self.nArgs != 0): 
      self.default(line)
      return False
    commands.listInfluencers()

  def do_cat(self, line):
    if(self.nArgs != 1): 
      self.default(line)
      return False
    commands.listCategories(int(self.cmdTokens[1]))

  def do_resp(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.listResponses(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_add_cat(self, line):
    if(self.nArgs != 1): 
      self.default(line)
      return False
    catCaption = raw_input(greenText("Type the new category name:"))
    catDisplay = raw_input(greenText("Type the new category DISPLAY name:"))
    commands.addCategory(int(self.cmdTokens[1]), catCaption, catDisplay)

  def do_add_resp(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    response = raw_input(greenText("Type the new response:"))
    commands.addResponse(int(self.cmdTokens[1]), int(self.cmdTokens[2]), response)

  def do_mes(self, line):
    if(self.nArgs != 1): 
      self.default(line)
      return False
    commands.listMessages(int(self.cmdTokens[1]))

  def do_set_cat(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.setCat(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_set_cat_batch(self, line):
    if(self.nArgs != 3): 
      self.default(line)
      return False
    commands.setCatBatch(int(self.cmdTokens[1]), int(self.cmdTokens[2]), float(self.cmdTokens[3]))

  def do_LDA(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.runLDA(int(self.cmdTokens[1]), int(self.cmdTokens[2]), 100000)
    # commands.runLDA(None, int(self.cmdTokens[1]), 100000)

  def do_topics(self, line):
    if(self.nArgs != 0): 
      self.default(line)
      return False
    commands.ldaTopics()

  def do_topic_all(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.ldaMessagesByTopic(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_prompt(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.promptInf(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_send_push(self, line):
    if(self.nArgs != 1):
      self.default(line)
      return False
    message = raw_input(greenText("Type the push message:"))      
    commands.sendPush(int(self.cmdTokens[1]), message)

  def default(self, line):
    print redText("the command " + line + " was not found.")
    self.printOptions()

  def do_EOF(self, line):     
      print "\n"
      return True

  def do_exit(self, line):     
      print "\n"
      return True

  def emptyline(self):
    pass

  def printOptions(self):
    print blueText("\n------------------------------------------------------------------")
    print blueText("add_cat <inf_id>:") + " add category for influencer"
    print blueText("add_resp <inf_id> <cat_id>:") + " add response to influencer's category"
    print blueText("cat <inf_id>:") + " see list of categories for <inf_id>"
    print blueText("LDA <infId> <k>:") + " run LDA with k topics for influencer's messages"
    print blueText("mes <inf_id>:") + " see list of messages for <inf_id>"
    print blueText("prompt <inf_id> <cat_id>:") + " prompt influencer to respond to category"    
    print blueText("inf:") + " see list of influencers"
    print blueText("resp <inf_id> <cat_id>:") + " see list of responses for influencers category"
    print blueText("set_cat_batch <cat_id> <topic> <threshold>:") + " set category of all messages with in topic (>threshold)"
    print blueText("set_cat <cat_id> <mes_id>:") + " set category of a single message"
    print blueText("send_push <inf_id>:") + " send custom push notification to influencer"
    print blueText("topics:") + " show topics discovered by LDA, each with 10 rep words"
    print blueText("topic_all k n:") + " show topic k with its best n samples"
    print blueText("exit:") + " exit the program"

def getBaseUrl(argv):
  if len(argv) > 1 and argv[1] == "staging":
    return "http://node-beast-staging.herokuapp.com/api/cli"
  elif len(argv) > 1 and argv[1] == "prod":
    return "http://node-beast-prod.herokuapp.com/api/cli"
  else:
    return "http://node-beast-dev.herokuapp.com/api/cli"    

if __name__ == '__main__':
  commands.baseUrl = getBaseUrl(sys.argv)
  cli = CLI()  
  cli.printOptions()  
  cli.prompt = greenText("(CLI)>>> ")
  cli.cmdloop()
