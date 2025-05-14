import random

def create_game():
    tiles = [[i, j] for i in range(7) for j in range(i, 7)]
    random.shuffle(tiles)
    return {
        "players": [
            {"hand": tiles[:7]},
            {"hand": tiles[7:14]}
        ],
        "board": [],
        "currentPlayer": 0
    }

def is_playable(tile, board):
    if not board:
        return True
    left_end, right_end = board[0][0], board[-1][1]
    return tile[0] in [left_end, right_end] or tile[1] in [left_end, right_end]

def apply_move(game, player_index, tile):
    hand = game["players"][player_index]["hand"]
    if tile not in hand:
        return False

    board = game["board"]

    # Determine valid placement
    if not board:
        board.append(tile)
    else:
        left_end = board[0][0]
        right_end = board[-1][1]

        if tile[1] == left_end:
            board.insert(0, tile)
        elif tile[0] == left_end:
            board.insert(0, tile[::-1])
        elif tile[0] == right_end:
            board.append(tile)
        elif tile[1] == right_end:
            board.append(tile[::-1])
        else:
            return False

    hand.remove(tile)
    game["currentPlayer"] = 1 - player_index
    return True
