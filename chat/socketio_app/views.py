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
from _thread import *



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
ThreadCount = 0

s.bind(('', port))         
print ("socket binded to %s" %(port)) 
s.listen()     
list_of_clients = [] 
rooms=[]

def tokenValidation(sid,payload,conn):
    print("connected: " , sid)
    print("email: ", payload['email'])
    print("token: ", payload['token'])
    print("gameKey: ", payload['gameKey'])
    token = payload['token']
    email = payload['email']
    gameKey = payload['gameKey']
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
                "socketId":sid,
                "gameKey": gameKey
            }
            response1 = requests.post("https://devplay.gamergraph.io/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            print(response1.json())
            # list_of_clients.append({sid:conn})
            list_of_clients.append({"sid": sid ,"email":email, "partner_sid":"","token":token,"conn":conn})
            print("list_of_clients: " , list_of_clients)
            # obj = {"sid":sid, "email":email,"partner_sid":"","token":token}
            # cache.add(sid,obj,timeout=CACHE_TTL)
            # print("=========== Redis Data ===================")
            # print(cache.get(sid))
            # print("============End Redis Data ==================")
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
        return caller_sid,target_sid
    except:
        return False

def getToken(sid):
    try:
        print(sid)
        token=""
        partner_sid = ""
        for client in list_of_clients:
            print("client: " , client)
            print("client sid: " ,client['sid'])
            if client['sid'] == sid:
                token = client['token']
                partner_sid = client['partner_sid']
        return token,partner_sid
    except Exception as e:
        print("error : " ,e)
        return ""

# def disconnect(sid):
#     try:
#         print(sid)
#         try:
#             token = ""
#             partner_sid = ""
#             print("=========== Redis Data ===================")
#             print("============== cache.get(sid) ======== " ,cache.get(sid))
#             print("============End Redis Data ==================")
#             removed_record = cache.get(sid)
#             print("removed_record: " , removed_record)
#             if removed_record != None:
#                 token = removed_record['token']
#                 partner_sid = removed_record['partner_sid']
#             print("removed_record token: " , token)
#             cache.delete(sid)
#             print("====== Deleted record ===========")
#         except Exception as e:
#             print("redis error : " , e)
        
#         payload1 = {
#             "availabilityStatus": "Offline",
#             "socketId":"",
#             "gameKey":""
#         }
#         try:
#             response1 = requests.post("https://devplay.gamergraph.io/chat/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
#             print("===========")
#             print(response1.json())
#             print("===========")
            
#             for room in rooms:
#                 payload2 = {
#                     "roomId":room['roomID']
#                 }
#                 response2 = requests.post("https://devplay.gamergraph.io/room/leave/", data=json.dumps(payload2), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
#                 print("===========")
#                 print(response2.json())
#                 print("===========")
            
#         except Exception as e:
#             print("API error: " ,e)
#             return ""

#         print('Disconnected', sid)
#         return partner_sid
#     except Exception as e:
#         print("error : " ,e)
#         return ""

def disconnect(sid):
    try:
        print(sid)
        try:
            token = ""
            partner_sid = ""
            token,partner_sid = getToken(sid)
            print("token: " , token)
            print("partner_sid: " , partner_sid)
        except Exception as e:
            print("error : " , e)
        
        payload1 = {
            "availabilityStatus": "Offline",
            "socketId":"",
            "gameKey":""
        }
        try:
            response1 = requests.post("https://devplay.gamergraph.io/player/availability/update/", data=json.dumps(payload1), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            print("===========")
            print(response1.json())
            print("===========")
            
            for room in rooms:
                payload2 = {
                    "roomId":room['roomID']
                }
                response2 = requests.post("https://devplay.gamergraph.io/room/leave/", data=json.dumps(payload2), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
                print("===========")
                print(response2.json())
                print("===========")
            
        except Exception as e:
            print("API error: " ,e)
            return ""

        print('Disconnected', sid)
        return partner_sid
    except Exception as e:
        print("error : " ,e)
        return ""



def threaded_client(conn):
    while True:
        data = conn.recv(1024)
        payload = json.loads(data)
        # ================== Token tokenValidation ==================
        if payload['action'] == "tokenValidation":
            print("==================== Start tokenValidation =========================")
            is_true = tokenValidation(payload['sid'],payload['payload'],conn)

            print(is_true)
            if is_true:
                msgfromserver = {"sid": payload['sid'] , "action": "tokenValidation" , "payload": {"token":"correct","partner_sid":"","partner_email":"","sdp":"","candidate":""}}
            else:
                msgfromserver = {"sid": payload['sid'] , "action": "tokenValidation" , "payload": {"token":"incorrect","partner_sid":"","partner_email":"","sdp":"","candidate":""}}

            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            conn.send(byt) 
            print("==================== End tokenValidation =========================")
        # ================== createConnection ==================
        if payload['action'] == 'createConnection':
            print("================== createConnection ==================" , list_of_clients)
            print(payload['payload']['caller'])
            print(payload['payload']['target'])
            target_conn = None
            caller_conn = None
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == payload['payload']['caller']['sid']:
                    caller_conn = client['conn']
                    client['partner_sid'] = payload['payload']['target']['sid']
                if client['sid'] == payload['payload']['target']['sid']:
                    target_conn = client['conn']
                    client['partner_sid'] = payload['payload']['caller']['sid']

            print("================== createConnection 1 ==================" , list_of_clients)
            print("caller_conn: " , caller_conn)
            print("target_conn: " , target_conn)

            # caller_id,target_id = createConnection(payload['sid'],payload['payload'])
            # print("caller_id: ", caller_id)
            # print("target_id: " , target_id)
            # target_conn = None
            # for item in list_of_clients:
            #     for key, value in item.items():
            #         if key == caller_id:
            #             caller_conn = value
            #         if key == target_id:
            #             target_conn = value
            
            # print("caller_conn: " , caller_conn)
            # print("target_conn: " , target_conn)

            # ======================== PAYLOAD ==========================
            msgfromserver = {"sid": payload['sid'] , "action": "other_user" , "payload": {"token":"" , "partner_sid":payload['payload']['target']['sid'],"partner_email":payload['payload']['target']['email'],"sdp":"","candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            caller_conn.send(byt) 
            print("===============")
            time.sleep(4)
            msgfromserver1 = {"sid": payload['payload']['target']['sid'] , "action": "user_joined" , "payload": {"token":"" , "partner_sid":payload['sid'], "partner_email":payload['payload']['caller']['email'],"sdp":"","candidate":""}}
            dataServer1 = json.dumps(msgfromserver1)
            print("dataServer1 = " , dataServer1)
            byt1=dataServer1.encode()
            target_conn.send(byt1) 
            print("================== End createConnection ==================")
        # ================== offer ==================
        if payload['action'] == 'offer':
            print("=================== Offer ==============")
            print(payload['payload']['target']['sid'])
            target_conn = None
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == payload['payload']['target']['sid']:
                    target_conn = client['conn']

            print("target_conn: " , target_conn)

            # for item in list_of_clients:
            #     for key, value in item.items():
            #         if key == payload['payload']['target']['sid']:
            #             target_conn = value

            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "offer" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":payload['payload']['sdp'],"candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            target_conn.send(byt) 
            print("=================== End Offer ==============")
        # ================== answer ==================
        if payload['action'] == 'answer':
            print("=================== Answer ==============")
            print(payload['payload']['target']['sid'])
            target_conn = None
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == payload['payload']['target']['sid']:
                    target_conn = client['conn']

            print("target_conn: " , target_conn)

            # for item in list_of_clients:
            #     for key, value in item.items():
            #         if key == payload['payload']['target']['sid']:
            #             target_conn = value

            # print("target_conn: " , target_conn)
            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "answer" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":payload['payload']['sdp'],"candidate":""}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            target_conn.send(byt) 
            print("=================== End Answer ==============")
        # ================== ice_candidate ==================
        if payload['action'] == 'ice_candidate':
            print("=================== ice_candidate ==============")
            print("target_sid: " , payload['payload']['target']['sid'])
            target_conn = None
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == payload['payload']['target']['sid']:
                    target_conn = client['conn']

            print("target_conn: " , target_conn)

            # for item in list_of_clients:
            #     for key, value in item.items():
            #         print("=== key , value ======" ,key, value)
            #         if key == payload['payload']['target']['sid']:
            #             target_conn = value

            # print("target_conn: " , target_conn)
            msgfromserver = {"sid": payload['payload']['target']['sid'] , "action": "ice_candidate" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":"" , "candidate":payload['payload']['candidate']}}
            dataServer = json.dumps(msgfromserver)
            print("dataServer = " , dataServer)
            byt=dataServer.encode()
            target_conn.send(byt) 
            print("=================== End ice_candidate ==============")
        # ================== disconnect ==================
        if payload['action'] == 'disconnect':
            print("========== Disconnect ==============")
            print(payload['sid'])
            print(payload['payload']['email'])
            sid = payload['sid']
            partner_sid = disconnect(sid)
            print("=== partner_sid ==== " ,partner_sid)
            target_conn = None
            caller_conn = None
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == partner_sid:
                    target_conn = client['conn']


            # for item in list_of_clients:
            #     for key, value in item.items():
            #         if key == partner_sid:
            #             target_conn = value
            #         if key == sid:
            #             caller_conn = value
            
            
            print("caller_conn: " , caller_conn)
            print("target_conn: " , target_conn)
            # Remove from list_of_clients
            for client in list_of_clients:
                print("client sid: " ,client['sid'])
                if client['sid'] == sid:
                    try:
                        list_of_clients.remove(client)
                    except:
                        print("Not in the list")
            # obj = {sid:caller_conn}
            # print("obj :" , obj)
            # try:
            #     list_of_clients.remove(obj)
            # except:
            #     print("Not in the list")
            
            
            for room in rooms:
                print(room)
                remove_obj = {"sid": payload['sid'] , "email":payload['payload']['email']}
                try:
                    room['members'].remove(remove_obj)
                except:
                    print("Not in the room")


            print("============== list_of_clients ===========" , list_of_clients)
            if target_conn:
                msgfromserver = {"sid": partner_sid , "action": "partner" , "payload": {"token":"" , "partner_sid":payload['sid'],"partner_email":"" , "sdp":"" , "candidate":""}}
                dataServer = json.dumps(msgfromserver)
                print("dataServer = " , dataServer)
                
                byt=dataServer.encode()
                target_conn.send(byt)
            print("========= End Disconnect ===========")
        
        if payload['action'] == 'createRoom':
            print("=============== createRoom ===================")
            print(payload['sid'])
            print(payload['payload']['email'])
            print(payload['payload']['members'])
            print(payload['payload']['roomID'])
            j = 0
            obj = {"roomID": payload['payload']['roomID'] , "members":[{"sid": payload['sid'] , "email":payload['payload']['email']}]}
            rooms.append(obj)
            print("rooms: " , rooms)
            while j < len(payload['payload']['members']):
                target_conn = None
                caller_conn = None
                for client in list_of_clients:
                    print("client: " ,client)
                    if client['sid'] == payload['payload']['members'][j]['sid']:
                        target_conn = client['conn']

                msgfromserver1 = {"sid": payload['payload']['members'][j]['sid'] , "action": "lobby_invitation" , "payload": {"token":"" , "partner_sid":payload['sid'], "partner_email":payload['payload']['email'],"sdp":"","candidate":"" , "roomID":payload['payload']['roomID']}}
                dataServer1 = json.dumps(msgfromserver1)
                print("dataServer1 = " , dataServer1)
                byt1=dataServer1.encode()
                target_conn.send(byt1) 
                j=j+1
                print("=============== End createRoom ===================")

        if payload['action'] == 'requestAccepted':
            print("=============== requestAccepted ===================")
            print(payload['sid'])
            print(payload['payload']['email'])
            print(payload['payload']['roomID'])
            print(payload['payload']['requestAccepted'])
            token,partner_sid = getToken(payload['sid'])
            print(token)
            print(partner_sid)
            if token:
                payload2 = {
                    "roomId":payload['payload']['roomID']
                }
                try:
                    response2 = requests.post("https://devplay.gamergraph.io/room/join/", data=json.dumps(payload2), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
                    print("===========")
                    print(response2.json())
                    print("===========")
                except Exception as e:
                    print("API error: " ,e)


            if payload['payload']['requestAccepted'] == True:
                for room in rooms:
                    print(room['roomID'])
                    if room['roomID'] == payload['payload']['roomID']:
                        room['members'].append({"sid": payload['sid'] , "email":payload['payload']['email']})
                print("rooms: " , rooms)
                caller_conn = None
                for client in list_of_clients:
                    print("client: " ,client)
                    if client['sid'] == payload['sid']:
                        caller_conn = client['conn']

                msgfromserver1 = {"sid": payload['sid'] , "action": "user_added" , "payload": {"token":"" , "partner_sid":"", "partner_email":"","sdp":"","candidate":""}}
                dataServer1 = json.dumps(msgfromserver1)
                print("dataServer1 = " , dataServer1)
                byt1=dataServer1.encode()
                caller_conn.send(byt1) 

        if payload['action'] == 'leaveRoom':
            print("=============== leaveRoom ===================")
            print(payload['sid'])
            print(payload['payload']['email'])
            print(payload['payload']['roomID'])
            token,partner_sid = getToken(payload['sid'])
            print(token)
            print(partner_sid)
            if token:
                payload2 = {
                    "roomId":payload['payload']['roomID']
                }
                try:
                    response2 = requests.post("https://devplay.gamergraph.io/room/leave/", data=json.dumps(payload2), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
                    print("===========")
                    print(response2.json())
                    print("===========")
                except Exception as e:
                    print("API error: " ,e)

            check = False
            for room in rooms:
                print(room['roomID'])
                if room['roomID'] == payload['payload']['roomID']:
                    obj = {"sid": payload['sid'] , "email":payload['payload']['email']}
                    try:
                        room['members'].remove(obj)
                        check = True
                    except:
                        print("Not in the room")
            print("rooms: " , rooms)
            if check == True:
                caller_conn = None
                for client in list_of_clients:
                    print("client: " ,client)
                    if client['sid'] == payload['sid']:
                        caller_conn = client['conn']
                
                msgfromserver1 = {"sid": payload['sid'] , "action": "user_removed" , "payload": {"token":"" , "partner_sid":"", "partner_email":"","sdp":"","candidate":""}}
                dataServer1 = json.dumps(msgfromserver1)
                print("dataServer1 = " , dataServer1)
                byt1=dataServer1.encode()
                caller_conn.send(byt1)

        if payload['action'] == 'communicateGameMove':
            print("=============== communicateGameMove ===================")
            print(payload['sid'])
            print(payload['payload']['email'])
            print(payload['payload']['roomID'])
            print(payload['payload']['message'])
            print("rooms: " , rooms)
            for room in rooms:
                if room['roomID'] == payload['payload']['roomID']:
                    for member in room['members']:
                        target_conn = None
                        caller_conn = None
                        for client in list_of_clients:
                            if client['sid'] == member['sid'] and member['sid'] != payload['sid']:
                                target_conn = client['conn']
                        if target_conn:
                            msgfromserver1 = {"sid": member['sid'] , "action": "player_move" , "payload": {"token":"" , "partner_sid":payload['sid'], "partner_email":payload['payload']['email'],"sdp":"","candidate":"" , "roomID":payload['payload']['roomID'] , "message": payload['payload']['message']}}
                            dataServer1 = json.dumps(msgfromserver1)
                            byt1=dataServer1.encode()
                            target_conn.send(byt1) 
            print("=============== End communicateGameMove ===================")            

while True: 
    conn, addr = s.accept()     

    print ('Got connection from', addr )

    start_new_thread(threaded_client, (conn, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

