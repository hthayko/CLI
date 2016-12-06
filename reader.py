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
  def preloop(self, line):
    print "preloop() called!!!" 
    self.cmdTokens = line.rsplit(" ")
    self.nArgs = len(cmdTokens)

  def do_inf(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)
    if(nArgs != 0): return False
    commands.listInfluencers()

  def do_cat(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 1): return False
    commands.listCategories(int(cmdTokens[0]))

  def do_resp(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    commands.listResponses(int(cmdTokens[0]), int(cmdTokens[1]))

  def do_add_cat(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 1): return False
    catCaption = raw_input(greenText("Type the new category name:"))
    commands.addCategory(int(cmdTokens[0]), catCaption)

  def do_add_resp(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    response = raw_input(greenText("Type the new response:"))
    commands.addResponse(int(cmdTokens[0]), int(cmdTokens[1]), response)

  def do_mes(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 1): return False
    commands.listMessages(int(cmdTokens[0]))

  def do_set_cat(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    commands.setCat(int(cmdTokens[0]), int(cmdTokens[1]))

  def do_set_cat_batch(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    commands.setCatBatch(int(cmdTokens[0]), int(cmdTokens[1]))

  def do_LDA(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    commands.runLDA(int(cmdTokens[0]), int(cmdTokens[1]), 100000)

  def do_topics(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 0): return False
    commands.ldaTopics()

  def do_topic_all(self, line):
    cmdTokens = line.rsplit(" ")
    nArgs = len(cmdTokens)    
    if(nArgs != 2): return False
    commands.ldaMessagesByTopic(int(cmdTokens[0]), int(cmdTokens[1]))

  def do_EOF(self, line):     
      print "\n"
      return True