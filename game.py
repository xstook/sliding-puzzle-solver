#!/usr/bin/env python

# Author: Michael Santoro
# Start Date: November 23, 2017

import time
from math import sqrt
import argparse
import random

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



def get_number_of_moves(node):
    if node.parent is not None:
        number_of_moves = get_number_of_moves(node.parent)
    else:
        return 0

    return number_of_moves + 1


all_permutations = []
def get_permutations(a, l, r):
    global all_permutations

    if l == r:
        #print "".join(a)
        all_permutations.append(",".join(a))
    else:
        for i in xrange(l, r + 1):
            a[l], a[i] = a[i], a[l]
            get_permutations(a, l + 1, r)
            a[l], a[i] = a[i], a[l]





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--layout", help="The layout of the board as a list of comma separated values. Ex. 1,2,0,3")
    parser.add_argument("--demo", help="Demo mode, outputs random board layouts and the number of moves it takes to solve them", action="store_true")
    parser.add_argument("--demo2", help="Demo mode, outputs all possible permutations of the board layout", action="store_true")
    parser.add_argument("-b", "--benchmark", help="Runs a benchmark and outputs the average time taken. This can be used to compare different CPUs", action="store_true")
    args = parser.parse_args()
    
    
    # 3x3 layout                          Moves
    initial_layout = "3,1,2,0,4,5,6,7,8" # 1
    #initial_layout = "3,1,2,6,4,5,0,7,8" # 2
    #initial_layout = "3,1,2,6,4,5,7,0,8" # 3
    #initial_layout = "3,1,5,2,7,4,0,6,8" # 10
    #initial_layout = "4,5,3,1,2,0,6,7,8" # 11
    #initial_layout = "0,7,4,1,8,2,3,6,5" # 12
    #initial_layout = "6,1,2,7,4,0,3,8,5" # 13
    #initial_layout = "1,5,0,6,2,7,8,3,4" # 14
    #initial_layout = "3,5,4,2,8,0,6,1,7" # 15
    #initial_layout = "7,3,1,6,8,2,0,4,5" # 16
    #initial_layout = "1,2,7,6,5,3,8,0,4" # 17
    #initial_layout = "3,2,1,6,0,8,5,7,4" # 18
    #initial_layout = "2,4,5,1,7,0,6,3,8" # 19
    #initial_layout = "0,5,7,1,6,4,8,2,3" # 20
    #initial_layout = "7,6,1,8,4,0,5,3,2" # 21
    #initial_layout = "5,7,2,3,8,6,1,4,0" # 22
    #initial_layout = "2,4,8,3,7,0,5,6,1" # 23
    #initial_layout = "6,5,7,8,2,4,0,1,3" # 24
    #initial_layout = "4,0,3,2,1,6,8,7,5" # 25
    #initial_layout = "2,3,0,7,8,4,5,1,6" # 26
    #initial_layout = "8,0,4,6,1,7,2,5,3" # 27
    #initial_layout = "1,8,0,4,7,6,2,5,3" # 28
    #initial_layout = "3,0,4,1,6,7,2,5,8" # 29
    #initial_layout = "2,7,1,5,4,3,8,6,0" # 30
    
    # 4x4 layout
    #initial_layout = "4,1,2,3,0,5,6,7,8,9,10,11,12,13,14,15"
    #initial_layout = "11,15,9,3,14,8,12,7,6,10,0,2,13,4,5,1"


    if args.layout is not None:
    	initial_layout = args.layout
    


    # Run demo mode
    if args.demo:
        final_layouts = dict() # key: number of moves, value: layout string
        checked_layouts = dict() # key: layout string, value: None

        # Run indefinitely
        while True:
            layout_choices = '012345678'
            #layout_choices = '0123'
            initial_layout = ""
            
            # Generate initial layout
            while len(layout_choices) > 0:
                chosen = random.choice(layout_choices)
                initial_layout = initial_layout + chosen + ','
                layout_choices = layout_choices.replace(chosen, '')
            
            initial_layout = initial_layout[:-1]

            if initial_layout not in checked_layouts:
                checked_layouts[initial_layout] = None

                # Search for a solution
                goal_node = bfs(Node(GameBoard(initial_layout), None))
   
                # If a solution is found
                if goal_node is not None:        
                    number_of_moves = get_number_of_moves(goal_node)

                    if number_of_moves not in final_layouts:
                        final_layouts[number_of_moves] = initial_layout
                        
                        final_layout_keys_sorted = final_layouts.keys()
                        final_layout_keys_sorted.sort()
                        output = str(len(final_layout_keys_sorted)) + " layouts found\n"
                        for key in final_layout_keys_sorted:
                            output = output + str(key) + " moves: " + final_layouts[key] + "\n"
                        print(output)
                        f = open("demo_output.txt", 'w')
                        f.write(output)
                        f.close()

    # Demo 2 mode
    elif args.demo2:
        # Find all permutations of the board layout
        layout_choices = "012345678"
        #layout_choices = "0123"
        n = len(layout_choices)
        a = list(layout_choices)
        get_permutations(a, 0, n - 1)
        all_permutations_count = len(all_permutations)
        #print len(all_permutations)

        f = open("demo2_output.txt", 'w')
        f.close()

        stats = dict()

        layout_count = 1
        for layout in all_permutations:
            goal_node = bfs(Node(GameBoard(layout), None))
            number_of_moves = 0

            # If a solution is found
            if goal_node is not None:        
                number_of_moves = get_number_of_moves(goal_node)
            
            output = str(number_of_moves) + ":" + layout
            f = open("demo2_output.txt", 'a')
            f.write(output + "\n")
            f.close()
            print("[" + str(layout_count) + " of " + str(all_permutations_count) + "] " + str(number_of_moves) + " moves to solve " + layout)
            layout_count = layout_count + 1
            if number_of_moves in stats:
                stats[number_of_moves] = stats[number_of_moves] + 1
            else:
                stats[number_of_moves] = 1.0
        
        # Print the statistics
        for key in stats:
            print(str(key) + " moves: " + str(int(stats[key] / all_permutations_count * 100)) + "%")

    elif args.benchmark:
        #layout = "2,7,1,5,4,3,8,6,0" # Takes 30 moves to solve
        layout = "0,5,7,1,6,4,8,2,3" # Takes 20 moves to solve
        runs = 20

        times_taken = []
        for x in range(0, runs):
            start_time = time.time()

            goal_node = bfs(Node(GameBoard(layout), None))

            times_taken.append(time.time() - start_time)
            print(str(int((x + 1) * 1.0 / runs * 100)) + "% complete")

        times_average = 0
        for time_taken in times_taken:
            times_average = times_average + time_taken

        print("Score: " + str(int(1 / (times_average / runs) * 10000)))

    # Normal mode
    else:
        # Start the timer
        start_time = time.time()
        
        # Run the breadth first search algorithm
        goal_node = bfs(Node(GameBoard(initial_layout), None))
            
        # End the timer
        time_elapsed = time.time() - start_time
        print("Time Taken: " + str(time_elapsed))
        
	if goal_node is not None:
            print_solution(goal_node, 0)


if __name__ == "__main__":
    main()
