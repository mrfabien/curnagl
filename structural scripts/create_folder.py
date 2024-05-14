import os

# Function to create folders for storms
def create_storm_folders(parent_folder, storm_count):
    for i in range(1, storm_count + 1):
        storm_folder_name = f"storm_{i}"
        storm_folder_path = os.path.join(parent_folder, storm_folder_name)
        os.makedirs(storm_folder_path)
        print(f"Created folder: {storm_folder_path}")

# Read CSV file and create folders
def create_folders_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        variables = [line.strip() for line in file.readlines()]
        for variable in variables:
            folder_path = os.path.join(os.getcwd(), variable)
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
            create_storm_folders(folder_path, 96)

# Example usage: provide the CSV file name as an argument
if __name__ == "__main__":
    csv_file = input("Enter the CSV file name: ")
    create_folders_from_csv(csv_file)
