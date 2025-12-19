import os
import glob
from phase4.main import process_file

def main():
    # Find all Phase 3 output files
    # Assuming they start with output_ and end with .json
    input_files = glob.glob("output_*.json")
    
    # Filter out any phase 4 outputs if they exist to avoid re-processing output
    input_files = [f for f in input_files if not f.startswith("phase4_output_")]

    print(f"Found {len(input_files)} files to process: {input_files}")

    for input_file in input_files:
        output_file = f"phase4_{input_file}"
        process_file(input_file, output_file)

if __name__ == "__main__":
    main()
