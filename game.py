#!/usr/bin/env python


# Node class
class Node:
    def __init__(self, _data, _parent):
        self.data = _data
        self.parent = _parent
        self.children = []

    def __eq__(self, other):
        return self.data == other.data


# Game Board class
class GameBoard:
    def __init__(self, _layout, _width):
        self.layout = _layout # should be in the list form [0,1,2,3,4,5,6,7,8]
        self.width = _width # should be a number such as 3, for a 3x3 square
        self.index = self.layout.index("0")

    def can_move_up(self):
        if self.index >= self.width:
            return True
        else:
            return False

    def can_move_down(self):
        if self.index < self.width * (self.width - 1):
            return True
        else:
            return False

    def can_move_left(self):
        if self.index % self.width > 0:
            return True
        else:
            return False

    def can_move_right(self):
        if ((self.index + 1) % self.width) > 0:
            return True
        else:
            return False

    def move_up(self):
        new_layout_list = list(self.layout)
        new_layout_list[self.index] = new_layout_list[self.index - self.width]
        new_layout_list[self.index - self.width] = "0"

        return GameBoard("".join(new_layout_list), self.width)

    def move_down(self):
        new_layout_list = list(self.layout)
        new_layout_list[self.index] = new_layout_list[self.index + self.width]
        new_layout_list[self.index + self.width] = "0"

        return GameBoard("".join(new_layout_list), self.width)

    def move_left(self):
        new_layout_list = list(self.layout)
        new_layout_list[self.index] = new_layout_list[self.index - 1]
        new_layout_list[self.index - 1] = "0"

        return GameBoard("".join(new_layout_list), self.width)

    def move_right(self):
        new_layout_list = list(self.layout)
        new_layout_list[self.index] = new_layout_list[self.index + 1]
        new_layout_list[self.index + 1] = "0"

        return GameBoard("".join(new_layout_list), self.width)
    
    def is_goal(self):
        is_goal_flag = True
        
        for x in range(0, self.width * self.width):
            if self.layout[x] != str(x):
                is_goal_flag = False
        
        return is_goal_flag

    def print_layout(self):
        for x in range(0, self.width * self.width):
            print self.layout[x],
            if (x + 1) % self.width == 0:
                print "\n",
         
        print "\n",
    
    def __eq__(self, other):
        return self.layout == other.layout
        



def bfs(initial_node):
    # Check if initial state is the goal state
        # Return a solution found
    if initial_node.data.is_goal():
        return []

    frontier = [] # queue 
    explored = []
    
    # push the initial state onto the frontier
    frontier.append(initial_node)

    # Run while the froniter is not empty
    while len(frontier) > 0:
        # remove the next item off the frontier
        node = frontier.pop(0)

        # Add it onto the explored set
        explored.append(node)
    
        # populate the children nodes
        if node.data.can_move_up():
            node.children.append(Node(node.data.move_up(), node))

        if node.data.can_move_down():
            node.children.append(Node(node.data.move_down(), node))
        
        if node.data.can_move_left():
            node.children.append(Node(node.data.move_left(), node))
        
        if node.data.can_move_right():
            node.children.append(Node(node.data.move_right(), node))
        
        # For each child of this node
        for child in node.children:
            # If they are not already in either the explored or frontier sets
            if child not in explored and child not in frontier:
                # Test for the goal state
                if child.data.is_goal():
                    return child

                # Push the child node onto the frontier
                frontier.append(child)


    # Return no solution found
    return []



def print_solution(node):
    if node.parent is not None:
        print_solution(node.parent)
    node.data.print_layout()



def main():
    '''
    0 1 2
    3 4 5
    6 7 8

    3 1 2
    6 4 5
    0 7 8
    '''
    # Game Settings
    #initial_layout = "312045678" # 1 move
    #initial_layout = "312645078" # 2 moves
    initial_layout = "312645708" # 3 moves
    board_width = 3

    # Run the breadth first search algorithm
    goal_node = bfs(Node(GameBoard(initial_layout, board_width), None))
    

    print_solution(goal_node)



if __name__ == "__main__":
    main()
