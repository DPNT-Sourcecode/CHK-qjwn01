
class SumSolution:
     
    def sum(self, x, y): # Main method to compute the sum of x and y.
        self._validate_input(x, 'x')
        self._validate_input(y, 'y')
        return x + y
    
    def compute(self, x: int, y: int) -> int:
        """Legacy method for compatibility with the bot's expected method name."""
        return self.sum(x, y)

    def _validate_input (self, value: int, name: str): # Internal method to valdate range (0 - 100)
        if not (0 <= value <= 100):
            raise ValueError(f"{name} must be between 0 and 100, got {value}")
