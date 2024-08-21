import csv
import faker  # Install with `pip install faker`

# Initialize the Faker library
fake = faker.Faker()

# Number of rows to generate
num_rows = 100

# Generate sample data
data = [
    [
       
        fake.name(),  # Random name
        fake.email(),  # Random email
        fake.phone_number()  # Random phone number
    ]
    for i in range(num_rows)
]

# Define CSV file path
csv_file_path = 'demo.csv'

# Write to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(['name', 'email', 'phone'])
    
    # Write data
    writer.writerows(data)

print(f"CSV file '{csv_file_path}' with {num_rows} rows has been created successfully.")
