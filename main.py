from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

#You haven't configured your environment variables ANDROID_HOME or ANDROID_SDK_HOME correctly in your system. Please refer this to: https://stackoverflow.com/questions/23042638/how-do-i-set-android-sdk-home-environment-variable


# Initiate player pieces
WHITE = [1,0.2,0.2,1] # 'white.png'
BLACK = [0.2,0.2,1,1] #'black.png'
EMPTY = [1,1,1,1]

class Notify(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GameControls:
    def __init__(self, lst,**kwargs):
        super().__init__(**kwargs)
        # Reversing cell order to match values to position
        self.game_board = [
            [lst[8],lst[7],lst[6]],
            [lst[5],lst[4],lst[3]],
            [lst[2],lst[1],lst[0]],   
        ]
    
    def get_board_pos(self,ind):
        # Convet 1D list 2D list 
        row = ind // 3
        col = ind % 3
        return [row,col]

    def get_neighbour(self,val):
        # Get grid index of cell of given val
        row,col = self.get_board_pos(val)
        neighbours = []
        
        # To check for neighbouring cells, add or subtract 1 to row,col
        for i,j in [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,1),(1,-1)]:
            new_row = row+i
            new_col = col+j

            # Exception to avoid being added as neighbours
            # Cells in middle adjacent sides are avoided from being neighbours
            if ((row,col) == (2,1) and (new_row,new_col) == (1,0)) or ((row,col) == (1,0) and (new_row,new_col) == (2,1)):
                continue
            elif ((row,col) == (1,2) and (new_row,new_col) == (0,1)) or ((row,col) == (0,1) and (new_row,new_col) == (1,2)):
                continue
            elif ((row,col) == (1,0) and (new_row,new_col) == (0,1)) or ((row,col) == (0,1) and (new_row,new_col) == (1,0)):
                continue
            elif ((row,col) == (1,2) and (new_row,new_col) == (2,1)) or ((row,col) == (2,1) and (new_row,new_col) == (1,2)):
                continue
            elif 0<=new_row<=2 and 0<=new_col<=2:
                neighbours.append([new_row,new_col])

        return neighbours

class Board(BoxLayout):
    def __init__(self, **kwargs):
        """
            Initiate values such as selected cell, target cell, player turn, neighbours of selected and game board
            Also create an instance for GameControls for calculating neighbours and board state
        """
        super().__init__(**kwargs)
        self.next = None
        self.winner = ''
        self.current = 0,0,0,0
        self.turn = WHITE
        self.neighbour = []
        self.selected = None
        self.grid = self.ids.grid.children
        self.reset_board()
        self.game = GameControls(self.grid)
    

    def check_winner(self,button):
        """
            Check for winners
            A Player is declared winner if their pieces satisfies one of 3 conditions-
                Condition 1:
                    If any row, excluding the initial state, is occupied by a player
                Condition 2:
                    If any of columns are occupied by a player
                Condition 3:
                    If any of the diagonals are occupied by a player
            
                    If a win condition is satisfied return True, else False
        """
        # check rows
        for i in range(3):
            if all( [x.src == WHITE for x in self.game.game_board[i]] ) and i<2:
                self.winner = 'white'
                return True
            elif all( [x.src == BLACK for x in self.game.game_board[i]] ) and i>0:
                self.winner = 'black'
                return True

        #check columns
        for col in range(3):
            if all( [self.game.game_board[row][col].src==WHITE for row in range(3)] ):
                self.winner = 'white'
                return True 
            elif all( [self.game.game_board[row][col].src==BLACK for row in range(3)] ):
                self.winner = 'black'
                return True
        
        # check diagonals
        if all( [self.game.game_board[i][i].src==WHITE for i in range(3)] ) or all( [self.game.game_board[i][2-i].src==WHITE for i in range(3)] ):
            self.winner = 'white'
            return True
        elif all( [self.game.game_board[i][i].src==BLACK for i in range(3)] ) or all( [self.game.game_board[i][2-i].src==BLACK for i in range(3)] ):
            self.winner = 'black'
            return True
        
        return False

    def click(self,button):
        """
            Action to perform on clicking pieces
            If  piece is clicked without any prior piece of ame player, it is stored in 'selected', the next empty slot clickd is set as target/next, provided is an immediate neighbour
            On click being registered as selection, said slot is replaced as blank and player piece is moved the next/target
        """
        if not self.selected:
            if self.turn == button.src:
                self.selected = button
                self.current = button.src
                button.src = EMPTY
                self.neighbour = self.game.get_neighbour(self.selected.val)
        elif not self.next:
            self.next = button
            if self.game.get_board_pos(self.next.val) in self.neighbour and self.next.src == EMPTY:#'blank.png':
                self.next.src = self.current
                self.selected = self.next = None
                self.turn = WHITE if self.turn == BLACK else BLACK
            else:
                self.selected.src = self.current
                self.selected = self.next = None

            self.selected = self.next = None
            if self.check_winner(button):
                game_msg = Notify()
                game_msg.open()
    

    def reset_board(self):
        """
            The board is reset with black pieces at top and white at bottom
        """
        for btn in self.grid:
            
            self.winner = ''
            # if btn.val in (0,4,7):
            #     btn.src = WHITE
            if btn.val in (0,1,2):
                btn.src = BLACK
            elif btn.val in (6,7,8):
                btn.src = WHITE
            else:
                btn.src = EMPTY
        self.turn = WHITE

        
class GameApp(App):
    def build(self):
        """
            Initiate board, set width and height as specified and set board to center of screen
        """
        board = Board()
        self.name:'board'
        board.size_hint = None,None
        self.height = min(Window.size)
        self.width = self.height

        board.height = self.height/1.1
        board.width = self.height/1.3
        board.pos_hint = {'center_x':0.5,'center_y':0.5}

        return board
    # Window.bind(on_resize=self.on_window_resized)
    # def on_window_resized(self, window, width, height):
    #     print("Window resized to:", width, height)


if __name__ == '__main__':
    GameApp().run()