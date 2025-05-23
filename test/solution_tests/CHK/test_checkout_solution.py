import pytest

from lib.solutions.CHK.checkout_solution import CheckoutSolution

class TestCheckoutSolution:
    def test_checkout_valid_skus_with_offer(self):
        # Test that the correct offers are applied
        assert CheckoutSolution().checkout("AAABBCD") == 210  # 3A for 130, 2B for 45, 1C for 20, 1D for 15
        assert CheckoutSolution().checkout("AAA") == 130  # 3A for 130
        assert CheckoutSolution().checkout("AAAAA") == 200  # 5A for 200
        assert CheckoutSolution().checkout("AAAAAA") == 250  # 5A for 200 + A for 50
        assert CheckoutSolution().checkout("AAAAAAA") == 300  # 5A for 200 + 2A for 100
        assert CheckoutSolution().checkout("BB") == 45  # 2B for 45
        assert CheckoutSolution().checkout("CC") == 40  # 2C for regular price
        assert CheckoutSolution().checkout("D") == 15  # Single D at regular price
        assert CheckoutSolution().checkout("EE") == 80  # 2E for 80 (no free B because 2E triggers the discount)

    def test_checkout_special_offer(self):
        #Test that special offers like "Buy 2E for 80, get 1B free" are applied
        assert CheckoutSolution().checkout("EE") == 80  # 2E for 80, get 1 B free
        assert CheckoutSolution().checkout("EEE") == 120  # 2E for 80, get 1B free, 1E at normal price
        assert CheckoutSolution().checkout("EEEE") == 160  # 4E, 2 offers, get 2 B's free

    def test_checkout_insufficient_quantity_for_offer(self):
        # Test for cases where the offer cannot be applied due to insufficient quantity
        assert CheckoutSolution().checkout("E") == 40  # Can't apply the offer, just pay normal price for 1 E
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
        assert CheckoutSolution().checkout("123") == -1  # Non-letter characters
        assert CheckoutSolution().checkout("AAB@") == -1  # Invalid character '@'
        
    def test_checkout_combined_items_with_offers(self):
        #Test combining items with offers and regular prices
        assert CheckoutSolution().checkout("EEB") == 80  #
        assert CheckoutSolution().checkout("EE") == 80
        assert CheckoutSolution().checkout("EEBB") == 110

    def test_checkout_special_offer_with_b(self):
        # Test that 2 E's with 1 B in the basket correctly applies the offer and sets B to 0 cost
        assert CheckoutSolution().checkout("EEB") == 80  # 2E for 80, 1 B free (B's cost should be 0)

    def test_checkout_item_f_offers(self):
        # F freebie offer check
        assert CheckoutSolution().checkout("FFF") == 20  # 2F paid, 1F free
        assert CheckoutSolution().checkout("FFFFFF") == 40  # 4F paid, 2F free (6 F's)
        assert CheckoutSolution().checkout("F") == 10  # 1F paid, no freebie
        assert CheckoutSolution().checkout("FF") == 20  # 2F paid, no freebie yet

    def test_grp_discount(self):
        
        assert CheckoutSolution().checkout("S") == 20  
        assert CheckoutSolution().checkout("ST") == 40 
        assert CheckoutSolution().checkout("STX") == 45 
        assert CheckoutSolution().checkout("SXYZ") == 62
        assert CheckoutSolution().checkout("SXYZXY") == 90
        assert CheckoutSolution().checkout("SXYZXYZ") == 107
        


