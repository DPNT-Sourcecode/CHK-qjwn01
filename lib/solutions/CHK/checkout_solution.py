from collections import Counter

class CheckoutSolution:

    def __init__(self):
        # Prices and special offers as class attributes
        self.items = [
            {'item': 'A', 'price': 50, 'offer': {'multibuy_price': [(5, 200), (3, 130)]}},
            {'item': 'B', 'price': 30, 'offer': {'multibuy_price': (2, 45)}},
            {'item': 'C', 'price': 20, 'offer': None},
            {'item': 'D', 'price': 15, 'offer': None},
            {'item': 'E', 'price': 40, 'offer': {'freebie': (2, 'B')}},
            {'item': 'F', 'price': 10, 'offer': {'freebie': (3, 'F')}},
            {'item': 'G', 'price': 20, 'offer': None},
            {'item': 'H', 'price': 10, 'offer': {'multibuy_price': [(10, 80), (5, 45)]}},
            {'item': 'I', 'price': 35, 'offer': None},
            {'item': 'J', 'price': 60, 'offer': None},
            {'item': 'K', 'price': 80, 'offer': {'multibuy_price': (2, 150)}},
            {'item': 'L', 'price': 90, 'offer': None},
            {'item': 'M', 'price': 15, 'offer': None},
            {'item': 'N', 'price': 40, 'offer': {'freebie': (3, 'M')}},
            {'item': 'O', 'price': 10, 'offer': None},
            {'item': 'P', 'price': 50, 'offer': {'multibuy_price': (5, 200)}},
            {'item': 'Q', 'price': 30, 'offer': {'multibuy_price': (3, 80)}},
            {'item': 'R', 'price': 50, 'offer': {'freebie': (3, 'Q')}},
            {'item': 'S', 'price': 30, 'offer': None},
            {'item': 'T', 'price': 20, 'offer': None},
            {'item': 'U', 'price': 40, 'offer': {'freebie': (4, 'U')}}, #self_freebie
            {'item': 'V', 'price': 50, 'offer': {'multibuy_price': [(3, 130), (2, 90)]}},
            {'item': 'W', 'price': 20, 'offer': None},
            {'item': 'X', 'price': 90, 'offer': None},
            {'item': 'Y', 'price': 10, 'offer': None},
            {'item': 'Z', 'price': 50, 'offer': None}
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
 
    def _award_freebies(self,counts, item_lookup):
        for item, count in counts.items():
            item_details = item_lookup[item]
            offer = item_details.get('offer')
            if offer and 'freebie' in offer:
                offer_qty, free_item = offer['freebie']
                offer_sets = count // offer_qty
                self.free_items_given[free_item] += offer_sets

    def _remove_freebies(self, counts):
        for free_item, free_qty in self.free_items_given.items():
            if free_item in counts:
                counts[free_item] = max(0, counts[free_item] - free_qty)
    

    def _apply_multi_price_offer(self, item_details: dict, count: int) -> int:
        price = item_details['price']
        multibuy_offer = item_details['offer'].get('multibuy_price')

        if isinstance(multibuy_offer, tuple):
            multibuy_offer = [multibuy_offer]

        multibuy_offer = sorted(multibuy_offer, key=lambda x: x[0], reverse=True)

        total = 0
        for offer_qty, offer_price in multibuy_offer:
            sets = count // offer_qty
            total += sets * offer_price
            count -= sets * offer_qty

        total += count * price
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


        # Stage 1 — Award freebies
        self._award_freebies(counts, item_lookup)
        

        # Stage 2 — Adjust basket by removing freebies
        self._remove_freebies(counts)
        

        #Stage 3 — Apply multi-buy offers and pricing on the adjusted basket
        for item, count in counts.items():
            item_details = item_lookup[item]

            offer = item_details.get('offer')

            if offer and 'multibuy_price' in offer:
                    total += self._apply_multi_price_offer(item_details, count)
            else:
                total += item_details['price'] * count


        return total