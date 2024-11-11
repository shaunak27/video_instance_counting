import google.generativeai as genai
import os
import time
import json
from tqdm import tqdm
import argparse

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

off_dict = {'off_by_zero': 0, 'off_by_one': 0, 'off_by_five': 0, 'total': 0}

def process_video(category, video, ground_truth_file,data_path):
    video_file_name = f"{data_path}/base_version/{category}/{video}"

    try:
        with open(ground_truth_file) as f:
            gt_file = json.load(f)
        gt_val = gt_file[f"{video.split('.')[0]}"]
    except Exception as e:
        print(f"Error reading ground truth file: {e}")
        return None, None

    try:
        video_file = genai.upload_file(path=video_file_name)
    except Exception as e:
        print(f"File upload error: {e}")
        return None, None

    try:
        while video_file.state.name == "PROCESSING":
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)
    except Exception as e:
        print(f"Error during file processing: {e}")
        return None, None

    prompt = f"As a proficient video understanding model, your task is to closely observe the objects within the scene in the provided video and determine the total count of {category} present. Please provide your response as a single numerical value, indicating the quantity of {category} observed, without any other word."

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
        rsps = response.text.replace("\n", "").replace(".", "")
        return int(rsps), int(gt_val)
    except Exception as e:
        print(f"Error during model generation: {e}")
        return None, None

def update_off_dict(rsps, gt_val):
    if rsps == gt_val:
        off_dict['off_by_zero'] += 1
    if abs(rsps - gt_val) <= 1:
        off_dict['off_by_one'] += 1
    if abs(rsps - gt_val) <= 5:
        off_dict['off_by_five'] += 1
    
    off_dict['total'] += 1

def main():
    parser = argparse.ArgumentParser(description="Process videos and evaluate model performance.")
    parser.add_argument("--data_path", type=str, default="/path/to/data", help="Path to the root data directory")
    parser.add_argument("--ground_truth_path", type=str, default="/path/to/ground_truth", help="Path to the ground truth files")
    parser.add_argument("--output_file", type=str, default="./results.json", help="Output file to save the results")
    args = parser.parse_args()

    categories = os.listdir(os.path.join(args.data_path,"base_version"))

    for category in tqdm(categories, total=len(categories)):
        ground_truth_file = f"{args.ground_truth_path}/office1_{category}.json"
        for video in os.listdir(f"{args.data_path}/base_version/{category}"):
            rsps, gt_val = process_video(category, video, ground_truth_file, args.data_path)
            if rsps is not None and gt_val is not None:
                update_off_dict(rsps, gt_val)
        with open(args.output_file, "w") as f:
            json.dump(off_dict, f)
    
    print("Evaluation complete.")
    json.dump(off_dict, open(args.output_file, "w"))
    off_by_zero = off_dict['off_by_zero'] / off_dict['total']
    off_by_one = off_dict['off_by_one'] / off_dict['total']
    off_by_five = off_dict['off_by_five'] / off_dict['total']


    print(f"Off by zero: {off_by_zero}")
    print(f"Off by one: {off_by_one}")
    print(f"Off by five: {off_by_five}")
    print(f"Total: {off_dict['total']}") #Should be 200

    print(f"Results saved to {args.output_file}")

if __name__ == "__main__":
    main()