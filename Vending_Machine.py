from abc import ABC, abstractmethod

TAX_PERCENT = 0.10
COUPONS = {"DISCOUNT10": 0.10, "SAVE20": 0.20}

class Item:
    def __init__(self, code, name, price, quantity):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.code] = item

    def is_available(self, code):
        return code in self.items and self.items[code].quantity > 0

    def get_price(self, code):
        return self.items[code].price if code in self.items else 0

    def dispense(self, code):
        if self.is_available(code):
            self.items[code].quantity -= 1
            return self.items[code].name
        return None

    def restock(self, code, quantity):
        if code in self.items:
            self.items[code].quantity += quantity

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CoinPayment(Payment):
    def pay(self, amount):
        print(f"💰 Paid ₹{amount} using coins.")
        return True

class CashPayment(Payment):
    def pay(self, amount):
        print(f"💵 Paid ₹{amount} using cash.")
        return True

class CardPayment(Payment):
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self):
        return True

    def pay(self, amount):
        if self.validate():
            print(f"💳 Charged ₹{amount} to card {self.card_number[-4:]}")
            return True
        return False

class ChangeDispenser:
    def return_change(self, amount_paid, item_price):
        change = amount_paid - item_price
        if change > 0:
            print(f"🪙 Returning ₹{change} in change.")
        else:
            print("✅ Exact amount received. No change.")
        return change

class AdminPanel:
    def __init__(self, inventory):
        self.inventory = inventory

    def restock_item(self, code, quantity):
        self.inventory.restock(code, quantity)
        print(f"✅ Restocked {quantity} units of item code {code}.")

class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.change_dispenser = ChangeDispenser()

    def add_items(self, items):
        for item in items:
            self.inventory.add_item(item)

    def display_items(self):
        print("\n🧾 Available Items:")
        for code, item in self.inventory.items.items():
            print(f"  {code}: {item.name} - ₹{item.price} (Stock: {item.quantity})")

    def purchase_item(self, code, payment: Payment, coupon_code=None):
        if not self.inventory.is_available(code):
            print("❌ Item not available.")
            return

        base_price = self.inventory.get_price(code)
        price_after_coupon = base_price
        if coupon_code in COUPONS:
            discount = COUPONS[coupon_code]
            price_after_coupon *= (1 - discount)
            print(f"🎁 Applied coupon {coupon_code}: -{int(discount * 100)}%")

        final_price = round(price_after_coupon * (1 + TAX_PERCENT))
        print(f"🧾 Final price with 10% tax: ₹{final_price}")

        if payment.pay(final_price):
            item = self.inventory.dispense(code)
            print(f"🎉 Dispensing {item}")
            self.change_dispenser.return_change(final_price, final_price)
        else:
            print("❌ Payment failed.")

if __name__ == "__main__":
    machine = VendingMachine()

    coke = Item("A1", "Coke", 40, 5)
    chips = Item("B1", "Chips", 35, 2)
    juice = Item("C1", "Juice", 50, 3)
    machine.add_items([coke, chips, juice])

    machine.display_items()

    print("\n💳 Purchase using Card with DISCOUNT10 coupon:")
    card = CardPayment("1234-5678-9876-5432")
    machine.purchase_item("A1", card, coupon_code="DISCOUNT10")

    print("\n💰 Purchase using Coins:")
    coins = CoinPayment()
    machine.purchase_item("B1", coins)

    print("\n🛠 Admin Restocking:")
    admin = AdminPanel(machine.inventory)
    admin.restock_item("B1", 5)

    machine.display_items()