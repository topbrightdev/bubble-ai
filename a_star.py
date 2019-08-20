import heapq


def a_star(start, is_goal, heuristic, g_function):
    """
    runs a star algorithm to find goal node in graph
    :param start: Game object representing the start state
    :param is_goal: a functions that determines whether a state is a goal state or not
    :param heuristic: a function that gives the heuristic's value of a state
    :param g_function: a function that returns the cost of the path from the start state to the current state
    :return: path, path_size, open_nodes
    path - list of actions to be done
    path_size - len of path
    open_nodes - nodes that were visited by the algorithm
    """
    visited_set = set()
    fringe_heap = [start]
    came_from = {}
    open_nodes = 0
    path = []
    path_size = 0

    while len(fringe_heap):
        current = heapq.heappop(fringe_heap)
        open_nodes += 1
        if is_goal(current, start):
            path, path_size = reconstruct_path(came_from, current)
            return path, path_size, open_nodes

        visited_set.add(current)

        list_of_childs = current.get_successors()
        for child in list_of_childs:
            child_node, child_action = child
            if child_node.dead_player or child_node in visited_set:
                continue

            g = g_function(child_node, start)
            if child_node not in fringe_heap:
                heapq.heappush(fringe_heap, child_node)
                h = heuristic(child_node, start)
                child_node.update_h_score(h)
            elif g <= child_node.get_g_score(): # if we already discovered this node, with better g
                continue

            # This path is the best until now
            came_from[child_node] = [current, child_action]
            child_node.update_g_score(g)
    # if we get here - return default (empty) path
    return path, path_size, open_nodes


def reconstruct_path(came_from, current):
    """
    reconstructs path from a dictionary containing a nodes and their parents.
    :param came_from: a dictionary containing a nodes and their parents.
    :param current: the node used for starting the reconstruction (last node)
    :return: reconstructed path and it's length
    """
    total_path = []
    while current in came_from.keys():
        # add the action that get from previous to the current node, and insert to the start of the list
        total_path.insert(0, came_from[current][1])
        current = came_from[current][0]
    return total_path, len(total_path)
