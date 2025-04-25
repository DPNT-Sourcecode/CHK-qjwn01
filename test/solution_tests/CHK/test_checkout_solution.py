import pytest

from lib.solutions.CHK.checkout_solution import CheckoutSolution

class TestCheckoutSolution:
    def test_checkout_valid_skus(self):
        assert CheckoutSolution().checkout("AAABBCD") == 210  # 3A for 130, 2B for 45, 1C for 20, 1D for 15
        assert CheckoutSolution().checkout("AAA") == 130  # 3A for 130
        assert CheckoutSolution().checkout("BB") == 45  # 2B for 45
        assert CheckoutSolution().checkout("CC") == 40  # 2C for regular price
        assert CheckoutSolution().checkout("D") == 15  # Single D at regular price

    def test_checkout_invalid_skus(self):
        assert CheckoutSolution().checkout("AAAX") == -1  # Invalid SKU X
        assert CheckoutSolution().checkout("ZZZ") == -1  # Invalid SKUs
        assert CheckoutSolution().checkout("AAB@") == -1  # Invalid character '@'
        assert CheckoutSolution().checkout("123") == -1  # Non-letter characters

    def test_checkout_empty_input(self):
        assert CheckoutSolution().checkout("") == -1  # Empty basket should be invalid
        assert CheckoutSolution().checkout(None) == -1  # None as input