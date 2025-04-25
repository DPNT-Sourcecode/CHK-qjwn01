from collections import Counter

class CheckoutSolution:

    def __init__(self):
        # Prices and special offers as class attributes
        self.items = [
            {'item': 'A', 'price': 50, 'offer': (3, 130)},
            {'item': 'B', 'price': 30, 'offer': (2, 45)},
            {'item': 'C', 'price': 20, 'offer': None},
            {'item': 'D', 'price': 15, 'offer': None},
            {'item': 'E', 'price': 40, 'offer': (2, 80, 'B')}
        ]
        self.free_items_given = Counter()
        
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
        print( 'freebie offer')
        price = item_details['price']
        # Extract offer details: quantity, price, and the free item
        offer_qty, offer_price, free_item = item_details['offer']

       
        # Calculate how many sets of the offer can be applied
        free_item_count = count // offer_qty

        self.free_items_given[free_item] += free_item_count

        print(free_item)
        # Total for the purchased items (excluding the free items)
        total = (count*price)
        return total

    def checkout(self, skus: str) -> int:
        # Get the item lookup once
        item_lookup = self._get_item_lookup()

        self.free_items_given = Counter() #reset the count of free items per 'checkout'

        # Handle empty or invalid input
        if not skus:
            return 0
        
        if not self._is_valid_input(skus, item_lookup):
            return -1

        total = 0
        counts = Counter(skus)

        # # Process each item based on whether it has an offer or not
        # for item, count in counts.items():
        #     item_details = item_lookup[item]
            
        #     # If the item has an offer, apply the offer
        #     if item_details['offer']:
        #         total += self._apply_offer(item_details, count, item_lookup)
        #     else:
        #         # If no offer, just add the regular price * count
        #         total += item_details['price'] * count

        

        # # Final bill adjustment — subtract free item prices from total
        # for item, free_count in self.free_items_given.items():
            
        #     if item in counts:  # Only subtract if the item exists in basket
        #         actual_free = min(free_count, counts[item])  # Only discount items that exist
        #         total -= actual_free * item_lookup[item]['price']

        # Stage 1 — Award freebies
        for item, count in counts.items():
            item_details = item_lookup[item]
            if item_details['offer'] and isinstance(item_details['offer'], (tuple, list)) and len(item_details['offer']) == 3:
                offer_qty, _, free_item = item_details['offer']
                offer_sets = count // offer_qty
                self.free_items_given[free_item] += offer_sets

        # Stage 2 — Adjust basket by removing freebies
        for free_item, free_qty in self.free_items_given.items():
            if free_item in counts:
                counts[free_item] = max(0, counts[free_item] - free_qty)

        #Stage 3 — Apply multi-buy offers and pricing on the adjusted basket
        for item, count in counts.items():
            item_details = item_lookup[item]

            if item_details['offer']:
                offer = item_details['offer']
                if isinstance(offer, (tuple, list)) and len(offer) == 2:
                    total += self._apply_multi_price_offer(item_details, count)
                else:
                    total += item_details['price'] * count
            else:
                total += item_details['price'] * count

        return total