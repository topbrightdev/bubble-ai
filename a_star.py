import heapq


def a_star(start, is_goal, heuristic, g_function):
    visited_set = set()
    fringe_heap = []
    heapq.heappush(fringe_heap, start)
    g = g_function(start)
    h = heuristic(start)
    start.update_f_score(g + h)
    came_from = {}

    while len(fringe_heap):
        current = heapq.heappop(fringe_heap)
        path, path_size = reconstruct_path(came_from, current)
        if is_goal(current, start):
            return path, path_size

        visited_set.add(current)

        list_of_childs = current.get_successors()
        for child in list_of_childs:
            child_node, child_action = child
            # TODO maybe return that later (after we check everything works)
            # if child_node.dead_player:
            #     continue
            # TODO it will never reached (this isn't the same object, we need to calculate equal game function)
            # elif child_node in visited_set:
            #     continue # Ignore the childs which is already evaluated

            g = g_function(child_node)
            h = heuristic(child_node)
            if child_node not in fringe_heap:
                heapq.heappush(fringe_heap, child_node)
                # TODO we need to check if we get the same state from two or more other ways?
            # TODO it will never reached (this isn't the same object, we need to calculate equal game function)
            # elif g + h <= child_node.get_f_score(): # if we already discovered in this node, with better g
            #     continue

            # This path is the best until now
            came_from[child_node] = [current, child_action]
            child_node.update_f_score(g + h)
    # TODO check if we get here (only if no goal found)
    return None


def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from.keys():
        total_path.insert(0, came_from[current][1])
        current = came_from[current][0]
    return total_path, len(total_path)

