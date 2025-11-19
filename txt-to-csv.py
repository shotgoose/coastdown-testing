import os

# Get the folder where the script is located
base_folder = os.path.dirname(os.path.abspath(__file__))

# Input folder is the same as the script folder
input_folder = base_folder

# Output folder inside the script folder
output_folder = os.path.join(base_folder, "CSVdata")
os.makedirs(output_folder, exist_ok=True)

# Iterate through all .txt files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".csv"
        output_path = os.path.join(output_folder, output_filename)

        with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
            for line in f_in:
                csv_line = ','.join(line.strip().split())
                f_out.write(csv_line + '\n')

        print(f"Converted {filename} -> {output_filename}")

print("All .txt files have been converted to CSV in the 'CSVdata' folder!")