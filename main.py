import os
import sys
from utils import *
import commands
import traceback
import cmd

commandsInfo = [
  {
    "name" : "add_cat",
    "params" : "<inf_id>", 
    "description" : "add category for influencer"
    },
    {
    "name" : "add_resp",
    "params" : "<inf_id> <cat_id>", 
    "description" : "add response to influencer's category"
    },
    {
    "name" : "bfnl",
    "params" : "<inf_id>", 
    "description" : "see list of longest conversations for <inf_id>"
    },    
    {
    "name" : "cat",
    "params" : "<inf_id>", 
    "description" : "see list of categories for <inf_id>"
    },
    {
    "name" : "cards_bfnl",
    "params" : "<inf_id>", 
    "description" : "List BFNL cards"
    },    
    {
    "name" : "cards_gm",
    "params" : "<inf_id>", 
    "description" : "List Grouped Messages cards"
    },
    {
    "name" : "cards_om",
    "params" : "<inf_id>", 
    "description" : "List Outbound Messages cards"
    },    
    {
    "name" : "conv",
    "params" : "<conv_id>",
    "description" : "see particular conv. with <conv_id>"
    },
    {
    "name" : "gm_revivable",
    "params" : "<inf_id>", 
    "description" : "list GM cards that can be revived"
    },
    {
    "name" : "gm_reopen",
    "params" : "<card_id> <group_id>", 
    "description" : "reopen GM card by appending new group"
    },
    {
    "name" : "gm_LDA",
    "params" : "<card_id> <k>", 
    "description" : "run LDA with k topics on gm card's messages"
    },
    {
    "name" : "gm_add_group",
    "params" : "<inf_id>", 
    "description" : "add/set group of GM Card's last messages"
    },
    {
    "name" : "gm_set_group",
    "params" : "<group_id> <topic> <threshold>", 
    "description" : "set group_id for all messages in topic (>threshold)"
    },
    {
    "name" : "inf",
    "params": "",  
    "description" : "see list of influencers"
    },
    {
    "name" : "LDA",
    "params" : "<inf_id> <k>", 
    "description" : "run LDA with k topics for influencer's messages"
    },
    {
    "name" : "mes",
    "params" : "<inf_id>", 
    "description" : "see list of messages for <inf_id>"
    },
    {
    "name" : "new_card_bfnl",
    "params" : "<inf_id> <conv_id>", 
    "description" : "add new bfnl card"
    },
    {
    "name" : "new_card_outbound",
    "params" : "<inf_id>", 
    "description" : "add new outbound card"
    },
    {
    "name" : "prompt",
    "params" : "<inf_id> <cat_id>", 
    "description" : "prompt influencer to respond to category"
    },
    {
    "name" : "resp",
    "params" : "<inf_id> <cat_id>", 
    "description" : "see list of responses for influencers category"
    },
    {
    "name" : "set_cat_batch",
    "params" : "<cat_id> <topic> <threshold>", 
    "description" : "set category of all messages with in topic (>threshold)"
    },
    {
    "name" : "set_cat",
    "params" : "<cat_id> <mes_id>", 
    "description" : "set category of a single message"
    },
    {
    "name" : "send_push",
    "params" : "<inf_id>", 
    "description" : "send custom push notification to influencer"
    },
    {
    "name" : "topics",
    "params": "", 
    "description" : "show topics discovered by LDA, each with 10 rep words"
    },
    {
    "name" : "topic_all",
    "params" : "<k> <n>:", 
    "description" : "show topic k with its best n samples"
    },
    {
    "name" : "exit",
    "params": "", 
    "description" : "exit the program"
    }
]

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

  def do_bfnl(self, line):
    if (self.nArgs != 1):
      self.default(line)
      return False
    commands.listBFNL(int(self.cmdTokens[1]))

  def do_conv(self, line):
    if (self.nArgs != 1):
      self.default(line)
      return False
    commands.listConv([int(self.cmdTokens[1])])

  def do_new_card_bfnl(self, line):
    if (self.nArgs != 2):
      self.default(line)
      return False
    commands.newCardBFNL(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_new_card_outbound(self, line):
    if (self.nArgs != 1):
      self.default(line)
      return False
    omPrompt = raw_input(greenText("Type the prompt for OM Card:"))    
    commands.newCardOutbound(int(self.cmdTokens[1]), omPrompt)

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

  def do_cards_bfnl(self, line):
    if(self.nArgs != 1):
      self.default(line)
      return False
    commands.listBFNLCards(int(self.cmdTokens[1]))

  def do_cards_gm(self, line):
    if(self.nArgs != 1):
      self.default(line)
      return False
    commands.listGMCards(int(self.cmdTokens[1]))

  def do_cards_om(self, line):
    if(self.nArgs != 1):
      self.default(line)
      return False
    commands.listOMCards(int(self.cmdTokens[1]))

  def do_gm_revivable(self, line):
    if(self.nArgs != 1):
      self.default(line)
      return False
    commands.listRevivableGMCards(int(self.cmdTokens[1]))

  def do_gm_LDA(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.runLDAForGMCard(int(self.cmdTokens[1]), int(self.cmdTokens[2]), 100000)

  def do_gm_reopen(self, line):
    if(self.nArgs != 2): 
      self.default(line)
      return False
    commands.reopenGMCard(int(self.cmdTokens[1]), int(self.cmdTokens[2]))

  def do_gm_add_group(self, line):
    if(self.nArgs != 1): 
      self.default(line)
      return False
    groupCaption = raw_input(greenText("Type the new group name:"))
    groupDisplay = raw_input(greenText("Type the new group DISPLAY name:"))
    commands.addGMGroup(int(self.cmdTokens[1]), groupCaption, groupDisplay)

  def do_gm_set_group(self, line):
    if(self.nArgs != 3): 
      self.default(line)
      return False
    commands.setGMGroup(int(self.cmdTokens[1]), int(self.cmdTokens[2]), float(self.cmdTokens[3]))

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
    for c in commandsInfo:
      print blueText(fixedLengthStr(c["name"], 15) + " " + c["params"]) + ": " + c["description"]


def getBaseUrl(argv):
  if len(argv) > 1 and argv[1] == "staging":
    return "http://node-beast-staging.herokuapp.com/api/cli"
  elif len(argv) > 1 and argv[1] == "prod":
    return "http://node-beast-prod.herokuapp.com/api/cli"
  elif len(argv) > 1 and argv[1] == "local":
    return "https://ffe30f0c.ngrok.io/api/cli"
  else:
    return "http://node-beast-dev.herokuapp.com/api/cli"


if __name__ == '__main__':
  commands.baseUrl = getBaseUrl(sys.argv)
  cli = CLI()  
  cli.printOptions()  
  cli.prompt = greenText("(CLI)>>> ")
  cli.cmdloop()


