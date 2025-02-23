import getpass
import bcrypt
import json

class ATM:
    def __init__(self):
        # Load data from file (if available)
        self.data_file = "atm_data.json"
        self.balance = 1000  # Default balance
        self.pin = None  # PIN will be hashed
        self.transactions = []
        
        self.load_data()  # Load previous data if exists
        
        # If no PIN is set, initialize it
        if self.pin is None:
            self.set_initial_pin()

    def set_initial_pin(self):
        """Set an initial PIN (only for first-time users)."""
        while True:
            new_pin = getpass.getpass("Set your new PIN: ")
            confirm_pin = getpass.getpass("Confirm your new PIN: ")
            if new_pin == confirm_pin:
                self.pin = bcrypt.hashpw(new_pin.encode(), bcrypt.gensalt()).decode()
                print("PIN set successfully!")
                self.save_data()  # Save to file
                break
            else:
                print("PINs do not match. Please try again.")

    def save_data(self):
        """Save balance, PIN, and transactions to a file."""
        data = {
            "balance": self.balance,
            "pin": self.pin,
            "transactions": self.transactions
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def load_data(self):
        """Load balance, PIN, and transactions from a file if it exists."""
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.balance = data.get("balance", 1000)
                self.pin = data.get("pin")
                self.transactions = data.get("transactions", [])
        except FileNotFoundError:
            pass  # No data file yet, continue with defaults

    def verify_pin(self):
        """Prompt user for PIN verification."""
        entered_pin = getpass.getpass("Enter your PIN: ")
        if bcrypt.checkpw(entered_pin.encode(), self.pin.encode()):
            return True
        else:
            print("Incorrect PIN. Access denied.")
            return False

    def check_balance(self):
        if self.verify_pin():
            print(f"Your current balance is: ₹{self.balance}")
            self.transactions.append("Checked balance")
            self.save_data()

    def deposit(self):
        if self.verify_pin():
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount > 0:
                    self.balance += amount
                    print(f"₹{amount} deposited successfully!")
                    self.transactions.append(f"Deposited: ₹{amount}")
                    self.save_data()
                else:
                    print("Invalid deposit amount.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def withdraw(self):
        if self.verify_pin():
            try:
                amount = float(input("Enter amount to withdraw: "))
                if 0 < amount <= self.balance:
                    self.balance -= amount
                    print(f"₹{amount} withdrawn successfully!")
                    self.transactions.append(f"Withdrew: ₹{amount}")
                    self.save_data()
                else:
                    print("Invalid amount or insufficient funds.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def change_pin(self):
        if self.verify_pin():
            while True:
                new_pin = getpass.getpass("Enter new PIN: ")
                confirm_pin = getpass.getpass("Confirm new PIN: ")
                if new_pin == confirm_pin:
                    self.pin = bcrypt.hashpw(new_pin.encode(), bcrypt.gensalt()).decode()
                    print("PIN changed successfully!")
                    self.transactions.append("Changed PIN")
                    self.save_data()
                    break
                else:
                    print("PIN confirmation failed. Try again.")

    def show_transactions(self):
        if self.verify_pin():
            print("Transaction History:")
            if not self.transactions:
                print("No transactions yet.")
            else:
                for transaction in self.transactions:
                    print(f" - {transaction}")

    def main_menu(self):
        while True:
            print("\nATM Machine:")
            print("1. Check Balance")
            print("2. Deposit Cash")
            print("3. Withdraw Cash")
            print("4. Change PIN")
            print("5. Transaction History")
            print("6. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.change_pin()
            elif choice == "5":
                self.show_transactions()
            elif choice == "6":
                print("Thank you for using our ATM!")
                break
            else:
                print("Invalid choice. Enter a number between 1 and 6.")

# Run the ATM Simulation
if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()
