from lib.solutions.SUM.sum_solution import SumSolution
import pytest


class TestSum():
    def test_sum(self):
        assert SumSolution().sum(1, 2) == 3
        assert SumSolution().sum(0, 0) == 0  # Minimum valid values
        assert SumSolution().sum(100, 100) == 200  # Maximum valid values
        assert SumSolution().sum(0, 100) == 100  # Boundary case
        assert SumSolution().sum(50, 50) == 100  # Regular case

    def test_sum_invalid_inputs(self):
            """Test for invalid inputs"""
            with pytest.raises(ValueError) as excinfo:
                SumSolution().sum(150, 20)
            assert str(excinfo.value) == "x must be between 0 and 100, got 150"

            with pytest.raises(ValueError) as excinfo:
                SumSolution().sum(20, -1)
            assert str(excinfo.value) == "y must be between 0 and 100, got -1"

            with pytest.raises(ValueError) as excinfo:
                SumSolution().sum(-1, -1)
            assert str(excinfo.value) == "x must be between 0 and 100, got -1"


