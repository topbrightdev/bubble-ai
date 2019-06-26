import heapq

def a_star(start, goal):
    visited_set = list()
    fringe_set = []
    cameFrom = {}
    g_function = {}
    f_function = {}
    g_function[start] = 0
    f_function[start] = - zero_heuristic(start, goal)

    while len(fringe_set):
        current = heapq.heappop(fringe_set)
        path, size_path = reconstruct_path(cameFrom, current)
        if is_goal(current, size_path):
            return path, size_path
        fringe_set.remove(current)
        visited_set.append(current)

        list_of_childs = current.get_successors

        for child in list_of_childs:
            if child in visited_set:
                continue # Ignore the childs which is already evaluated
            tentative_g = child.get_score()

            if child not in fringe_set:
                fringe_set.append(child)
                # TODO we need to check if we get the same state from two or more other ways?
            elif tentative_g <= g_function[child]: # if we already discovered in this node
                continue

            # This path is the best until now
            cameFrom[child] = current
            g_function[child] = tentative_g
            f_function[child] = - g_function[child] - zero_heuristic(child, goal) # TODO we need to do it with minus?


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.Keys:
        current = cameFrom[current]
        total_path.append(current)
    return total_path, len(total_path)


def zero_heuristic(start, goal):
    return 0

def is_goal(game, path_size):
    return None
