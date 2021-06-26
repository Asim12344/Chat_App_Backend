# import socketio
# import socketio_app.config as config
# import requests
# sio = socketio.Server(cors_allowed_origins='*')
# from requests.auth import AuthBase
# import json
# from django.core.cache import cache
# from django.conf import settings
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# import json


 
# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# class TokenAuth(AuthBase):
#     """Implements a custom authentication scheme."""

#     def __init__(self, token):
#         print("init")
#         self.token = token
 
#     def __call__(self, r):
#         print("call")
#         """Attach an API token to a custom auth header."""
#         r.headers['Authorization'] = f'{self.token}'  # Python 3.6+
#         print(r)
#         return r

# # Create your views here.

# rooms = {}
# users = []
# ROOM = 'room'

# # This event assigns a unique sid to user
# @sio.event
# def connect(sid, environ):
#     print('Connected', sid)
#     sio.enter_room(sid, ROOM)

# # This event takes token as a parameter and validate wheater a token is correct or not and also
# # changes availability status to online
# @sio.event
# def connected(sid, payload):
#     print("payload = " ,payload['token'])
#     token = 'Bearer ' + payload['token']
#     try:
#         response = requests.post(config._Auth_URL, auth=TokenAuth(token)).json()
#         print("response")
#         print(response)
#         response_Text  = json.dumps(response, sort_keys=True)
#         print("response_Text")
#         print(response_Text)
#         status = response_Text.find('token_not_valid')
#         print("status")
#         print(status)
#         if status == -1:
#             print('Authenticated')
#             payload1 = {
#                 "availabilityStatus": "Online",
#                 "socketId":sid
#             }
#             response1 = requests.post("https://devplay.gamergraph.io/chat/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + payload['token'], "Content-Type": "application/json"})
#             print(response1.json())
#             obj = {"sid":sid, "email":payload['email'],"partner_sid":"","token":payload['token']}
#             cache.add(sid,obj,timeout=CACHE_TTL)
#             print("==============================")
#             print(cache.get(sid))
#             sio.emit('token', "correct" , room=sid)
#         else:
#             print('Not Authenticated else')
#             sio.emit('token', "incorrect" , room=sid)
#     except:
#         print('Not Authentication except')
    
# # This event creates connection between two users and pass their sid's to their partners
# @sio.event
# def create_connection(sid,payload):
#     print("create_connection")
#     print(payload)
#     caller_sid = payload[0]['sid']
#     target_sid = payload[1]['sid']

#     get_caller_record = cache.get(caller_sid)
#     print("get_caller_record = " , get_caller_record)
#     get_caller_record['partner_sid'] = payload[1]['sid']
#     print("get_caller_record1 = " , get_caller_record)
#     cache.set(caller_sid,get_caller_record,timeout=CACHE_TTL)

#     get_target_record = cache.get(target_sid)
#     print("get_target_record = " , get_target_record)
#     get_target_record['partner_sid'] = payload[0]['sid']
#     print("get_target_record1 = " , get_target_record)
#     cache.set(target_sid,get_target_record,timeout=CACHE_TTL)

#     sio.emit('other_user', payload[1] , room=payload[0]['sid'])
#     sio.emit('user_joined', payload[0] , room=payload[1]['sid'])

# # LOBBY
# @sio.event
# def create_lobby(sid,payload):
#     print("create_lobby")
#     print(payload)
#     for socketId in payload:
#         sio.emit('lobby', payload , room=socketId)

# # This event changes availability status to offline and also remove entry from redis
# @sio.event
# def disconnect(sid):
#     print(sid)
#     print(type(sid))
#     removed_record = cache.get(sid)
#     print("======== disconnect ===========")
#     print(removed_record)
#     print(removed_record['token'])
#     cache.delete(sid)
#     payload1 = {
#         "availabilityStatus": "Offline",
#         "socketId":""
#     }
#     response1 = requests.post("https://devplay.gamergraph.io/chat/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + removed_record['token'], "Content-Type": "application/json"})
#     print("===========")
#     print(response1.json())
#     print("============")
#     sio.emit('partner', room=removed_record['partner_sid'])
#     sio.leave_room(sid, ROOM)
#     print('Disconnected', sid)
    
