from lib.solutions.HLO.hello_solution import HelloSolution

class TestHello:
    def test_hello_valid_inputs(self):
        assert HelloSolution().hello("Alice") == "Hello, World!"
        assert HelloSolution().hello("Bobby") == "Hello, World!"
        assert HelloSolution().hello("World") == "Hello, World!"
        assert HelloSolution().hello("世界") == "Hello, World!"
    
    def test_hello_valid_empty_input(self):
        assert HelloSolution().hello("") == "Hello, World!"
        assert HelloSolution().hello(None) == "Hello, World!"
        assert HelloSolution().hello() == "Hello, World!"

    def test_hello_non_string(self):
        assert HelloSolution().hello(123) == "Hello, World!"
        assert HelloSolution().hello(["a", "b"]) == "Hello, World!"