import random
import unittest
from agent import SearchAgent
from visual_grid_game import VisualGridHuntGame


class Lab04Tests(unittest.TestCase):
    def setUp(self):
        self.agent = SearchAgent()

    def follow(self, start, path, walls, size):
        pos = start
        for action in path:
            choices = {a: p for p, a in self.agent.get_neighbors(pos, size, walls)}
            self.assertIn(action, choices)
            pos = choices[action]
        return pos

    def test_distances(self):
        self.assertEqual(self.agent.manhattan_distance((0, 0), (3, 4)), 7)
        self.assertEqual(self.agent.euclidean_distance((0, 0), (3, 4)), 5.0)

    def test_wall_detour(self):
        walls = {(1, 0), (2, 0), (0, 2), (1, 2), (2, 2)}
        for h in ('manhattan', 'euclidean'):
            path = self.agent.astar_search((0, 0), (3, 3), walls, (4, 4), h)
            self.assertEqual(len(path), 6)
            self.assertEqual(self.follow((0, 0), path, walls, (4, 4)), (3, 3))

    def test_edge_cases(self):
        self.assertEqual(self.agent.astar_search((0, 0), (0, 0), [], (3, 3)), [])
        self.assertEqual(self.agent.astar_search((0, 0), (2, 2), [(1, 2), (2, 1)], (3, 3)), [])
        self.assertEqual(self.agent.astar_search((0, 0), (3, 0), [], (3, 3)), [])
        with self.assertRaises(ValueError):
            self.agent.astar_search((0, 0), (2, 2), [], (3, 3), 'invalid')

    def test_random_maps_against_bfs(self):
        rng = random.Random(42)
        for _ in range(100):
            walls = {(x, y) for x in range(6) for y in range(6)
                     if (x, y) not in ((0, 0), (5, 5)) and rng.random() < .25}
            expected = self.agent.bfs_search((0, 0), (5, 5), (6, 6), walls)
            for h in ('manhattan', 'euclidean'):
                path = self.agent.astar_search((0, 0), (5, 5), walls, (6, 6), h)
                self.assertEqual(len(path), len(expected))
                if path:
                    self.assertEqual(self.follow((0, 0), path, walls, (6, 6)), (5, 5))

    def test_real_environment(self):
        env = VisualGridHuntGame(4, 4, 0, 0, custom_walls={(1, 0)}, traps=0)
        env.food_positions = {(2, 0), (3, 3), (0, 3)}
        while not env.is_done():
            env.execute_action(self.agent.sense_and_act(env.get_percept()))
        self.assertEqual(env.food_positions, set())
        self.assertEqual(env.score, 60)

    def test_skip_unreachable_food(self):
        percept = {'agent_pos': (0, 0), 'all_food': [(2, 0), (0, 3)],
                   'walls': [(1, 0), (2, 1)], 'grid_size': (3, 4)}
        self.assertEqual(self.agent.sense_and_act(percept), 'Up')

    def test_no_food_and_food_here(self):
        percept = {'agent_pos': (0, 0), 'all_food': [], 'walls': [], 'grid_size': (3, 3)}
        self.assertEqual(self.agent.sense_and_act(percept), 'Stay')
        percept['all_food'] = [(0, 0)]
        self.assertEqual(self.agent.sense_and_act(percept), 'Eat')


if __name__ == '__main__':
    unittest.main(verbosity=2)
