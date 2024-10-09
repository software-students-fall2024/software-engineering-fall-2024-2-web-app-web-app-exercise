
from src.app import get_db

class Board():
    def __init__(self, user, pedals: list[list], name) -> None:
        self.user = user
        self.pedals = pedals
        self.name = name


def get_boards_by_user(email:str):
    boards = get_db().boards
    return boards.find({"user":email})

def create_board(user:str, name:str):
    new_board = Board()
    new_board.user = user
    new_board.name = name
    boards = get_db().boards
    return boards.insert_one({"user": user, "name": name})

def update_board(user: str, name:str, board_state: list[list]):
    boards = get_db().boards
    return boards.update_one({})