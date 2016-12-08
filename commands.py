from utils import *
from flask import jsonify, json
import requests
from LDAManager import LDAManager
import traceback

baseUrl = "http://node-beast-dev.herokuapp.com/api/cli"
ldaManager = LDAManager()

def getMessages(infId, limit = 100):
  resp = requests.get(baseUrl + "/get_phrases_with_cli_status", params={
    "influencer_id" : infId, 
    "limit" : limit, 
    "offset" : 0})
  if not checkStatus(resp):
    return
  messages = resp.json()["data"]["messages"]
  return messages

def checkStatus(resp):
  try:
    respObj = resp.json()
    if(respObj["status"] != "success"):
      raise Exception("ERROR: status of the request is:" + respObj["status"])
  except Exception as e:
    print redText(str(e))
    traceback.print_exc()
    return False
  return True

def listInfluencers():
  resp = requests.get(baseUrl + "/get_all_influencers")
  if not checkStatus(resp):
    return
  data = resp.json()["data"]  
  for inf in data:
    print "%s: %s %s(%s)" % (inf["id"], inf["first_name"], (inf["last_name"] or ""), inf["main_phone_number"])
  print greenText("DONE")

def listCategories(infId):
  resp = requests.get(baseUrl + "/get_cats_by_influencer", params={
    "influencer_id" : infId, 
    "limit" : 100, 
    "offset" : 0})
  if not checkStatus(resp):
    return  
  data = resp.json()["data"]["messages"]
  for cat in data:
    print "%s: %s" % (cat["id"], cat["name"])
  print greenText("DONE")

def listResponses(infId, catId):
  resp = requests.get(baseUrl + "/get_resps_by_cat_inf", params = {
    "influencer_id" : infId, 
    "category_id" : catId, 
    "limit" : 100, 
    "offset" : 0})
  if not checkStatus(resp):
    return
  data = resp.json()["data"]
  for r in data:
    print [str(ri) for ri in r["response"]]
  print greenText("DONE")

def addCategory(infId, catName):
  resp = requests.post(baseUrl + "/add_cat_by_name_inf", json = {
    "influencer_id" : infId, 
    "name" : catName
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")


def addResponse(infId, catId, response):
  resp = requests.post(baseUrl + "/add_resp_by_cat_inf", json = {
    "influencer_id" : infId,
    "category_id" : catId,
    "responses" : [response]
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def addResponse(infId, catId, response):
  resp = requests.post(baseUrl + "/add_resp_by_cat_inf", json = {
    "influencer_id" : infId,
    "category_id" : catId,
    "responses" : [response]
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def runLDA(infId, k, useN):
  messagesInfo = getMessages(infId)
  messages = [m["message"] for m in messagesInfo]
  ids = [m["id"] for m in messagesInfo]
  ldaManager.runLDA((messages, ids), k, useN)
  # ldaManager.runLDA(None, k, useN)
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
  ldaManager.getBestByTopic(topicId, n, True)

def listMessages(infId):
  messages = getMessages(infId)
  for m in messages:
    print "%s: %s" % (m["id"], m["message"])
  print greenText("DONE")

def setCat(catId, mesId):
  resp = requests.put(baseUrl + "/update_cli_messages", json = {
    mesId : catId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def promptInf(infId, catId):  
  resp = requests.put(baseUrl + "/prompt_influencer_by_cat_id", json = {
    "influencer_id" : infId,
    "category_id" : catId
    })
  if not checkStatus(resp):
    return
  print greenText("DONE")

def setCatBatch(catId, topicId):
  if not ldaManager.model:
    print redText("TASK CANCELLED: Need to first run LDA...")
    return  
  bestByTopic = ldaManager.getBestByTopic(topicId, 100)
  batchSetData = dict((m[0], catId) for m in bestByTopic)
  resp = requests.put(baseUrl + "/update_cli_messages", json = batchSetData)
  if not checkStatus(resp):
    return
