class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """Add a deposit to the ledger."""
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=""):
        """Withdraw an amount from the ledger if sufficient funds exist."""
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        """Calculate the current balance of the category."""
        total = sum(item['amount'] for item in self.ledger)
        return total

    def transfer(self, amount, category):
        """Transfer an amount to another category if sufficient funds exist."""
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """Check if there are sufficient funds for a withdrawal or transfer."""
        return amount <= self.get_balance()

    def __str__(self):
        """Return a string representation of the category."""
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}"
            items += f"{description:<23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    """Create a spend chart showing the percentage spent in each category."""
    
    total_spent = sum(
        sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        for category in categories
    )
    category_spent = {
        category.name: sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        for category in categories
    }

    # Calculate percentages rounded down to the nearest 10
    percentages = {
        name: (spent / total_spent) * 100 for name, spent in category_spent.items()
    }

    # Create the chart header
    chart = "Percentage spent by category\n"
    
    # Create percentage rows (100% to 0%)
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for category in categories:
            chart += "o  " if percentages[category.name] >= i else "   "
        chart += "\n"

    # Create the horizontal line (two spaces past the last bar)
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Align category names vertically
    max_length = max(len(category.name) for category in categories)
    for i in range(max_length):
        chart += "     "  # 5 spaces for alignment
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        if i != max_length - 1:
            chart += "\n"

    return chart


# Example usage
food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
clothing.deposit(500, 'initial deposit')
clothing.withdraw(50.00, 'clothes')

entertainment = Category('Entertainment')
entertainment.deposit(300, 'initial deposit')
entertainment.withdraw(100, 'movies')

# Print the food category
print(food)

# Create and print the spend chart
print(create_spend_chart([food, clothing, entertainment]))