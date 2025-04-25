from collections import Counter

class CheckoutSolution:

    def __init__(self):
        # Prices and special offers as class attributes
        self.items = [
            {'item': 'A', 'price': 50, 'offer': (3, 130)},
            {'item': 'B', 'price': 30, 'offer': (2, 45)},
            {'item': 'C', 'price': 20, 'offer': None},
            {'item': 'D', 'price': 15, 'offer': None},
            {'item': 'E', 'price': 40, 'offer': [(2, 40, 'B')]}
        ]
        
    def _get_item_lookup(self) -> dict:
        # Build a lookup dictionary from the items
        return {item['item']: item for item in self.items}

    def _is_valid_input(self, skus: str) -> bool:
        item_lookup = self._get_item_lookup()  # No need to pass as argument
        return isinstance(skus, str) and all(c in item_lookup for c in skus)
    
    def _apply_offer(self, item_details: dict, count: int) -> int:
        # Calculate the total price considering offers
        price = item_details['price']
        offer = item_details['offer']
        if offer:
            offer_qty, offer_price = offer
            return (count // offer_qty) * offer_price + (count % offer_qty) * price
        return count * price

    def checkout(self, skus: str) -> int:
        # Validate input and calculate total price
        item_lookup = self._get_item_lookup()
        if not skus:
            return 0
    
        if not self._is_valid_input(skus):
            return -1
        
        total = 0
        counts = Counter(skus)

        for item, count in counts.items():
            item_details = item_lookup[item]
            total += self._apply_offer(item_details, count)

        return total



