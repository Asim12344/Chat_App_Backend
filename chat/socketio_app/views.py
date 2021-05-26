import socketio
import socketio_app.config as config
import requests
sio = socketio.Server(cors_allowed_origins='*')
from requests.auth import AuthBase
import json
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT



 
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

# Create your views here.

rooms = {}
users = []
ROOM = 'room'

@sio.event
def connect(sid, environ):
    print('Connected', sid)
    sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)

@sio.event
def connected(sid, payload):
    print("connected")
    print(payload['token'])
    token = 'Bearer ' + payload['token']
    try:
        response = requests.post(config._Auth_URL, auth=TokenAuth(token)).json()
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
            sio.emit('token', "correct" , room=sid)
        else:
            print('Not Authenticated else')
            sio.emit('token', "correct" , room=sid)
    except:
        print('Not Authentication except')
    
@sio.event
def join_room(sid, roomID):
    print("roomID")
    print(roomID)
    print(type(roomID))
    print("rooms")
    print(rooms)
    # print(rooms.)
    if rooms:
        rooms[roomID].append(sid)
    else:
        rooms[roomID] = [sid]
    
    print(rooms)
    otherUser = None
    # rooms[roomID].find(id => id !== socket.id)
    for r in rooms[roomID]:
        if r != sid:
            otherUser = r
    print(otherUser)
    if otherUser:
        sio.emit('other_user', otherUser , room=sid)
        sio.emit('user_joined', sid , room=otherUser)


@sio.event
def join_room2(sid,email):
    global users
    print("join_room2")
    print(email)
    if len(users) < 2:
        obj = {}
        obj = {"sid":sid, "email":email,"partner_sid":""}
        users.append(obj)
        print(users)
        sio.emit('online_users', users)

    else:
        print("else")
        obj = {}
        obj = {"sid":sid, "email":email,"partner_sid":""}
        users.append(obj)
        print(users)
        sio.emit('third_user' , room=sid)

@sio.event
def create_connection(sid,payload):
    print("create_connection")
    print(payload)
    i=0
    global users
    for user in users:
        if user['sid'] == payload[1]['sid']:
            users[i]["partner_sid"]=payload[1]['target']
        if user['sid'] == payload[0]['sid']:
            users[i]["partner_sid"]=payload[0]['target']
        i=i+1
    
    print(users)
        
    sio.emit('other_user', payload[1] , room=payload[0]['sid'])
    sio.emit('user_joined', payload[0] , room=payload[1]['sid'])

@sio.event
def join_room1(sid):
    print("join_room1")
    if len(users) == 0:
        users.append(sid)
        print(users)
        sio.emit('no_user', users , room=sid)
    elif len(users) == 1:
        users.append(sid)
        print(users)
        sio.emit('other_user', users[0] , room=sid)
        sio.emit('user_joined', sid , room=users[0])
    else:
        users.append(sid)
        print("else")
        sio.emit('third_user' , room=sid)

@sio.event
def disconnect(sid):
    print(sid)
    print(type(sid))
    global users
    print(users)
    i = 0
    for user in users:
        if user['sid'] == sid:
            break
        i=i+1
    print(i)
    if len(users) > 0:
        temp = users[i]
        print("temp = " , temp)
        users.pop(i)
        print(users)
        sio.emit('disconnect', sid)
        sio.emit('partner', room=temp['partner_sid'])
   
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)
    

@sio.event
def offer(sid,payload):
    print('Message from {}: {}'.format(sid, payload))
    cache.set('sdp',payload,timeout=CACHE_TTL)

    test = cache.get('sdp')
    print("test")
    print(test)
    print("offer")
    print(payload)
    sio.emit('offer', payload , room=payload['target'])


@sio.event
def answer(sid,payload):
    print("answer")
    print(payload)
    # print('Message from {}: {}'.format(sid, data))
    sio.emit('answer', payload, room=payload['target'])

@sio.event
def ice_candidate(sid,payload):
    # print('Message from {}: {}'.format(sid, data))
    print("ice_candidate")
    print(payload)
    sio.emit('ice_candidate', payload['candidate'], room=payload['target'])