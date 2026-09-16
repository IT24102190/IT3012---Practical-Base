#agent.py
from collections import deque
import heapq
import math
   
class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'
        self.heuristic_type = 'manhattan'
        
    def manhattan_distance(self, pos, goal):
        """Lower bound on steps for four-way, unit-cost movement."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """Straight-line distance between two grid positions."""
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    def astar_search(self, start_pos, goal_pos, walls, grid_size,
                     heuristic_type='manhattan'):
        """Return a shortest list of actions, or [] if no route exists.

        Manhattan and Euclidean are consistent on this four-way grid,
        so a position can be closed when it is popped from the heap.
        """
        heuristics = {'manhattan': self.manhattan_distance,
                      'euclidean': self.euclidean_distance}
        if heuristic_type not in heuristics:
            raise ValueError("Use 'manhattan' or 'euclidean'.")
        heuristic = heuristics[heuristic_type]
        start_pos, goal_pos = tuple(start_pos), tuple(goal_pos)
        walls = {tuple(wall) for wall in walls}
        width, height = grid_size
        for x, y in (start_pos, goal_pos):
            if not (0 <= x < width and 0 <= y < height) or (x, y) in walls:
                return []

        frontier = []
        reached_states = set()
        best_g = {start_pos: 0}
        # Queue entries: (f_cost, g_cost, current_pos, path_taken).
        heapq.heappush(frontier, (heuristic(start_pos, goal_pos),
                                 0, start_pos, []))
        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)
            if current_pos in reached_states or g_cost != best_g[current_pos]:
                continue
            if current_pos == goal_pos:
                return path_taken
            reached_states.add(current_pos)
            for neighbor, action in self.get_neighbors(current_pos, grid_size, walls):
                if neighbor in reached_states:
                    continue
                new_g = g_cost + 1
                if new_g < best_g.get(neighbor, math.inf):
                    best_g[neighbor] = new_g
                    new_h = heuristic(neighbor, goal_pos)
                    heapq.heappush(frontier, (new_g + new_h, new_g,
                                             neighbor, path_taken + [action]))
        return []

    def get_neighbors(self, position, grid_size, walls):
        x,y = position
        width, height = grid_size
        
        moves = [
            ("Up", (x,y+1)),
            ("Down", (x, y-1)),
            ("Left", (x-1, y)),
            ("Right", (x+1, y))
        ]
        
        neighbors = []
        
        for action, new_pos in moves:
            nx, ny = new_pos
            
            if nx < 0 or nx >= width:
                continue
            
            if ny < 0 or ny>= height:
                continue
            
            if new_pos in walls:
                continue
            
            neighbors.append((new_pos , action))
            
        return neighbors
    
    def bfs_search(self, start, goal, grid_size, walls):
        frontier = deque()
        frontier.append((start,[]))
        
        reached = {start}
        
        while frontier:
            current, path = frontier.popleft()
            
            if current == goal:
                return path
            
            for next_pos, action in self.get_neighbors(
                current, grid_size, walls
            ):
                if next_pos not in reached:
                    reached.add(next_pos)
                    
                    new_path = path + [action]
                    frontier.append((next_pos, new_path))
        return[]
    
    def dfs_search(self, start, goal, grid_size, walls):
        frontier = []
        frontier.append((start,[]))
        
        reached = {start}
        
        while frontier:
            current, path = frontier.pop()
            
            if current == goal:
                return path
            
            neighbors = self.get_neighbors(
                current, grid_size, walls
            )
            
            for next_pos, action in reversed(neighbors):
                if next_pos not in reached:
                    reached.add(next_pos)
                    
                    new_path = path + [action]
                    frontier.append((next_pos, new_path))
        return []
    
    def ucs_search(self, start, goal,grid_size, walls):
        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )

        reached = {}

        while frontier:
            cost, _, current, path = heapq.heappop(frontier)

            if current in reached:
                continue

            reached[current] = cost

            if current == goal:
                return path

            for next_pos, action in self.get_neighbors(
                current, grid_size, walls
            ):
                if next_pos not in reached:

                    counter += 1

                    new_path = path + [action]
                    new_cost = cost + 1

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            next_pos,
                            new_path
                        )
                    )

        return []              
    

    def find_closest_food(self, start, foods):
        if not foods:
            return None

        return min(
            foods,
            key=lambda food: (
                abs(start[0] - food[0]) +
                abs(start[1] - food[1])
            )
        )

#choose search algorithm
    def search(self, start, goal, grid_size, walls):

        if self.active_algo == 'BFS':
            return self.bfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'DFS':
            return self.dfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'UCS':
            return self.ucs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'AStar':
            return self.astar_search(start, goal, walls, grid_size,
                                     self.heuristic_type)

        return []

    def sense_and_act(self, percept: dict):
        start = tuple(percept['agent_pos'])
        foods = [tuple(food) for food in percept['all_food']]
        if not foods:
            self.plan = []
            return "Stay"
        if start in foods:
            self.plan = []
            return "Eat"

        if not self.plan:
            # Closest means Manhattan distance, not wall-aware route length.
            # Try the next food if the closest food is unreachable.
            candidates = sorted(foods, key=lambda food:
                                (self.manhattan_distance(start, food), food))
            for goal in candidates:
                self.plan = self.search(start, goal, percept['grid_size'],
                                        {tuple(w) for w in percept['walls']})
                if self.plan:
                    break
        return self.plan.pop(0) if self.plan else "Stay"


if __name__ == '__main__':
    agent = SearchAgent()
    print("Manhattan:", agent.manhattan_distance((0, 0), (3, 4)))
    print("Euclidean:", agent.euclidean_distance((0, 0), (3, 4)))
