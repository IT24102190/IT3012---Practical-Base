#agent.py
from collections import deque
import heapq
   
class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'UCS'
        
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

        return []

    def sense_and_act(self, percept: dict):

        if not self.plan:

            start = tuple(percept['agent_pos'])

            foods = percept['all_food']

            if not foods:
                return "Up"

            # Find closest food
            goal = self.find_closest_food(
                start,
                foods
            )

            # Generate a plan
            self.plan = self.search(
                start,
                goal,
                percept['grid_size'],
                set(percept['walls'])
            )
        if self.plan:
            return self.plan.pop(0)

        return "Up"