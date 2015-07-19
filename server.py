#coding=utf-8
import time
import traceback
import sys
import web
import hashlib
import os
import dbOperations

#initDatabase()

#Configurations for session
#Non debug mode
#Sessions doesn't work in debug mode because it interfere with reloading
#See session_with_reloader for more details
web.config.debug = False
web.config.session_parameters['cookie_name'] = 'user_session_id'
web.config.session_parameters['cookie_domain'] = None
#24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['timeout'] = 86400,
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
#Randomly generate strings with fixed length as secret key
web.config.session_parameters['secret_key'] = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
web.config.session_parameters['expired_message'] = 'Warning: Session Expired'

# Define urls and the corresponding handlers 
urls = (
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/sendApFeatures', 'SendApFeatures',
    '/sendApQuery', 'SendApQuery',
    '/sendRTTValue', 'SendRTTValue',
    '/updateAuthorizedAPList','UpdateAuthorizedAPList',
    '/fail/(\w+)','Fail',
    '/success/(\w+)','Success',
)

app = web.application(urls,globals())
#session = web.session.Session(app, web.session.DBStore('RogueAPDetection'), initializer={'logged_in': 0})
t_globals = {
    'datestr': web.datestr,
    'cookie' : web.cookies,
}
render = web.template.render('/Users/wuzhenyu/Desktop/templates/', base='base', globals=t_globals)


db = web.database(dbn='mysql', db='RogueAPDetection', user='root')
store = web.session.DBStore(db, 'Sessions')
session = web.session.Session(app, store,initializer={'logged_in': False})

class Fail:
    def GET(self, operation):
        return render.fail(operation)

class Success:
    def GET(self, operation):
        return render.success(operation)

class Login:
    #create login form
    login_form = web.form.Form(
        web.form.Textbox('Username',web.form.notnull,size=30),
        web.form.Password('Password',web.form.notnull,size=30),
        web.form.Button('Login'),
    )
    def GET(self):
        form = self.login_form()
        return render.login(form)
    def POST(self):
        i = web.input()
        username, password = web.net.websafe(i.Username), hashlib.md5(web.net.websafe(i.Password)).hexdigest()
        if not verifyLogin(username,password):
            raise web.seeother('/fail/login')
        else:
            web.setcookie('username', username)
            session.logged_in=True
            raise web.seeother('/success/login')
            
def verifyLogin(username,password):
    return True;

class Logout:
    def GET(self):
        session.logged_in=False
        session.kill()
        web.setcookie('username','',expires=-1)
        raise web.seeother('/success/logout')
        
class Register:
    regist_form = web.form.Form(
        web.form.Textbox('Username',web.form.notnull,size=30,description='No longer than 30 chars'),
        web.form.Password('Password',web.form.notnull,size=30,description='No longer than 30 chars, composed of alphanumerics and contain special chars'),
        web.form.Password('Password2',web.form.notnull,size=30,description='Enter password again, the same as the former'),
        web.form.Button('Register'),
        validators = [web.form.Validator("Passwords do not match, try again", lambda i: i.Password == i.Password2)]
    )
    def GET(self):
        form = self.regist_form()
        return render.register(form)
    def POST(self):
        i = web.input()
        username, password = web.net.websafe(i.Username), hashlib.md5(web.net.websafe(i.Password)).hexdigest()
        if not self.regist_form.validates():
            form = self.regist_form()
            return render.register(form)
        else:
            if not verifyRegister(username,password):
                raise web.seeother('/fail/register')
            else:
                web.setcookie('username', hashlib.md5(username).hexdigest())
                raise web.seeother('/success/register')

def verifyRegister(username,password):
    return False;
        
