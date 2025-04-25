from collections import Counter

class CheckoutSolution:

    def __init__(self):
        # Prices and special offers as class attributes
        # self.items = [
        #     {'item': 'A', 'price': 50, 'offer': {'multibuy_price': [(5, 200), (3, 130)]}},
        #     {'item': 'B', 'price': 30, 'offer': {'multibuy_price': (2, 45)}},
        #     {'item': 'C', 'price': 20, 'offer': None},
        #     {'item': 'D', 'price': 15, 'offer': None},
        #     {'item': 'E', 'price': 40, 'offer': {'freebie': (2, 'B')}},
        #     {'item': 'F', 'price': 10, 'offer': {'freebie': (3, 'F')}},
        #     {'item': 'G', 'price': 20, 'offer': None},
        #     {'item': 'H', 'price': 10, 'offer': {'multibuy_price': [(10, 80), (5, 45)]}},
        #     {'item': 'I', 'price': 35, 'offer': None},
        #     {'item': 'J', 'price': 60, 'offer': None},
        #     {'item': 'K', 'price': 70, 'offer': {'multibuy_price': (2, 120)}},
        #     {'item': 'L', 'price': 90, 'offer': None},
        #     {'item': 'M', 'price': 15, 'offer': None},
        #     {'item': 'N', 'price': 40, 'offer': {'freebie': (3, 'M')}},
        #     {'item': 'O', 'price': 10, 'offer': None},
        #     {'item': 'P', 'price': 50, 'offer': {'multibuy_price': (5, 200)}},
        #     {'item': 'Q', 'price': 30, 'offer': {'multibuy_price': (3, 80)}},
        #     {'item': 'R', 'price': 50, 'offer': {'freebie': (3, 'Q')}},
        #     {'item': 'S', 'price': 20, 'offer': None},
        #     {'item': 'T', 'price': 20, 'offer': None},
        #     {'item': 'U', 'price': 40, 'offer': {'freebie': (4, 'U')}}, #self_freebie
        #     {'item': 'V', 'price': 50, 'offer': {'multibuy_price': [(3, 130), (2, 90)]}},
        #     {'item': 'W', 'price': 20, 'offer': None},
        #     {'item': 'X', 'price': 17, 'offer': None},
        #     {'item': 'Y', 'price': 20, 'offer': None},
        #     {'item': 'Z', 'price': 21, 'offer': None}
        # ]

        self.items = [
            {'item': 'A', 'price': 50, 'offer': {'multibuy_price': [(5, 200), (3, 130)]}},
            {'item': 'B', 'price': 30, 'offer': {'multibuy_price': (2, 45)}},
            {'item': 'C', 'price': 20, 'offer': None},
            {'item': 'D', 'price': 15, 'offer': None},
            {'item': 'E', 'price': 40, 'offer': {'freebie': (2, 'B')}},
            {'item': 'F', 'price': 10, 'offer': {'freebie': (3, 'F')}},  # Self-freebie (leave as is for now)
            {'item': 'G', 'price': 20, 'offer': None},
            {'item': 'H', 'price': 10, 'offer': {'multibuy_price': [(10, 80), (5, 45)]}},
            {'item': 'I', 'price': 35, 'offer': None},
            {'item': 'J', 'price': 60, 'offer': None},
            {'item': 'K', 'price': 70, 'offer': {'multibuy_price': (2, 120)}},  # Price changed
            {'item': 'L', 'price': 90, 'offer': None},
            {'item': 'M', 'price': 15, 'offer': None},
            {'item': 'N', 'price': 40, 'offer': {'freebie': (3, 'M')}},
            {'item': 'O', 'price': 10, 'offer': None},
            {'item': 'P', 'price': 50, 'offer': {'multibuy_price': (5, 200)}},
            {'item': 'Q', 'price': 30, 'offer': {'multibuy_price': (3, 80)}},
            {'item': 'R', 'price': 50, 'offer': {'freebie': (3, 'Q')}},
            {'item': 'S', 'price': 20, 'offer': {'group_discount': True}},  # NEW
            {'item': 'T', 'price': 20, 'offer': {'group_discount': True}},  # NEW
            {'item': 'U', 'price': 40, 'offer': {'freebie': (4, 'U')}},      # Self-freebie (leave as is for now)
            {'item': 'V', 'price': 50, 'offer': {'multibuy_price': [(3, 130), (2, 90)]}},
            {'item': 'W', 'price': 20, 'offer': None},
            {'item': 'X', 'price': 17, 'offer': {'group_discount': True}},  # NEW
            {'item': 'Y', 'price': 20, 'offer': {'group_discount': True}},  # NEW
            {'item': 'Z', 'price': 21, 'offer': {'group_discount': True}}   # NEW
        ]
        self.group_discount_items = ['S', 'T', 'X', 'Y', 'Z']
        self.group_discount_price = 45
        self.group_discount_quantity = 3
        self.free_items_given = Counter()
        
    def _get_item_lookup(self) -> dict:
        # Build a lookup dictionary from the items
        return {item['item']: item for item in self.items}

    def _is_valid_input(self, skus: str, item_lookup: dict) -> bool:
        # Validate that all characters in skus are valid (A, B, C, D, E)
        return isinstance(skus, str) and all(c in item_lookup for c in skus)
    
    
    def _apply_group_discount(self, counts: Counter, item_lookup: dict) -> int:
        total = 0
        group_items = []

        # Collect all group discount items from the basket
        for item in self.group_discount_items:
            group_items += [item] * counts.get(item, 0)

        # Sort group items by price descending (favor customer)
        group_items.sort(key=lambda item: item_lookup[item]['price'], reverse=True)

        # Apply group discounts
        while len(group_items) >= self.group_discount_quantity:
            total += self.group_discount_price
            for _ in range(self.group_discount_quantity):
                used_item = group_items.pop(0)
                counts[used_item] -= 1  # Mark that we've used up this item

        return total

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
        
        # Stage 3 - Apply group discounts
        total += self._apply_group_discount(counts, item_lookup)

        #Stage 4 — Apply multi-buy offers and pricing on the adjusted basket
        for item, count in counts.items():
            item_details = item_lookup[item]

            offer = item_details.get('offer')

            if offer and 'multibuy_price' in offer:
                    total += self._apply_multi_price_offer(item_details, count)
            else:
                total += item_details['price'] * count


        return total

