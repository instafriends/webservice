#!/usr/bin/env python

import webapp2
import urllib2
import json

class MainPage(webapp2.RequestHandler):
  def get(self):
    token = self.request.get('token', False)
    if token:
      self.response.headers['Content-Type'] = 'text/plain'
      inst = Instafriends(token)
      userid = inst.getMyOwnID()
      if userid != 0:
        inst.userid = userid
        result = inst.processMyInfo()
        result =  result.replace(' ','')
        self.response.out.write(result)
      else:
        self.response.out.write('{error:error}')
    else:
      self.response.out.write('{error:error}')

class Instafriends:
  def __init__(self, token):
    self.token = token
    self.userid = 0
    self.requestsLimit = 100
  def getToken(self):
    return self.token
  def getResultByURL(self, url):
    result = {}
    if self.requestsLimit > 0:
      self.requestsLimit = self.requestsLimit - 1
      response = urllib2.urlopen(url)
      if response.code == 200:
        jsonResult = json.loads(response.read())
        if 'data' in jsonResult:
          for user in jsonResult['data']:
            result[user['username']] = user
        if 'pagination' in jsonResult:
          if 'next_url' in jsonResult['pagination']:
            next_url = jsonResult['pagination']['next_url']
            resultTemp = self.getResultByURL(next_url)
            for k, v in resultTemp.iteritems():
              result[k] = v
    return result
  
  def getFollows(self):
    url = 'https://api.instagram.com/v1/users/' + self.userid + '/follows?count=100&access_token=' + self.token
    result = self.getResultByURL(url)
    return result
  
  def getFollowedBy(self):
    url = 'https://api.instagram.com/v1/users/' + self.userid + '/followed-by?count=100&access_token=' + self.token
    result = self.getResultByURL(url)
    return result

  def getMyOwnID(self):
    url = 'https://api.instagram.com/v1/users/self/?access_token=' + self.token
    response = urllib2.urlopen(url)
    result = 0
    if response.code == 200:
      jsonResult = json.loads(response.read())
      if 'data' in jsonResult:
        if 'id' in jsonResult['data']:
          result = jsonResult['data']['id']
    return result

  def processMyInfo(self):
    follows = self.getFollows();
    followedBy = self.getFollowedBy();
    result = {}
    result['friends'] = {}
    result['fans'] = {}
    result['followings'] = {}

    for k, v in follows.iteritems():
      if k in followedBy:
        user = {'username':v['username'],'profile_picture':v['profile_picture'],'id':v['id']}
        result['friends'][k] = user
      else:
        user = {'username':v['username'],'profile_picture':v['profile_picture'],'id':v['id']}
        result['followings'][k] = user
    for k, v in followedBy.iteritems():
      if k in follows:
        user = {'username':v['username'],'profile_picture':v['profile_picture'],'id':v['id']}
        result['friends'][k] = user
      else:
        user = {'username':v['username'],'profile_picture':v['profile_picture'],'id':v['id']}
        result['fans'][k] = user

    result['fans'] = json.dumps(result['fans'], sort_keys=True, ensure_ascii=False)
    result['friends'] = json.dumps(result['friends'], sort_keys=True, ensure_ascii=False)
    result['followings'] = json.dumps(result['followings'], sort_keys=True, ensure_ascii=False)

    fans = result['fans'].replace('\\','')
    if fans.startswith('"'):
      fans = fans[1:]
      fans = fans[:-1]
    result['fans'] = fans

    friends = result['friends'].replace('\\','')
    if friends.startswith('"'):
      friends = friends[1:]
      friends = friends[:-1]
    result['friends'] = friends

    followings = result['followings'].replace('\\','')
    if followings.startswith('"'):
      followings = followings[1:]
      followings = followings[:-1]
    result['followings'] = followings

    theJson = json.dumps(result)

    theJson = theJson.replace('\\','').replace('"{','{').replace('}"','}')

    return theJson
    #

app = webapp2.WSGIApplication([('/', MainPage)])



