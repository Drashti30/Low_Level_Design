from enum import Enum

class Size(Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'

class Crust(Enum):
    Thin = "Thin Crust"
    PAN = "Pan Tossed"
    STUFFED = "Cheese Stuffed Pizza"
    Newyork = "New York"

class Topping:
    def __init__(self,name,price):
        self.name = name
        self.price = price

class Coupon:
    def __init__(self, code, discount_type, value):
        self.code = code                          # e.g., "SAVE10"
        self.discount_type = discount_type        # "flat" or "percent"
        self.value = value                        # 10 for $10 off or 10% off


class Pizza:
    TAX_RATE = 0.08
    def __init__(self,size,crust):
        self.crust = crust
        self.size = size
        self .toppings = []
        self.coupon = None


    def add_toppings(self,topping):
        self.toppings.append(topping)

    def remove_topping(self,topping_name):
        self.toppings = [t for t in self.toppings if t.name.lower() != topping_name.lower()]
    
    def apply_coupon(self, coupon):
        self.coupon = coupon
    
    def calculate_price(self):
        base_price = {Size.SMALL : 6 , Size.MEDIUM: 8 , Size.LARGE: 10}[self.size]
        crust_price = {Crust.Thin: 2, Crust.PAN : 3, Crust.STUFFED : 7, Crust.Newyork : 6}[self.crust]
        topping_price = sum([t.price for t in self.toppings])
        sub_total = base_price + crust_price + topping_price

        if self.coupon:
            if self.coupon.discount_type == 'flat':
                sub_total -= self.coupon.value
            elif self.coupon.discount_type == 'percent':
                sub_total -= (self.coupon.value / 100.0) * sub_total


            
        tax = sub_total * Pizza.TAX_RATE
        total_price = sub_total + tax
    
        return round(total_price, 2)


pizza = Pizza(Size.MEDIUM, Crust.PAN)
pizza.add_toppings(Topping("Mushroom", 1.0))
pizza.add_toppings(Topping("Olives", 1.5))
pizza.add_toppings(Topping("Extra Cheese", 2))
pizza.add_toppings(Topping("Tomatoes", 1))
pizza.add_toppings(Topping("Pinepal", 1))

# Apply a 10% discount coupon
coupon = Coupon("SAVE10", "percent", 10)
pizza.apply_coupon(coupon)

print("Total with tax and discount:", pizza.calculate_price())  
# Base: 7 + 2 + 2.5 = 11.5  
# 10% off → 10.35  
# + 8% tax → ~11.18