class SendApFeatures:
    features_form = web.form.Form(
        web.form.Textbox('BSSID',web.form.notnull,size=17),
        web.form.Textbox('SSID',web.form.notnull,size=30),
        web.form.Textbox('Channel',web.form.notnull,size=2),
        web.form.Textbox('Vendor',web.form.notnull,size=20),
        web.form.Textbox('Location',web.form.notnull,size=30),
        web.form.Textbox('Security',web.form.notnull,size=20),
        web.form.Textbox('Signal',web.form.notnull,size=2),
        web.form.Textbox('Noise',web.form.notnull,size=2),
        web.form.Textbox('Route',web.form.notnull,size=30),
        web.form.Button('Submit'),
    )
    def GET(self):
        if session.logged_in == True:
            form = self.features_form()
            return render.apFeatures(form)
        else:
            raise web.seeother('/login')
    def POST(self):
        i = web.input()
        bssid,ssid,channel,vendor,location,security,signal,noise,route = web.net.websafe(i.BSSID),\
        web.net.websafe(i.SSID),web.net.websafe(i.Channel),web.net.websafe(i.Vendor),web.net.websafe(i.Location),\
        web.net.websafe(i.Security),web.net.websafe(i.Signal),web.net.websafe(i.Noise),web.net.websafe(i.Route)
        featuresDict = {'BSSID':bssid, 'SSID':ssid, 'CHANNEL':channel, 'VENDOR':vendor, 'LOCATION':location, 'SECURITY':security, 'SIGNAL':signal, 'NOISE':noise, 'ROUTE':route}
        if not verifyFeatures(featuresDict):
            raise web.seeother('/fail/sendAPFeatures')
        else:
            raise web.seeother('/success/sendAPFeatures')

def verifyFeatures(featuresDict):
    return True

class SendApQuery:
    query_form = web.form.Form(
        web.form.Textbox('BSSID',web.form.notnull,size=17),
        web.form.Button('Query'),
    )
    def GET(self):
        if session.logged_in == False:
            form = self.query_form()
            return render.apQuery(form)
        else:
            raise web.seeother('/login')
    def POST(self):
        i = web.input()
        bssid = web.net.websafe(i.BSSID)
        if not verifyAPQuery(bssid):
            raise web.seeother('/fail/sendAPQuery')
        else:
            raise web.seeother('/success/sendAPQuery')

def verifyAPQuery(bssid):
    return False

class SendRTTValue:
    rtt_form = web.form.Form(
        web.form.Textbox('BSSID',web.form.notnull,size=17),
        web.form.Textarea('Value',web.form.notnull,rows=10,cols=80,description='RTTValueList'),
        web.form.Button('Submit'),
    )
    def GET(self):
        if session.logged_in == True:
            form = self.rtt_form()
            return render.rttValue(form)
        else:
            raise web.seeother('/login')
    def POST(self):
        i = web.input()
        bssid = web.net.websafe(i.BSSID)
        rttValue = i.Value
        if not verifyRTTValue(bssid, rttValue):
            raise web.seeother('/fail/sendRTTValue')
        else:
            raise web.seeother('/success/sendRTTValue')

def verifyRTTValue(bssid, rttValue):
    return False
    
class UpdateAuthorizedAPList:
    update_form = web.form.Form(
        web.form.Textbox('BSSID',web.form.notnull,size=17),
        web.form.Textbox('SSID',web.form.notnull,size=30),
        web.form.Textbox('Channel',web.form.notnull,size=2),
        web.form.Textbox('Vendor',web.form.notnull,size=20),
        web.form.Textbox('Location',web.form.notnull,size=30),
        web.form.Textbox('Route',web.form.notnull,size=30),
        web.form.Button('Update'),
    )
    def GET(self):
        if session.logged_in == True:
            form = self.update_form()
            return render.apUpdate(form)
        else:
            raise web.seeother('/login')
    def POST(self):
        i = web.input()
        bssid,ssid,channel,vendor,location,route = web.net.websafe(i.BSSID),web.net.websafe(i.SSID),\
        web.net.websafe(i.Channel),web.net.websafe(i.Vendor),web.net.websafe(i.Location),web.net.websafe(i.Route)
        authorizedAPDict = {'BSSID':bssid, 'SSID':ssid, 'CHANNEL':channel, 'VENDOR':vendor, 'LOCATION':location, 'ROUTE':route}
        if not verifyAuthorizedAP(authorizedAPDict):
            raise web.seeother('/fail/updateAuthorizedAPList')
        else:
            raise web.seeother('/success/updateAuthorizedAPList')

def verifyAuthorizedFeatures(authorizedAPDict):
    return False

# We haven't work out the following functions
# The following function are the core of the detection system, where we compute route, location, rtt evaluation and credit
'''
def computeLocation(APPosition,neighborAPs):
def computeRoute(routeInfo):
def computeRTTEval(RTTProbe, RTTDns):
def computeCredit(location,route,useAccess):
'''

def notfound():
    return web.notfound("Sorry, the page your were looking for was not found.")
    
app.notfound = notfound

# running our server
if __name__ == '__main__':
    app.run()
