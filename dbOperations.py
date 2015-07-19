#coding = utf-8

import web
import datetime

db = web.database(dbn='mysql', db='RogueAPDetection', user='root')

def insertUser(username,password):
    db.insert('Users',username=username,password=password)

def insertAuthorizedAPs(bssid, ssid, channel, vendor, location):
    db.insert('AuthorizedAPs',bssid=bssid,ssid=ssid,channel=channel,vendor=vendor,location=location)

def deleteAuthorizeAPs(bssid):
    db.delete('AuthorizedAPs',where = 'bssid = $bssid', vars = locals())

def insertAPFeatures(bssid, ssid, channel, vendor, location, security, signal, noise, route):
    db.insert('APsFeatures', bssid=bssid, ssid=ssid, channel=channel, vendor=vendor, location=location, security=security, signal=signal, noise=noise, route=route)

def insertAPCredits(bssid, location_history, useraccess_history, security_history, route_history, credit):
    db.insert('APsCredit', bssid=bssid, location_history=location_history, useraccess_history=useraccess_history, security_history=security_history, route_history=route_history, credit=credit)
'''    
def insertUserAccess(ip, bssid):
    db.insert('UsersAccess',ip=ip,bssid=bssid,connectStart=datetime.datetime.utcnow())
'''
'''
def updateUserAccess(ip, bssid):
    db.update('UsersAccess', where='ip=$ip and bssid=$bssid',vars=locals(),connectEnd=datetime.datetime.utcnow())
'''

def insertRTTValue(bssid, meanProbe, meanDns, devProbe, devDns, rttEval):
    db.insert('RTTEvals', where='bssid=$bssid',vars=locals(),mean_probe=meanProbe,mean_dns=meanDns,dev_probe=devProbe,dev_dns=devDns,rtt_eval=rttEval)

def selectAPCredit(bssid):
    result = db.select('APsCredit', where='bssid=$bssid',vars=locals(),what='credit')