# # Offer event pass sid to his partner
# @sio.event
# def offer(sid,payload):
#     print('Message from {}: {}'.format(sid, payload))
#     print("offer")
#     print(payload)
#     sio.emit('offer', payload , room=payload['target'])

# # Answer event pass sid to his partner
# @sio.event
# def answer(sid,payload):
#     print("answer")
#     print(payload)
#     sio.emit('answer', payload, room=payload['target'])

# @sio.event
# def ice_candidate(sid,payload):
#     print("ice_candidate")
#     print(payload)
#     sio.emit('ice_candidate', payload['candidate'], room=payload['target'])


import socketio_app.config as config
import requests
from requests.auth import AuthBase
import json
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import socket
import json
import time


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        print("init")
        self.token = token
 
    def __call__(self, r):
        print("call")
        """Attach an API token to a custom auth header."""
        r.headers['Authorization'] = f'{self.token}'  # Python 3.6+
        print(r)
        return r

s = socket.socket()         
print ("Socket successfully created!")
port = 8080

s.bind(('', port))         
print ("socket binded to %s" %(port)) 
s.listen()     

def tokenValidation(sid,payload):
    print("connected: " , sid)
    print("email: ", payload['email'])
    print("token: ", payload['token'])
    token = payload['token']
    email = payload['email']
    try:
        # response = requests.post(config._Auth_URL, auth=TokenAuth(token)).json()
        response = requests.post(config._Auth_URL, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}).json()
        print("response")
        print(response)
        response_Text  = json.dumps(response, sort_keys=True)
        print("response_Text")
        print(response_Text)
        status = response_Text.find('token_not_valid')
        print("status")
        print(status)
        if status == -1:
            print('Authenticated')
            payload1 = {
                "availabilityStatus": "Online",
                "socketId":sid
            }
            response1 = requests.post("https://devplay.gamergraph.io/chat/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            print(response1.json())
            obj = {"sid":sid, "email":email,"partner_sid":"","token":token}
            cache.add(sid,obj,timeout=CACHE_TTL)
            print("==============================")
            print(cache.get(sid))
            return True
        else:
            print('Not Authenticated else')
            return False
    except:
        print('Not Authentication except')
        return False

def createConnection(sid,payload):
    print("create_connection")
    print(payload)
    try:
        caller_sid = payload['caller']['sid']
        target_sid = payload['target']['sid']
        print(caller_sid)
        print(target_sid)

        get_caller_record = cache.get(caller_sid)
        print("get_caller_record = " , get_caller_record)
        get_caller_record['partner_sid'] = target_sid
        print("get_caller_record1 = " , get_caller_record)
        cache.set(caller_sid,get_caller_record,timeout=CACHE_TTL)

        get_target_record = cache.get(target_sid)
        print("get_target_record = " , get_target_record)
        get_target_record['partner_sid'] = caller_sid
        print("get_target_record1 = " , get_target_record)
        cache.set(target_sid,get_target_record,timeout=CACHE_TTL)
        return True
    except:
        return False

def disconnect(sid):
    try:
        print(sid)
        print(type(sid))
        removed_record = cache.get(sid)
        print("======== disconnect ===========")
        print(removed_record)
        print(removed_record['token'])
        cache.delete(sid)
        payload1 = {
            "availabilityStatus": "Offline",
            "socketId":""
        }
        response1 = requests.post("https://devplay.gamergraph.io/chat/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + removed_record['token'], "Content-Type": "application/json"})
        print("===========")
        print(response1.json())
        print("============")

        print('Disconnected', sid)
        return removed_record['partner_sid']
    except:
        return ""

while True: 
    conn, addr = s.accept()     
    print ('Got connection from', addr )
    while True:
        data = conn.recv(1024)
        payload = json.loads(data)
        print("payload = " , payload)
        # ================== Token tokenValidation ==================
        if payload['action'] == "tokenValidation":
            is_true = tokenValidation(payload['sid'],payload['payload'])
            print(is_true)
            if is_true:
                msgfromserver = {"sid": payload['sid'] , "action": "tokenValidation" , "payload": {"token":"correct","partner_sid":"","partner_email":"","sdp":"","candidate":""}}
            else:
                msgfromserver = {"sid": payload['sid'] , "action": "tokenValidation" , "payload": {"token":"incorrect","partner_sid":"","partner_email":"","sdp":"","candidate":""}}

            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt) 
        # ================== createConnection ==================
        if payload['action'] == 'createConnection':
            is_true = createConnection(payload['sid'],payload['payload'])
            if is_true:
                # ======================== PAYLOAD ==========================
                msgfromserver = {"sid": payload['sid'] , "action": "other_user" , "payload": {"token":"" , "partner_sid":payload['payload']['target']['sid'],"partner_email":payload['payload']['target']['email'],"sdp":"","candidate":""}}
                dataServer = json.dumps(msgfromserver)
                print("dataServer = " , dataServer)
                byt=dataServer.encode()
                conn.send(byt) 
                print("===============")
                time.sleep(4)
                msgfromserver1 = {"sid": payload['payload']['target']['sid'] , "action": "user_joined" , "payload": {"token":"" , "partner_sid":payload['sid'], "partner_email":payload['payload']['caller']['email'],"sdp":"","candidate":""}}
                dataServer1 = json.dumps(msgfromserver1)
                print("dataServer1 = " , dataServer1)
                byt1=dataServer1.encode()
                conn.send(byt1) 
        # ================== offer ==================
        if payload['action'] == 'offer':
            print(payload['payload']['target']['sid'])
            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "offer" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":payload['payload']['sdp'],"candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt) 
        # ================== answer ==================
        if payload['action'] == 'answer':
            print(payload['payload']['target']['sid'])
            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "answer" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":payload['payload']['sdp'],"candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt) 
        # ================== ice_candidate ==================
        if payload['action'] == 'ice_candidate':
            print(payload['payload']['target']['sid'])
            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "ice_candidate" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":"" , "candidate":payload['payload']['candidate']}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt) 
        # ================== disconnect ==================
        if payload['action'] == 'disconnect':
            sid = payload['sid']
            print(sid)
            partner_sid = disconnect(sid)
            print(partner_sid)
            msgfromserver = {"sid": partner_sid , "action": "partner" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":"" , "candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt)
        # ==================== Lobby =======================
        if payload['action'] == 'lobby':
            print(payload['payload']['members'])
            i = 0
            while i < len(payload['payload']['members']):
                j = i + 1
                print(j)
                while j < len(payload['payload']['members']):
                    print("j = " , j)
                    msgfromserver = {"sid": payload['payload']['members'][i]['sid'] , "action": "other_user" , "payload": {"token":"" , "partner_sid":payload['payload']['members'][j]['sid'] ,"partner_email":payload['payload']['members'][j]['email'] ,"sdp":"","candidate":""}}
                    dataServer = json.dumps(msgfromserver)
                    print("dataServer = " , dataServer)
                    byt=dataServer.encode()
                    conn.send(byt) 
                    
                    time.sleep(4)
                    msgfromserver1 = {"sid": payload['payload']['members'][j]['sid'] , "action": "user_joined" , "payload": {"token":"" , "partner_sid":payload['payload']['members'][i]['sid'], "partner_email":payload['payload']['members'][i]['email'],"sdp":"","candidate":""}}
                    dataServer1 = json.dumps(msgfromserver1)
                    print("dataServer1 = " , dataServer1)
                    byt1=dataServer1.encode()
                    conn.send(byt1) 
                    print("===============")
                    j=j+1
                i=i+1
