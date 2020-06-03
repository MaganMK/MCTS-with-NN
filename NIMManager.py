from GameManager import GameManager

class NIMManager(GameManager):
    
    def __init__(self, N, K, P):
        super().__init__(P)
        self.N = N
        self.K = K
        
    def initial_state(self):
        super().initial_state()
        return {"pile": self.N, "current player": self.current_player}
    
    def is_finished(self, game_state):
        return game_state["pile"] == 0
    
    def get_winner(self, game_state):
        return self.alternate_player(game_state["current player"])
        
    def get_all_next_states(self, game_state):
        if (self.is_finished(game_state)):
            return None
        
        res = []
        next_player = self.alternate_player(game_state["current player"])
        for i in range(1, self.K+1):
            new_pile = game_state["pile"] - i
            if (new_pile >= 0):
                res.append({"pile": new_pile, "current player": next_player})
        
        return res
    
    def get_move_as_string(self, old_game_state, new_game_state):
        player = old_game_state["current player"]
        removed_stones = old_game_state["pile"] - new_game_state["pile"]
        remaining_stones = new_game_state["pile"]
        return f"P{player} removed {removed_stones} stones. Remaining pile:\t {remaining_stones}"
    
    def get_start_position_as_string(self):
        return f"Start pile:\t\t\t\t {self.N}"
    