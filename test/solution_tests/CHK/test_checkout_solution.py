import pytest

from lib.solutions.CHK.checkout_solution import CheckoutSolution

class TestCheckoutSolution:
    def test_checkout_valid_skus_with_offer(self):
        # Test that the correct offers are applied
        assert CheckoutSolution().checkout("AAABBCD") == 210  # 3A for 130, 2B for 45, 1C for 20, 1D for 15
        assert CheckoutSolution().checkout("AAA") == 130  # 3A for 130
        assert CheckoutSolution().checkout("BB") == 45  # 2B for 45
        assert CheckoutSolution().checkout("CC") == 40  # 2C for regular price
        assert CheckoutSolution().checkout("D") == 15  # Single D at regular price
        #assert CheckoutSolution().checkout("EE") == 80  # 2E for 80 (no free B because 2E triggers the discount)

    #def test_checkout_special_offer(self):
        # Test that special offers like "Buy 2E for 80, get 1B free" are applied
        #assert CheckoutSolution().checkout("EE") == 80  # 2E for 80, get 1 B free
        #assert CheckoutSolution().checkout("EEE") == 120  # 2E for 80, get 1B free, 1E at normal price
        #assert CheckoutSolution().checkout("EEEE") == 160  # 4E, 2 offers, get 2 B's free

    def test_checkout_insufficient_quantity_for_offer(self):
        # Test for cases where the offer cannot be applied due to insufficient quantity
        # assert CheckoutSolution().checkout("E") == 40  # Can't apply the offer, just pay normal price for 1 E
        assert CheckoutSolution().checkout("A") == 50  # Can't apply the offer, just pay normal price for 1 A

    def test_checkout_no_offer(self):
        # Test that items without offers are charged at normal price
        assert CheckoutSolution().checkout("C") == 20  # No offer for C
        assert CheckoutSolution().checkout("D") == 15  # No offer for D

    def test_checkout_empty_input(self):
        # Test empty input handling (should return 0)
        assert CheckoutSolution().checkout("") == 0  # Empty basket should return 0
        assert CheckoutSolution().checkout(None) == 0  # None as input

    def test_checkout_invalid_input(self):
        # Test invalid SKU input (should return -1)
        assert CheckoutSolution().checkout("AAAX") == -1  # Invalid SKU X
        assert CheckoutSolution().checkout("ZZZ") == -1  # Invalid SKUs
        assert CheckoutSolution().checkout("123") == -1  # Non-letter characters
        assert CheckoutSolution().checkout("AAB@") == -1  # Invalid character '@'
        
    #def test_checkout_combined_items_with_offers(self):
        # Test combining items with offers and regular prices
        #assert CheckoutSolution().checkout("AAABBCDDE") == 380  # 3A for 130, 2B for 45, 1C for 20, 1D for 15, 2E for 80

    #def test_checkout_special_offer_with_b(self):
        # Test that 2 E's with 1 B in the basket correctly applies the offer and sets B to 0 cost
        #assert CheckoutSolution().checkout("EEB") == 80  # 2E for 80, 1 B free (B's cost should be 0)

