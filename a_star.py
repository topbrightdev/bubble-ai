import heapq


def a_star(start, is_goal, heuristic, g_function):
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
            print(open_nodes)
            return path, path_size, open_nodes

        visited_set.add(current)

        list_of_childs = current.get_successors()
        for child in list_of_childs:
            child_node, child_action = child
            if child_node.dead_player or child_node in visited_set:
                # TODO visited_child will never reached (this isn't the same object, we need to calculate equal game function)
                continue

            g = g_function(child_node, start)
            if child_node not in fringe_heap:
                heapq.heappush(fringe_heap, child_node)
                h = heuristic(child_node, start)
                child_node.update_h_score(h)
            elif g <= child_node.get_g_score(): # if we already discovered this node, with better g
                # TODO it will never reached (this isn't the same object, we need to calculate equal game function)
                continue

            # This path is the best until now
            came_from[child_node] = [current, child_action]
            child_node.update_g_score(g)
    print(open_nodes)
    # if we get here - return default (empty) path
    return path, path_size, open_nodes


def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from.keys():
        # add the action that get from previous to the current node, and insert to the start of the list
        total_path.insert(0, came_from[current][1])
        current = came_from[current][0]
    return total_path, len(total_path)
