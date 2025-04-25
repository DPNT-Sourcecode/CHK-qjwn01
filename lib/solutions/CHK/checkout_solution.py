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
        price = item_details['price']
        offer = item_details['offer']
        
        # If there's a multi-buy price offer, apply it
        best_offer_price = float('inf')  # Start with a very high price

        if isinstance(offer, (tuple, list)):  # Check if the offer is iterable (list or tuple)
            if len(offer) == 2:  # Multi-price offer (e.g., 3A for 130)
                    return self._apply_multi_price_offer(item_details, count)
            if len(offer) == 3:  # Freebie offer (e.g., 2E gets free B)
                    return self._apply_freebie_offer(item_details, count)
            
        # If no valid offer, just return the regular price
        return count * item_details['price']
 
            
    def _apply_multi_price_offer(self, item_details: dict, count: int) -> int:
        price = item_details['price']
        total = 0

        offer_qty, offer_price = item_details['offer']
        
        # Apply the offer for full sets and calculate the remainder at regular price
        total += (count // offer_qty) * offer_price
        total += (count % offer_qty) * price
        
        return total

    def _apply_freebie_offer(self, item_details: dict, count: int) -> int:
        price = item_details['price']
        total = 0

        # Extract offer details: quantity, price, and the free item
        offer_qty, offer_price, free_item = item_details['offer']

        # Check if we have enough items to apply the offer
        if count >= offer_qty:
            # Calculate how many sets of the offer can be applied
            free_item_count = count // offer_qty
            
            # Total for the purchased items (excluding the free items)
            total = (count - (free_item_count * offer_qty)) * price + free_item_count * offer_price
            
            # Add the free item to the total (free item should be priced at 0)
            # We handle the free item in the checkout method by setting its price to 0 (for simplicity, we assume the free item is handled elsewhere)
            total += self._apply_freebie_item(free_item, free_item_count)
        
        else:
            # If the offer can't be applied (not enough items), just charge the regular price
            total = count * price

        return total

    def _apply_freebie_item(self, free_item: str, free_item_count: int) -> int:
        # Handle the free item's price, which is always 0
        return 0  # Free item costs nothing

    def checkout(self, skus: str) -> int:
        # Get the item lookup once
        item_lookup = self._get_item_lookup()

        # Handle empty or invalid input
        if not skus:
            return 0
        
        if not self._is_valid_input(skus, item_lookup):
            return -1

        total = 0
        counts = Counter(skus)

        # Process each item based on whether it has an offer or not
        for item, count in counts.items():
            item_details = item_lookup[item]
            
            # If the item has an offer, apply the offer
            if item_details['offer']:
                total += self._apply_offer(item_details, count, item_lookup)
            else:
                # If no offer, just add the regular price * count
                total += item_details['price'] * count

        return total
