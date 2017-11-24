#!/usr/bin/env python

import time
from math import sqrt
import argparse

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
    def __init__(self, _layout):
        self.layout = _layout # should be in the form "0,1,2,3,4,5,6,7,8"
        self.width = int(sqrt(len(self.layout.split(","))))
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

        return GameBoard(",".join(new_layout_list))

    def move_down(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index + self.width]
        new_layout_list[self.index + self.width] = "0"

        return GameBoard(",".join(new_layout_list))

    def move_left(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index - 1]
        new_layout_list[self.index - 1] = "0"

        return GameBoard(",".join(new_layout_list))

    def move_right(self):
        new_layout_list = self.layout.split(",")
        new_layout_list[self.index] = new_layout_list[self.index + 1]
        new_layout_list[self.index + 1] = "0"

        return GameBoard(",".join(new_layout_list))
    
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
    if initial_node.data.is_goal():
        return None

    # These are supposed to be queue's but I use a hashmap (dict) for speed
    frontier = dict() # key: layout string, value: node 
    frontier_list = []
    explored = dict()
    
    # push the initial state onto the frontier
    frontier[initial_node.data.layout] = initial_node
    frontier_list.append(initial_node)
    
    # Run while the froniter is not empty
    while len(frontier_list) > 0:
        # remove the next item off the frontier
        node = frontier_list.pop(0)
        del frontier[node.data.layout]

        # Add it onto the explored set
        explored[node.data.layout] = node

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
            if child.data.layout not in explored and child.data.layout not in frontier:
                # Test for the goal state
                if child.data.is_goal():
                    return child

                # Push the child node onto the frontier
                frontier[child.data.layout] = child
                frontier_list.append(child)


    # Return no solution found
    return None



def print_solution(node, number_of_moves):
    if node.parent is not None:
        print_solution(node.parent, number_of_moves + 1)
    else:
        print("Solution found in " + str(number_of_moves) + " moves")

    node.data.print_layout()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layout", help="The layout of the board as a list of comma separated values. Ex. 1,2,0,3")
    args = parser.parse_args()
    
    if args.layout is not None:
        initial_layout = args.layout
    else:
        #initial_layout = "312045678" # 1 move
        #initial_layout = "312645078" # 2 moves
        #initial_layout = "3,1,2,6,4,5,7,0,8" # 3 moves
        #initial_layout = "4,1,2,3,0,5,6,7,8,9,10,11,12,13,14,15"
        #initial_layout = "11,15,9,3,14,8,12,7,6,10,0,2,13,4,5,1"
        initial_layout = "1,7,0,2,6,4,3,8,5"

    
    # Start the timer
    start_time = time.time()

    # Run the breadth first search algorithm
    goal_node = bfs(Node(GameBoard(initial_layout), None))
    
    # End the timer
    time_elapsed = time.time() - start_time
    print("Time Taken: " + str(time_elapsed))

    print_solution(goal_node, 0)



if __name__ == "__main__":
    main()
