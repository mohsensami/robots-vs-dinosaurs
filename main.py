from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from models.items import GamePayload, RobotPayload
from models.game import Game
from services.play import create_random_game, create_game, move_robot
from services.utils import create_html, COMMANDS

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Caching the games by id
GAMES = {}

@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse("/docs")


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
        return JSONResponse(status_code=400, content={"status": False, "detail": str(e)})


@app.get("/games/{game_id}")
def display_game(game_id: str) -> HTMLResponse:
    """
    Display the game board in html
    :param game_id: a specified game id
    :return: html page
    """
    try:
        if game_id not in GAMES:
            return JSONResponse(status_code=404, content={"status": False, "detail": f"Game ID '{game_id}' does not exist"})
        game = GAMES[game_id]
        html = create_html(game_id, game.get_board(), game.dim)
        return HTMLResponse(content=html, status_code=200)

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": False, "detail": str(e)})


@app.put("/games/{game_id}")
async def play_robots(game_id: str, item: RobotPayload) -> JSONResponse:
    """
    Operate specified robot to move forward and backward, turn right and left, and attack
    :param game_id: a specified game id
    :param item: parameters to operate the robot
    :return: the state of current game
    0 -> forward, 1 -> backward, 2 -> right, 3 -> left, 4 -> attack"
    """
    try:
        if game_id not in GAMES:
            return JSONResponse(
                status_code=404,
                content={"status": False, "detail": f"Game ID '{game_id}' does not exist"}
            )

        game: Game = GAMES[game_id]
        robots_list = list(game.robots.keys())
        chose_robot = str(item.robot_id)
        if chose_robot not in robots_list:
            chose_robot = list(game.robots.keys())[0]
        
        if item.command not in range(5):
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "detail": "You must insert the correct instructions as following \
                    0 -> forward, 1 -> backward, 2 -> right, 3 -> left, 4 -> attack"
                }
            )

        command = COMMANDS[item.command]
        game = await move_robot(game, chose_robot, command)
        res = {
            "game_id": game_id,
            "robot_id": chose_robot,
            "command": command,
            "new_position": game.robots[chose_robot],
            "dinosaurs": len(game.dinosaurs_position),
            "dinosaurs_position": game.dinosaurs_position,
            "number_of_moves": game.get_number_of_moves(),
            "all_dinosaurs_has_been_terminated": not bool(game.dinosaurs_position),
        }
        return JSONResponse(status_code=200, content=res)

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": False, "detail": str(e)})


@app.delete("/games/{game_id}")
def remove_game(game_id: str) -> JSONResponse:
    """
    Remove a specified game instance in the cache
    :param game_id: a specified game id
    :return: the state of remove
    """
    try:
        if game_id not in GAMES:
            return JSONResponse(status_code=404, content={"status": False, "detail": f"Game ID '{game_id}' does not exist"})
        GAMES.pop(game_id)
        res = {
            "game_id": game_id,
            "is_deleted": game_id not in GAMES,
        }
        return JSONResponse(status_code=200, content=res)

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": False, "detail": str(e)})


@app.delete("/games")
def remove_games() -> JSONResponse:

    """ Remove all games instances in the cache """

    try:
        [GAMES.pop(game) for game in GAMES.copy()]
        return JSONResponse(status_code=204, content={})

    except Exception as e:
        return JSONResponse(status_code=400, content={"status": False, "detail": str(e)})


