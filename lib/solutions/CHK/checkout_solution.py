from collections import Counter

class CheckoutSolution:

    def __init__(self):
        # Prices and special offers as class attributes
        self.items = [
            {'item': 'A', 'price': 50, 'offer': (3, 130)},
            {'item': 'B', 'price': 30, 'offer': (2, 45)},
            {'item': 'C', 'price': 20, 'offer': None},
            {'item': 'D', 'price': 15, 'offer': None},
            {'item': 'E', 'price': 40, 'offer': [(2, 80, 'B')]}
        ]
        
    def _get_item_lookup(self) -> dict:
        # Build a lookup dictionary from the items
        return {item['item']: item for item in self.items}

    def _is_valid_input(self, skus: str, item_lookup: dict) -> bool:
        # Validate that all characters in skus are valid (A, B, C, D, E)
        return isinstance(skus, str) and all(c in item_lookup for c in skus)

    def _apply_offer(self, item_details: dict, count: int, item_lookup: dict) -> int:
        # Main offer application logic: decide which type of offer to apply
        if len(item_details['offer']) == 2:  # Multi-price offer (like 3A for 130)
            return self._apply_multi_price_offer(item_details, count)
        elif len(item_details['offer']) == 3:  # Special offer with another item (like 2E for 80 get 1B free)
            return self._apply_special_offer(item_details, count, item_lookup)
        return count * item_details['price']  # Default: no offer applied

    def _apply_multi_price_offer(self, item_details: dict, count: int) -> int:
        # Apply multi-price offer (e.g., 3A for 130)
        price = item_details['price']
        total = 0
        for offer_details in item_details['offer']:
            offer_qty, offer_price = offer_details
            total += (count // offer_qty) * offer_price
            total += (count % offer_qty) * price
        return total

    def _apply_special_offer(self, item_details: dict, count: int, item_lookup: dict) -> int:
        price = item_details['price']
        offer_total = 0
        free_b_count = 0  # Track the number of free B's given

        # Loop through the offer details
        for offer_details in item_details['offer']:
            offer_qty, offer_price, free_item = offer_details
            
            # Apply the offer for every full set of the offer quantity
            if count >= offer_qty:
                free_item_count = count // offer_qty
                free_item_details = item_lookup[free_item]
                
                # Reduce the price of B's already in the basket by the free item offer
                # Subtract the cost of the free B's
                offer_total += (count - (free_item_count * offer_qty)) * price
                offer_total += free_item_count * offer_price  # Price of free B's (which is essentially 0 in this case)
                free_b_count += free_item_count  # Increment the free B's count
                
            else:
                offer_total += count * price  # If offer cannot be applied, just charge normal price

        return offer_total

    def checkout(self, skus: str) -> int:
        # Get the item lookup once
        item_lookup = self._get_item_lookup()

        # Handle empty or invalid input
        if not skus or not self._is_valid_input(skus, item_lookup):
            return -1

        total = 0
        counts = Counter(skus)

        # Process each item based on whether it has an offer or not
        for item, count in counts.items():
            item_details = item_lookup[item]
            total += self._apply_offer(item_details, count, item_lookup)

        return total

