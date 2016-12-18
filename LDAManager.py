import numpy
import lda
import csv

class LDAManager :
  def __init__(self):
    self.ids = []
    self.messages = []
    self.mesTrain = []
    self.influencers = []
    self.model = None
    self.modelMessages = None


  def readData(self):  
    self.ids = []
    self.messages = []
    self.influencers = []    
    with open('allMessages.csv', 'rb') as csvfile:
      csvReader = csv.reader(csvfile)
      for row in csvReader:
        if row[1] == "morggkatherinee":
          self.ids.append(row[0])
          self.influencers.append(row[1])
          self.messages.append(row[2])
    
  def getDataMatrix(self, messages, vocab):
    n = len(messages)
    m = len(vocab)
    dataX = numpy.zeros(shape=(n,m), dtype=int)
    vWordIndex = dict((vocab[i], i) for i in range(m))
    for i in range(n):
      mes = messages[i]
      for w in mes.rsplit(" "):
        if w != "":
          dataX[i][vWordIndex[w]] = dataX[i][vWordIndex[w]] + 1
    return dataX


  def runLDA(self, mesData, k = 10, useN = 100):
    self.model = lda.LDA(n_topics = k, n_iter = 150, random_state = 1)
    if mesData is None: # use default data for demo purposes    
      self.readData()
    else:
      self.messages = mesData[0]
      self.ids = mesData[1]
    mesTrain = self.messages[:useN]    
    vocab = list(set([w for m in mesTrain for w in m.rsplit(" ")]))
    vocab = [v for v in vocab if v != ""]
    vocab.sort()
    dataX = self.getDataMatrix(mesTrain, vocab)
    self.modelMessages = mesTrain
    self.modelVocab = vocab
    self.model.fit(dataX)  # model.fit_transform(X) is also available
    self.mesTopic = [self.model.doc_topic_[i].argmax() for i in range(len(self.modelMessages))]
    self.topicCounts = numpy.zeros(shape=(k), dtype=int)
    for t in self.mesTopic:
      self.topicCounts[t] += 1

  def printTopics(self):
    topic_word = self.model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = numpy.array(self.modelVocab)[numpy.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}, (contains {} phrases)'.format(i, ', '.join(topic_words), self.topicCounts[i]))

  def getBestByTopic(self, topic, filterBy, shouldPrint = False):
    def filterMessages(tm, filterBy):
      if "bestN" in filterBy:
        return tm[:filterBy["bestN"]]
      elif "threshold" in filterBy:
        return [m for m in topicMessages if m[2] >= filterBy["threshold"]]
      else:
        return tm[:100] # if nothing provided, return first 100

    doc_topic = self.model.doc_topic_
    n = len(self.modelMessages)
    topicMessages = [(self.ids[i], i, doc_topic[i].max()) for i in range(n) if doc_topic[i].argmax() == topic]
    topicMessages = sorted(topicMessages, key = lambda x: -x[2])
    bestOf = filterMessages(topicMessages, filterBy)
    if shouldPrint:
      for i in range(len(bestOf)):
        mInd = topicMessages[i][1]
        mAcc = topicMessages[i][2]
        print("{} (top topic: {}, accuracy: {})".format(self.modelMessages[mInd], \
          topic, mAcc))
    else:
      return [(m[0], m[2]) for m in bestOf]
