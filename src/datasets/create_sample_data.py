import json
import os 

INPUT_FILE = "datasets/yelp_academic_dataset_review.json"
OUTPUT_FILE = "datasets/sample_reviews.json"
input_path = os.path.abspath(INPUT_FILE)
output_path = os.path.abspath(OUTPUT_FILE)
SAMPLE_SIZE = 500

with open(input_path, 'r') as infile, open(output_path, "w") as outfile:
    for i, line in enumerate(infile):
        if i >= 500:  
            break
        outfile.write(line)
