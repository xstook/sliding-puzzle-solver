#!/usr/bin/env python

import time
from math import sqrt

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
        self.layout = _layout # should be in the form "0,1,2,3,4,5,6,7,8"
        self.width = _width # should be a number such as 3, for a 3x3 square 
        self.index = self.layout.split(",").index("0")

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
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index - self.width]
        new_layout_list[self.index - self.width] = "0"

        return GameBoard(",".join(new_layout_list), self.width)

    def move_down(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index + self.width]
        new_layout_list[self.index + self.width] = "0"

        return GameBoard(",".join(new_layout_list), self.width)

    def move_left(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index - 1]
        new_layout_list[self.index - 1] = "0"

        return GameBoard(",".join(new_layout_list), self.width)

    def move_right(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index + 1]
        new_layout_list[self.index + 1] = "0"

        return GameBoard(",".join(new_layout_list), self.width)
    
    def is_goal(self):
        is_goal_flag = True
        
        for x in range(0, self.width * self.width):
            if self.layout.split(",")[x] != str(x):
                is_goal_flag = False
        
        return is_goal_flag

    def print_layout(self):
        print "--------" * self.width
        for x in range(0, self.width * self.width):
            print self.layout.split(",")[x] + "\t",
            if (x + 1) % self.width == 0:
                print "\n\n",
        
        print "--------" * self.width
        print "\n\n",
    
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



def print_solution(node, number_of_moves):
    if node.parent is not None:
        print_solution(node.parent, number_of_moves + 1)
    else:
        print("Solution found in " + str(number_of_moves) + " moves")

    node.data.print_layout()



def main():
    '''
    0 1 2
    3 4 5
    6 7 8

    3 1 2
    6 4 5
    0 7 8

    0  1  2  3
    4  5  6  7
    8  9  10 11
    12 13 14 15
    '''
    # Game Settings
    #initial_layout = "312045678" # 1 move
    #initial_layout = "312645078" # 2 moves
    initial_layout = "3,1,2,6,4,5,7,0,8" # 3 moves
    #initial_layout = "4,1,2,3,0,5,6,7,8,9,10,11,12,13,14,15"
    #initial_layout = "11,15,9,3,14,8,12,7,6,10,0,2,13,4,5,1"
    board_width = int(sqrt(len(initial_layout.split(","))))
    
    # Start the timer
    start_time = time.time()

    # Run the breadth first search algorithm
    goal_node = bfs(Node(GameBoard(initial_layout, board_width), None))
    
    # End the timer
    time_elapsed = time.time() - start_time
    print("Time Taken:")
    print(time_elapsed)

    print_solution(goal_node, 0)



if __name__ == "__main__":
    main()
