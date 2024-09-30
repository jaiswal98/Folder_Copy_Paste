import os
import shutil
import csv

def find_and_copy_folders(csv_file, parent_folder, destination_folder):
    try:
        # Read order IDs from CSV file
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            order_ids = set()
            for row in csv_reader:
                order_id = row[0].strip()
                if order_id:
                    if order_id not in order_ids:
                        order_ids.add(order_id)
                    else:
                        print(f"Duplicate order ID '{order_id}' found in the CSV file. Ignoring duplicate.")

        print(f"Order IDs to copy: {order_ids}")

        # Traverse through each child directory of the parent directory
        for root, dirs, _ in os.walk(parent_folder):
            for dir_name in dirs:
                # Check if the directory name starts with any of the order IDs
                matching_order_id = next((order_id for order_id in order_ids if dir_name.startswith(order_id)), None)
                if matching_order_id:
                    source_path = os.path.join(root, dir_name)
                    destination_path = os.path.join(destination_folder, os.path.relpath(source_path, parent_folder))
                    try:
                        shutil.copytree(source_path, destination_path)
                        print(f"Folder '{dir_name}' copied successfully.")
                        order_ids.remove(matching_order_id)  # Remove the copied order ID from the set
                    except FileExistsError:
                        print(f"Folder '{dir_name}' already exists in the destination location.")
                    except Exception as e:
                        print(f"An error occurred while copying folder '{dir_name}': {e}")

        print("Folder copy process completed.")

    except Exception as e:
        print(f"An error occurred in find_and_copy_folders function: {e}")

# Example usage
if __name__ == "__main__":
    try:
        csv_file = input("Enter the path to the CSV file containing order IDs: ")
        parent_folder = input("Enter the path to the parent folder where child directories will be searched: ")
        destination_folder = input("Enter the path to the destination folder where folders will be copied: ")

        find_and_copy_folders(csv_file, parent_folder, destination_folder)
    except Exception as e:
        print(f"An error occurred in the main program: {e}")
