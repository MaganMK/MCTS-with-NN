from GameManager import GameManager
from copy import deepcopy
import networkx as nx
from math import sqrt
import matplotlib.pyplot as plt

class HexManager(GameManager):
    
    def __init__(self, size, frame_rate, P):
        super().__init__(P)
        self.size = size
        self.frame_rate = frame_rate
        self.state = self.initial_state()    
    
    def initial_state(self):
        super().initial_state()
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        return {"board": self.board, "current player": self.current_player}
    
    
    def is_finished(self, game_state):
        board = game_state["board"]
        player = self.alternate_player(game_state["current player"])
        if(player == 1):
            return self.opposite_side_connection(board, True, 1)
        else:
            return self.opposite_side_connection(board, False, 2)        
    
    
    def opposite_side_connection(self, board, top_left_to_bottom_right, player):
        starting_nodes = []
        if (top_left_to_bottom_right):
            starting_nodes = [(row, 0) for row in range(self.size)]
        else:
            starting_nodes = [(0, col) for col in range(self.size)]
        
        for starting_node in starting_nodes:
            is_full_path = self.breath_first(board, starting_node, player)
            if(is_full_path):
                return True
                
        return False
    
    
    def is_valid_neighbour(self, board, row, col, player):
        if(row >= self.size or col >= self.size or row < 0 or col < 0):
            return False
        elif(board[row][col] != player):
            return False
        return True
        
        
    def get_neighbours(self, board, node, player):
        row, col = node
        moves = ((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (-1, 1))
        neighbours = []
        for move_row, move_col in moves:
            new_row = row + move_row
            new_col = col + move_col
            if(self.is_valid_neighbour(board, new_row, new_col, player)):
                neighbours.append((new_row, new_col))
        
        return neighbours
    
    
    def breath_first(self, board, starting_node, player):
        start_row, start_col = starting_node
        if(board[start_row][start_col] != player):
            return False
            
        neighbours = self.get_neighbours(board, starting_node, player)
        
        walked_path = []
        walked_path.append(starting_node)
        for neighbour in neighbours:
            if(neighbour in walked_path):
                continue
            else:
                row, col = neighbour
                if player == 1 and col == self.size - 1 or player == 2 and row == self.size - 1:
                    return True
                    
                new_neighbours = self.get_neighbours(board, neighbour, player)
                neighbours += new_neighbours
                walked_path.append(neighbour)
                

        return False

    
    def get_all_next_states(self, game_state):
        if (self.is_finished(game_state)):
            return None        
        board = game_state["board"]
        current_player = game_state["current player"]
        next_player = self.alternate_player(current_player)
        res = []
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    child_board= deepcopy(board)
                    child_board[row][col] = current_player
                    child = {"board": child_board, "current player": next_player}
                    res.append(child)
        return res
        
        
    def get_move_as_string(self, old_game_state, new_game_state):
        self.visualize_board(new_game_state["board"])
        return f"Board: {new_game_state}"
    
    def get_start_position_as_string(self):
        self.visualize_board(self.board)
        return f"Board: {self.board}"
    
    def visualize_board(self, board):
        
            graph = nx.Graph()
            node_colors = []
            edge_colors = []
            
            for row in range(self.size):
                for col in range(self.size):
                    id = self.get_id(row, col)
                    player = board[row][col]
                    position = (col - row) / 2, -(col + row) * sqrt(3) / 2

                    graph.add_node(id, pos=position)

                    if player == 0:
                        node_colors.append("white")
                    elif player == 1:
                        node_colors.append("green")
                    else:
                        node_colors.append("blue")

            for row in range(self.size):
                for col in range(self.size):
                    self.create_neighbourhood(graph, self.board, row, col)

            top_id = "0"
            bottom_id = str(self.size - 1)
            for n, m in graph.edges:
                n_row = n[0]
                n_col = n[1]
                m_row = m[0]
                m_col = m[1]

                if n_row == top_id and m_row is top_id or n_row == bottom_id and m_row == bottom_id:
                    edge_colors.append("blue")
                elif n_col == top_id and m_col == top_id or n_col == bottom_id and m_col == bottom_id:
                    edge_colors.append("green")
                else:
                    edge_colors.append("black")

            plt.clf()
            nx.draw(graph, nx.get_node_attributes(graph, 'pos'), node_color=node_colors, edge_color=edge_colors, with_labels=True)
            plt.draw()
            plt.pause(self.frame_rate)


    def create_neighbourhood(self, graph, board, row, col):
        id = self.get_id(row, col)
        colors = []

        if col + 1 < self.size:
            graph.add_edge(id, self.get_id(row, col + 1))
            colors.append("red")
            if row > 0:
                graph.add_edge(id, self.get_id(row - 1, col + 1))
                colors.append("red")
        if row + 1 < self.size:
            graph.add_edge(id, self.get_id(row + 1, col))
            colors.append("red")

        return colors
    
    def get_id(self, row, col):
        return f"{row}{col}"
        
        
        
        
        
        
        
        
        