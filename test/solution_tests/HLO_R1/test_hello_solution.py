from lib.solutions.HLO.hello_solution import HelloSolution

class TestHello:
    def test_hello_valid_inputs(self):
        assert HelloSolution().hello("Alice") == "Hello, Alice!"
        assert HelloSolution().hello("Bobby") == "Hello, Bobby!"
        assert HelloSolution().hello("World") == "Hello, World!"
        assert HelloSolution().hello("世界") == "Hello, 世界!"
    

    def test_hello_non_string(self):
        assert HelloSolution().hello(123) == "Hello, 123!"
        assert HelloSolution().hello(["a", "b"]) == "Hello, ['a', 'b']!"