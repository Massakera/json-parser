import os
import subprocess

# Base directory containing your test step folders
base_test_dir = 'tests/'

# List of step directories to iterate through
step_dirs = ['step1', 'step2', 'step3', 'step4']

for step_dir in step_dirs:
    # Construct the path to the current step directory
    current_test_dir = os.path.join(base_test_dir, step_dir)
    
    print(f"Testing in {current_test_dir}...")

    # Check if the step directory exists
    if not os.path.exists(current_test_dir):
        print(f"Directory {current_test_dir} does not exist, skipping...")
        continue

    # Iterate over every file in the current step directory
    for filename in os.listdir(current_test_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(current_test_dir, filename)
            print(f"Testing {file_path}...")

            # Run your JSON parser script and capture the output
            result = subprocess.run(['python3', 'json_parser.py', file_path], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"SUCCESS: {result.stdout.strip()}")
            else:
                print(f"FAILURE: {result.stderr.strip()}")
