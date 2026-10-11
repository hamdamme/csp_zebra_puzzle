import unittest
from copy import deepcopy
from csp_solver import solve, check_constraints

class SolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solution = solve()
    def test_solver_returns_valid_grid(self):
        self.assertTrue(check_constraints(self.solution))
    def test_duplicate_category_rejected(self):
        grid = deepcopy(self.solution)
        grid["Pet"][0] = grid["Pet"][1]
        self.assertFalse(check_constraints(grid))
    def test_empty_grid_rejected(self):
        self.assertFalse(check_constraints({key: [""] * 5 for key in self.solution}))
    def test_fixed_clue_cannot_be_overridden(self):
        self.assertIsNone(solve({"Nationality": ["German", "", "", "", ""]}))
    def test_complete_invalid_partial_rejected(self):
        grid = deepcopy(self.solution)
        grid["Drink"][2], grid["Drink"][0] = grid["Drink"][0], grid["Drink"][2]
        self.assertIsNone(solve(grid))
    def test_unknown_value_rejected(self):
        with self.assertRaises(ValueError):
            solve({"Color": ["Purple", "", "", "", ""]})
