from Models.redis_client import RedisClient
from Models.account import Account
from Utils.data_loader import DataLoader

def main():
    try:
        # Create Redis Client directly without using get_client
        redis_client = RedisClient(
            host='mycampsiteredis.redis.cache.windows.net',
            port=6380,
            password='F21P4lrm3B63A5nNWUldt528Usqtped65AzCaNnjtg8=',
            ssl=True  # Ensure SSL is enabled if required by your Redis server
        ).client  # Access the client directly
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return

    # Initialize the Account Manager with the Redis client
    account_manager = Account(redis_client)
    
    # Load initial data from the CSV file (optional step for testing)
    try:
        data_loader = DataLoader(redis_client)
        data_loader.load_initial_data('ICT320 - Task 2 - Initial Database.csv')
    except FileNotFoundError:
        print("CSV file not found. Ensure the file path is correct.")
    except Exception as e:
        print(f"Error loading initial data: {e}")

    while True:
        print("\n1. Create Account\n2. Login\n3. Forgot Password\n4. Exit")
        choice = input("Enter your choice: ").strip().lower()  # Stripping spaces and converting input to lowercase

        # Create Account Option
        if choice in ['1', 'create account']:
            login_name = input("Enter login name (email): ").strip()
            password = input("Enter password: ").strip()
            first_name = input("Enter your first name: ").strip()
            account_manager.create_account(login_name, password, first_name)

        # Login Option
        elif choice in ['2', 'login']:
            login_name = input("Enter login name (email): ").strip()
            password = input("Enter password: ").strip()
            account_manager.login(login_name, password)

        # Forgot Password Option
        elif choice in ['3', 'forgot password']:
            login_name = input("Enter login name (email): ").strip()
            account_manager.forgot_password(login_name)

        # Exit Option
        elif choice in ['4', 'exit']:
            print("Exiting...")
            break

        # Invalid Input Handling
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
