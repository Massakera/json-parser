import os
import subprocess

# Directory containing your test JSON files
test_dir = 'tests/step3/'

# Iterate over every file in the test directory
for filename in os.listdir(test_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(test_dir, filename)
        print(f"Testing {file_path}...")

        # Run your JSON parser script and capture the output
        result = subprocess.run(['python3', 'json_parser.py', file_path], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"SUCCESS: {result.stdout}")
        else:
            print(f"FAILURE: {result.stderr}")
