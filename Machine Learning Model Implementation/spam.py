# Import required libraries
import pandas as pd  # For data manipulation and CSV file handling
import os  # For file system operations

def validate_csv_file(file_path: str) -> bool:
    """
    Validate if the CSV file exists and has the correct format.
    This function checks for file existence, non-empty status, and required columns.
    
    Args:
        file_path (str): Path to the CSV file to validate
    
    Returns:
        bool: True if file is valid and has correct format, False otherwise
    """
    # Step 1: Check if the file exists in the specified path
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        return False
    
    # Step 2: Check if the file is empty (size = 0 bytes)
    if os.path.getsize(file_path) == 0:
        print(f"Error: File '{file_path}' is empty")
        return False
    
    try:
        # Step 3: Attempt to read the first 5 rows of the CSV file
        # Using latin-1 encoding which is common for spam datasets
        df = pd.read_csv(file_path, nrows=5, encoding='latin-1')
        
        # Step 4: Verify that the required columns exist
        # v1 = label column (spam/ham)
        # v2 = text column (message content)
        required_columns = ['v1', 'v2']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: Missing required columns. File must contain columns: {required_columns}")
            return False
            
        # If all checks pass, return True
        return True
        
    except Exception as e:
        # Catch and report any errors during file reading
        print(f"Error reading CSV file: {str(e)}")
        return False

def create_sample_csv(file_path: str):
    """
    Create a sample spam CSV file with correct structure.
    This function generates a small example dataset with both spam and ham messages.
    
    Args:
        file_path (str): Path where the sample file will be created
    """
    # Define sample data with correct column structure
    # Include examples of both spam and ham messages
    sample_data = """v1,v2
ham,Hello how are you?
spam,CONGRATULATIONS! You've won a prize!
ham,Meeting at 3pm tomorrow
spam,Get 90% discount today only!
"""
    # Write the sample data to a new file
    # Using latin-1 encoding for compatibility
    with open(file_path, 'w', encoding='latin-1') as f:
        f.write(sample_data)
    print(f"Created sample file at: {file_path}")

def load_spam_data(file_path: str) -> pd.DataFrame:
    """
    Load and validate spam dataset.
    This function combines validation and loading of the spam CSV file.
    
    Args:
        file_path (str): Path to the spam CSV file to load
    
    Returns:
        pd.DataFrame: Loaded dataset if valid
    
    Raises:
        ValueError: If the file is invalid or missing
    """
    # Step 1: Validate the file before attempting to load
    if not validate_csv_file(file_path):
        # If validation fails, show an example of the correct format
        print("\nExample of correct CSV format:")
        print("v1,v2")
        print("ham,Hello how are you?")
        print("spam,CONGRATULATIONS! You've won a prize!")
        raise ValueError("Invalid or missing CSV file. Please check the format above.")
    
    # Step 2: If validation passes, load and return the full file
    return pd.read_csv(file_path, encoding='latin-1')

# Main execution block
if __name__ == "__main__":
    try:
        # Step 1: Define the sample file name
        sample_file = "sample_spam.csv"
        
        # Step 2: Create a sample file if it doesn't exist
        if not os.path.exists(sample_file):
            create_sample_csv(sample_file)
        
        # Step 3: Load and validate the data
        df = load_spam_data(sample_file)
        
        # Step 4: Display the first few rows of the loaded data
        print("\nSuccessfully loaded data:")
        print(df.head())
        
    except Exception as e:
        # Handle any errors that occur during execution
        print(f"Error: {str(e)}")
