from datetime import datetime

# Function to calculate age
def calculate_age(birth_date):
    today = datetime.today()
    # Calculate the difference in years
    age = today.year - birth_date.year
    
    # Adjust age if the birth date hasn't occurred this year yet
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

# Example usage
birth_date_input = input("Enter your birth date (YYYY-MM-DD): ")
birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d")

age = calculate_age(birth_date)
print(f"Your age is: {age} years")
