from utils import *
from flask import jsonify, json
import requests
from LDAManager import LDAManager
import traceback
from pprint import pprint
import csv
import os

baseUrl = "http://node-beast-dev.herokuapp.com" # will be overridden by main
BEAST_API_AUTH_KEY = os.environ.get('BEAST_API_AUTH_KEY', 5000)
ldaManager = LDAManager()

def getMessages(infId, limit = 1000):
  offset = 0
  messages = []
  while 1:
    resp = requests.get(baseUrl + "/api/cli/get_phrases_with_cli_status", params={
      "influencer_id" : infId, 
      "limit" : limit, 
      "offset" : offset})
    if not checkStatus(resp):
      return None
    jsonData = resp.json()["data"]
    messages = messages + jsonData["messages"]
    offset += len(jsonData["messages"])
    print "[DEBUG] Got {} messages".format(len(jsonData["messages"]))
    if len(jsonData["messages"]) == 0:
      break
  return messages

def getGMCardMessages(cardId, limit = 1000):
  offset = 0
  messages = []
  while 1:
    resp = requests.get(baseUrl + "/api/cli/card/answers/" + str(cardId), params={
      "limit" : limit, 
      "offset" : offset})
    if not checkStatus(resp):
      print redText("NO MESSAGES AVAILABLE")
      return []    
    jsonData = resp.json()["data"]
    messages = messages + jsonData
    offset += len(jsonData)
    if len(jsonData) == 0:
      break
  return messages  

def printNiceConv(conv):
  convId = conv[0]["conversation_id"]
  infId = conv[0]["influencer_id"]
  userId = conv[0]["user_id"]
  print "\n<<<<<<< Conversation {} between influencer {} and user {}. (Green is the influencer)".format(convId, infId, userId)
  count = min(10, len(conv))
  if (len(conv) > 10):
    print "... skipped {} message(s) ...".format(len(conv) - 10)
  for i in range(count):
    ind = count - 1 - i
    mes = conv[ind]
    if mes["message"] is None:
      mes["message"] = "IMAGE: %s" % (mes["media"])
    if mes["sent_by_user"]:
      print blueText("%s [%s]" % (mes["message"], mes["time_sent"]))
    else:
      print greenText("%s [%s]" % (mes["message"], mes["time_sent"]))

def checkStatus(resp):
  try:
    respObj = resp.json()
    if(respObj["status"] != "success"):
      raise Exception("ERROR: status of the request is:" + respObj["status"])
  except Exception as e:
    print redText("Bad Request")
    print redText(str(e))
    # traceback.print_exc()
    return False
  return True

def listInfluencers():
  resp = requests.get(baseUrl + "/api/cli/get_all_influencers")
  if not checkStatus(resp):
    return
  data = resp.json()["data"]  
  data = sorted(data, key = lambda x: int(x["id"]))
  for inf in data:
    print "%s: %s %s(%s)" % (inf["id"], inf["first_name"], (inf["last_name"] or ""), inf["main_phone_number"])
  print greenText("DONE")

def listCategories(infId):
  resp = requests.get(baseUrl + "/api/cli/get_cats_by_influencer", params={
    "influencer_id" : infId, 
    "limit" : 100, 
    "offset" : 0})
  if not checkStatus(resp):
    return  
  data = resp.json()["data"]["messages"]
  data = sorted(data, key = lambda x: int(x["id"]))
  for cat in data:
    print "%s: %s" % (cat["id"], cat["name"])
  print greenText("DONE")

def listResponses(infId, catId):
  resp = requests.get(baseUrl + "/api/cli/get_resps_by_cat_inf", params = {
    "influencer_id" : infId, 
    "category_id" : catId, 
    "limit" : 100, 
    "offset" : 0})
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  for r in data:
    print [ri for ri in r["response"]]
  print greenText("DONE")

def getConversations(convIds):
  resp = requests.get(baseUrl + "/api/cli/chats/conversations", params = {
    "conversation_ids[]" : convIds, 
    "limit" : 100})
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  return data

def listConv(convIds):
  convs = getConversations(convIds)
  for (convId, conv) in convs.iteritems():
    printNiceConv(conv)

def addCatHelper(infId, catName, catDisplayName, isCard):
  if catDisplayName == "" or catName == "":
    print redText("category name or display name cannot be empty")
    return 
  resp = requests.post(baseUrl + "/api/cli/add_cat_by_name_inf", json = {
    "influencer_id" : infId, 
    "category_name" : catName,
    "display_name" : catDisplayName,
    "is_card" : isCard
    })
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  if isCard:
    print greenText("Added group with ID:{}".format(data["id"]))  
  else:
    print greenText("Added category with ID:{}".format(data["id"]))  

def addCategory(infId, catName, catDisplayName):
  addCatHelper(infId, catName, catDisplayName, False)

