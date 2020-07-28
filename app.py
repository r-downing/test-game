from typing import List, Optional

from connect4 import Connect4

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel

app = FastAPI()
game = Connect4()

app.mount("/static/", StaticFiles(directory="static"), name="static")


@app.get('/')
def homepage():
    return RedirectResponse('/static/index.html')


class GameState(BaseModel):
    grid: List[List[int]]
    current_player: int
    winner: Optional[int]


@app.get('/state', response_model=GameState)
async def get_state():
    return {'grid': game.grid, 'current_player': game.current_player(), 'winner': game.winner}


@app.get('/new_game', response_model=bool)
async def new_game():
    global game
    game = Connect4()
    return True


@app.get('/place', response_model=bool)
async def put_piece(player: int, col: int):
    return game.place(player, col)


if __name__ == "__main__":
    uvicorn.run(app)

