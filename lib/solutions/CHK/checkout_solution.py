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
        total = 0

        if offer:
            best_offer_price = float('inf')  # We will track the best (lowest) price
            
            # Ensure offer is iterable (list or tuple) and apply the best one
            if isinstance(offer, (list, tuple)):  # Check if offer is iterable
                for offer_details in offer:
                    # Validate that offer_details is a tuple or list
                    if isinstance(offer_details, (list, tuple)) and len(offer_details) > 1:
                        if len(offer_details) == 2:  # Normal multi-price offer (like 3A for 130)
                            offer_qty, offer_price = offer_details
                            total_for_this_offer = (count // offer_qty) * offer_price + (count % offer_qty) * price
                        elif len(offer_details) == 3:  # Special offer with another item (like 2E for 80 get 1B free)
                            offer_qty, offer_price, free_item = offer_details
                            if count >= offer_qty:
                                free_item_count = count // offer_qty
                                free_item_details = item_lookup[free_item]
                                total_for_this_offer = (count - (free_item_count * offer_qty)) * price + free_item_count * offer_price
                            else:
                                total_for_this_offer = count * price  # If offer cannot be applied, just charge normal price
                        else:
                            total_for_this_offer = count * price  # No offer, just normal price

                        # Check if this offer gives a better (lower) total price
                        if total_for_this_offer < best_offer_price:
                            best_offer_price = total_for_this_offer
                    else:
                        # Handle invalid offer structure
                        print(f"Invalid offer details for {item_details['item']}: {offer_details}")
                        return -1  # Return -1 for invalid offer details

                total = best_offer_price  # Apply the best offer

            else:
                # Handle invalid offer format
                print(f"Invalid offer format for {item_details['item']}: {offer}")
                return -1  # Return -1 for invalid offer format

        else:
            total = count * price  # No offer, just use regular price

        return total
        
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

