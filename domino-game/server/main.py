import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game_logic import create_game, apply_move

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
asgi_app = socketio.ASGIApp(sio, other_asgi_app=app)

games = {}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def createGame(sid):
    game_id = sid
    games[game_id] = create_game()
    await sio.enter_room(sid, game_id)
    await sio.emit('gameCreated', game_id, room=sid)

@sio.event
async def joinGame(sid, game_id):
    if game_id in games and len(sio.rooms(sid)) < 2:
        await sio.enter_room(sid, game_id)
        await sio.emit('startGame', games[game_id], room=game_id)
    else:
        await sio.emit('error', 'Game full or not found.', room=sid)

@sio.event
async def playTile(sid, data):
    game_id = data['gameId']
    tile = data['move']['tile']
    player_index = data['move']['playerIndex']

    game = games.get(game_id)
    if not game:
        return

    success = apply_move(game, player_index, tile)
    if success:
        await sio.emit('tilePlayed', game, room=game_id)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
