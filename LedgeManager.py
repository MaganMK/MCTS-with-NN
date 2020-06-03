from GameManager import GameManager

class LedgeManager(GameManager):
    
    def __init__(self, board, P):
        super().__init__(P)
        self.board = board
    
    def initial_state(self):
        super().initial_state()
        return {"board": self.board, "current player": self.current_player}
        
    def is_finished(self, game_state):
        return 2 not in game_state["board"]
    
    def get_all_next_states(self, game_state):
        if (self.is_finished(game_state)):
            return None
        
        res = []
        next_player = self.alternate_player(game_state["current player"])
        board = game_state["board"]
        index = 0
        last_zero = None
        for piece in board:
            new_board = board.copy()
            if(piece == 0 and last_zero == None):
                last_zero = index
            elif (index == 0):
                new_board[index] = 0
                res.append({"board": new_board, "current player": next_player})
            elif(last_zero != None and piece != 0):
                for i in range(last_zero, index):
                    new_board[i] = piece
                    new_board[index] = 0
                    res.append({"board": new_board, "current player": next_player})
                    new_board = board.copy()
                last_zero = None
            
            index += 1
        return res
    
    def get_winner(self, game_state):
        return self.alternate_player(game_state["current player"])
    
    def get_move_as_string(self, old_game_state, new_game_state):
        translation = {1: "copper", 2: "gold"}
        
        player = old_game_state["current player"]
        old_board = old_game_state["board"]
        new_board = new_game_state["board"]
        
        if (old_board[0] != new_board[0] and new_board[0] == 0):
            return f"P{player} picked up {translation[old_board[0]]}:\t\t {new_board}"
        
        from_index = None
        to_index = None
        for i in range(len(old_board)):
            if(old_board[i] != new_board[i] and to_index == None):
                to_index = i
            elif(old_board[i] != new_board[i]):
                from_index = i
                return f"P{player} moved {translation[old_board[i]]} from {from_index} to {to_index}:\t {new_board}"
        
        return f"ERROR"
    
    def get_start_position_as_string(self):
        return f"Board:\t\t\t\t {self.board}"
        
        
        
        
        
        
        
        
        