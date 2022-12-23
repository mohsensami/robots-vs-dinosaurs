from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.items import GamePayload
from models.game import Game
from services.play import create_random_game, create_game

app = FastAPI()

# Caching the games by id
GAMES = {}

@app.get('/')
async def first_api():
    return {'title': 'Front'}


@app.post("/games/start")
def start_game(item: GamePayload) -> JSONResponse:
    """
    Start a game
    :param item: parameters to initialize a game instance
    :return: the game information
    """
    try:
        dim, robots, robots_count, dinosaurs, dinosaurs_count = item.grid_dim, item.robots, item.robots_count, item.dinosaurs, item.dinosaurs_count
        if dim <= 2:
            return JSONResponse(
                status_code=400,
                content={"status": False, "detail": "You must create a bigger grid"}
            )

        if robots and dinosaurs:
            match: Game = create_game(dim, robots=robots, dinosaurs=dinosaurs)
        else:
            match: Game = create_random_game(dim, robots_count=robots_count, dinosaurs_count=dinosaurs_count)

        GAMES[str(match.game_id)] = match

        res = {
            "game_id": str(match.game_id),
            "grid": f"{match.dim}*{match.dim}",
            "dinosaurs": len(match.dinosaurs_position),
            "dinosaurs_position": match.dinosaurs_position,
            "robots": len(match.robots_position),
            "robots_position": list(match.robots.values()),
        }

        return JSONResponse(status_code=200, content=res)

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )
