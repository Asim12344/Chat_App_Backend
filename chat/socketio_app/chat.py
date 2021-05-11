from aiohttp import web
import socketio
# import eventlet
# import eventlet.wsgi

ROOM = 'room'

sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
# sio = socketio.Server(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
# application = socketio.WSGIApp(sio)


rooms = {}

sio.event
async def connect(sid, environ):
    print('Connected', sid)
    await sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)


@sio.event
async def join_room(sid, roomID):
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
        await sio.emit('other_user', otherUser , room=sid)
        await sio.emit('user_joined', sid , room=otherUser)


@sio.event
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
async def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    await sio.emit('data', data, room=ROOM, skip_sid=sid)

@sio.event
async def offer(sid,payload):
    # print('Message from {}: {}'.format(sid, data))
    print("offer")
    print(payload)
    await sio.emit('offer', payload , room=payload['target'])

@sio.event
async def answer(sid,payload):
    print("answer")
    print(payload)
    # print('Message from {}: {}'.format(sid, data))
    await sio.emit('answer', payload, room=payload['target'])

@sio.event
async def ice_candidate(sid,payload):
    # print('Message from {}: {}'.format(sid, data))
    print("ice_candidate")
    print(payload)
    await sio.emit('ice_candidate', payload['candidate'], room=payload['target'])
    
if __name__ == '__main__':
    web.run_app(app, port=8000)
    # eventlet.wsgi.server(eventlet.listen(('', 8000)), application)