def addResponse(catId, response):
  resp = requests.post(baseUrl + "/api/cli/category/add_response", json = {
    "id" : catId,
    "message" : response
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def runLDA(infId, k, useN, freqToLeave):
  if infId == -1:
    ldaManager.runLDA(None, k, useN)
  else:
    messagesInfo = getMessages(infId)
    print "[DEBUG] Got {} total messages".format(len(messagesInfo))
    messages = [m["message"].encode('utf-8') for m in messagesInfo]
    ids = [m["id"] for m in messagesInfo]
    ldaManager.runLDA((messages, ids), k, useN, freqToLeave)   
  ldaTopics()

def runLDAForGMCard(cardId, k, useN):
  messagesInfo = getGMCardMessages(cardId)
  print "[DEBUG] Got {} messages".format(len(messagesInfo))
  messages = [m["message"].encode('utf-8') for m in messagesInfo]
  ids = [m["id"] for m in messagesInfo]
  ldaManager.runLDA((messages, ids), k, useN)   
  ldaTopics()

def ldaTopics():
  if not ldaManager.model:
    print redText("TASK CANCELLED: Need to first run LDA...")
    return
  ldaManager.printTopics()

def ldaMessagesByTopic(topicId, n):
  if not ldaManager.model:
    print redText("TASK CANCELLED: Need to first run LDA...")
    return
  ldaManager.getBestByTopic(topicId, {"bestN" : n}, True)

def listMessages(infId):
  messages = getMessages(infId)
  messages = sorted(messages, key = lambda x: -int(x["id"]))  
  for m in messages[:100]:
    print "%s: %s" % (m["id"], m["message"])
  print greenText("Fetched {} messages".format(len(messages)))

def setCat(catId, mesId):
  resp = requests.put(baseUrl + "/api/cli/update_cli_messages", json = {
    mesId : catId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def promptInf(infId, catId):  
  resp = requests.put(baseUrl + "/api/cli/prompt_influencer_by_cat_id", json = {
    "influencer_id" : infId,
    "category_id" : catId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def setCatBatch(catId, topicId, threshold):
  if not ldaManager.model:
    print redText("TASK CANCELLED: Need to first run LDA...")
    return  
  bestByTopic = ldaManager.getBestByTopic(topicId, {"threshold" : threshold})
  batchSetData = dict((m[0], catId) for m in bestByTopic)
  resp = requests.put(baseUrl + "/api/cli/update_cli_messages", json = batchSetData)
  if not checkStatus(resp):
    return
  else:
    print greenText("Set category '{}' for {} message(s)".format(catId, len(batchSetData)))

def sendPush(infId, message):
  resp = requests.get(baseUrl + "/api/cli/sendPush", params = {
    "influencer_id" : infId,
    "message" : message
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def sendPushEngage(infId, message):
  resp = requests.post(baseUrl + "/api/cli/sendPush/engage/" + str(infId), json = {
    "message" : message
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")


def addNewCardBFNL(infId, convId):
  resp = requests.post(baseUrl + "/api/cli/new_card", json = {
    "influencer_id" : infId,
    "type" : "conversation",
    "conversation_id" : convId
    })
  if not checkStatus(resp):
    return

def newCardBFNL(infId):
  resp = requests.get(baseUrl + "/api/cli/bfnl/" + str(infId), params = {
    "limit" : 100
    })
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  bfnlCardsMade = 0
  convIds = [c["conversation_id"] for c in data]
  if len(convIds) == 0:
    print redText("No Conversations found")
    return
  for i in range(0, len(convIds)):
    cId = convIds[i]    
    conv = getConversations([cId])
    if(not conv[str(cId)][0]["sent_by_user"]):
      continue
    printNiceConv(conv[str(cId)])
    userInput = raw_input(greenText("Make a BFNL card? (Y/N/exit)"))
    if userInput == "Y":      
      addNewCardBFNL(infId, cId)
      bfnlCardsMade += 1
      print greenText("{} cards made so far".format(bfnlCardsMade))
    elif userInput == "exit":
      print greenText("{} cards made so far".format(bfnlCardsMade))
      break

def newCardGM(infId, catId, fansNum):
  resp = requests.post(baseUrl + "/api/cli/new_card/grouped_message", json = {
    "influencer_id" : infId,
    "group_id" : catId,
    "message" : "fans asked you:"
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def newCardOutbound(infId, omPrompt):
  resp = requests.post(baseUrl + "/api/cli/new_card", json = {
    "influencer_id" : infId,
    "type" : "message_all",
    "relevant_info" : omPrompt
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def listBFNLCards(infId):
  resp = requests.get(baseUrl + "/api/cli/cards/" + str(infId), params = {
    "is_active" : True,
    "state" : "new"
    })
  if not checkStatus(resp):
    return
  cards = resp.json()["data"]["data"]
  cardsBFNL = [c for c in cards if c["type"] == "conversation"]
  for c in cardsBFNL:
    print ("BFNL CARD ID: {}: Between inf {} and user {}, conv id: {}".
      format(c["card_id"], c["influencer_id"], c["user_id"], c["conversation_id"]))
  print greenText("DONE")


def listGMCardsHelper(infId, isActive, state):
  resp = requests.get(baseUrl + "/api/cli/cards/" + str(infId), params = {
    "is_active" : isActive,
    "state" : state
    })
  if not checkStatus(resp):
    return
  cards = resp.json()["data"]["data"]
  cardsGM = [c for c in cards if c["type"] == "grouped_message"]
  for c in cardsGM:
    showGMCard(c)

def listGMCards(infId):
  listGMCardsHelper(infId, True, "new")

def showGMCard(gmCard):
  resp = requests.get(baseUrl + "/api/cli/cards/grouped_message/" + str(gmCard["card_id"]), params = {})
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  mes = gmCard["message"]
  if mes is None:
    mes = "IMAGE: %s" % (gmCard["media"])
  print "\n<<<<<<< GM CARD ID: {}: (Green is the influencer)".format(gmCard["card_id"])
  print greenText(mes)
  for g in data:
    print blueText(g["display_name"])
    if g["response"] is not None:
      print greenText(g["response"][0])

def listOMCards(infId):
  resp = requests.get(baseUrl + "/api/cli/cards/" + str(infId), params = {
    "is_active" : True,
    "state" : "new"
    })
  if not checkStatus(resp):
    return
  cards = resp.json()["data"]["data"]
  cardsOM = [c for c in cards if c["type"] == "message_all"]
  for c in cardsOM:
    print ("OUTBOUND MESSAGE CARD ID: {}: From inf {}: ". format(c["card_id"], c["influencer_id"]) +
      greenText(c["relevant_info"]))
  print greenText("DONE")


# list NEW,  INACTIVE GM cards + DONE, ACTIVE cards
def listRevivableGMCards(infId):
  listGMCardsHelper(infId, False, "new")
  listGMCardsHelper(infId, True, "done")

def reopenGMCard(cardId, groupId):
  resp = requests.post(baseUrl + "/api/cli/reopen_card", json = {
    "card_id" : cardId, 
    "group_id" : groupId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def addGMGroup(infId, groupName, groupDisplayName):
  addCatHelper(infId, groupName, groupDisplayName, True)

def setGMGroup(groupId, topicId, threshold):
  if not ldaManager.model:
    print redText("TASK CANCELLED: Need to first run LDA...")
    return  
  bestByTopic = ldaManager.getBestByTopic(topicId, {"threshold" : threshold})
  batchSetData = dict((m[0], groupId) for m in bestByTopic)
  resp = requests.put(baseUrl + "/api/cli/update_cli_messages", json = batchSetData)
  if not checkStatus(resp):
    return
  else:
    print greenText("Set group '{}' for {} message(s)".format(groupId, len(batchSetData)))

def sendAllFraction(infId, pn, message):
  sentToCount = 0
  resp = requests.put(baseUrl + "/api/cli/send_message_to_convs_by_pn_end", json = {
    "number_ending" : pn,
    "message" : message,
    "influencer_id" : infId
    })
  if not checkStatus(resp):
    return
  sentToCount += resp.json()["count"]
  print greenText("DONE: Sent to {} users".format(sentToCount))

def sendAllPattern(infId, pn_pattern, message):
  sentToCount = 0
  resp = requests.put(baseUrl + "/api/cli/send_message_to_convs_by_pn_pattern", json = {
    "number_pattern" : pn_pattern, # gotata be in format like '+1650%'
    "message" : message,
    "influencer_id" : infId
    })
  if not checkStatus(resp):
    return
  sentToCount += resp.json()["count"]
  print greenText("DONE: Sent to {} users".format(sentToCount))



def onboardInf(twitterHandle, infData):
  resp = requests.post(baseUrl + "/api/cli/onboarding", json = {
    "twitter_username" : twitterHandle,
    "info" : infData
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def genActivationCode(desc):
  resp = requests.post(baseUrl + "/api/activation/generate", json = {
    "description" : desc
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def verifyInf(infId):
  resp = requests.post(baseUrl + "/api/activation/activate", json = {
    "influencer_id" : infId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def importUsers(infId, csvPath):
  payload = []
  with open(csvPath, 'rb') as csvfile:
    csvReader = csv.DictReader(csvfile)
    for row in csvReader:
      udict = extractValidatedUser(row)
      if udict is not None:
        payload.append(udict)
  if len(payload) > 0:
    resp = requests.post(baseUrl + "/api/cli/import_users", 
      json = {
        "users_array" : payload,
        "influencer_id" : infId
        },
      headers = {
        "beast-api-auth" : BEAST_API_AUTH_KEY
      })
    if not checkStatus(resp):
      return
    print greenText("DONE: sent {} users for importing".format(len(payload)))
  else:
    print redText("Found 0 validateed users")

def extractValidatedUser(fullDict):
  ret = {};
  ret["phone_number"] = fullDict["phone_number"]
  ret["first_name"] = fullDict["first_name"]
  ret["last_name"] = fullDict["last_name"]
  ret["email"] = fullDict["email"]
  ret["zip_code"] = fullDict["zip_code"]
  ret["birthday"] = fullDict["birthday"]
  return ret;









