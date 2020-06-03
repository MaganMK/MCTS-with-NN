from math import sqrt, log

class Node:
    
    def __init__(self, game_state, parent):
        self.game_state = game_state
        self.parent = parent
        self.children = {}
        self.evaluation = 0
        self.visited = 0
    
    def __str__(self):
        return f"Game state: {self.game_state}, visted: {self.visited}"
    
    def __repr__(self):
        return f"Game state: {self.game_state}, visted: {self.visited}"
        
    def is_leaf(self):
        return len(self.children) == 0
    
    def add_child(self, node):
        self.children[node] = {"q(s, a)": 0, "n(s, a)": 0}
    
    def best_traverse(self):
        player = self.game_state["current player"]
        best_node = None
        best_value = -10000
    
        for current_node, current_edge in self.children.items():
            if(player == 2):
                q = -current_edge["q(s, a)"]/current_edge["n(s, a)"] if not current_edge["n(s, a)"] == 0 else 0
            else:
                q = current_edge["q(s, a)"]/current_edge["n(s, a)"] if not current_edge["n(s, a)"] == 0 else 0
                
            u = sqrt(log(self.visited)/current_edge["n(s, a)"]) if not current_edge["n(s, a)"] == 0 else 0
            current_value = q + u
             
            if current_value > best_value:
                best_node = current_node
                best_value = current_value
        
        
        return best_node
    
    def most_visited_child(self):
        visited_count = -1
        child = None
        
        for current_child, current_edge in self.children.items():
            if(current_edge["n(s, a)"] > visited_count):
                child = current_child
                visited_count = current_edge["n(s, a)"]
        
        return child
    
    def set_as_root(self):
        self.parent = None
        