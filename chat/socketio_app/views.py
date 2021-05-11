from django.shortcuts import render
from django.http import HttpResponse
import socketio
sio = socketio.Server(cors_allowed_origins='*')
# Create your views here.

rooms = {}
ROOM = 'room'

@sio.event
def connect(sid, environ):
    print('Connected', sid)
    sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)


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
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    sio.emit('data', data, room=ROOM, skip_sid=sid)

@sio.event
def offer(sid,payload):
    # print('Message from {}: {}'.format(sid, data))
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