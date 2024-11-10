# RIPL Lab Task - Long-form Video Understanding

Please read through this [document](https://docs.google.com/document/d/1oHEfUq9oA7n3Ei2N9U-kwiQVHuEEWYwxnYSItemeFIo/edit?usp=sharing) to understand the task. To set up the project, follow the instructions below.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/shaunak27/video_instance_counting.git
    ```
2. Navigate to the project directory:
    ```sh
    cd video_instance_counting
    ```
3. Install the required dependencies:
    Ideally you should create a virtual environment with Python 3.10. Install the Google Generative AI library to access Gemini.
    ```sh
    pip install google-generativeai
    ```
4. Set up API keys for [Gemini](https://ai.google.dev) for your account. Set up the API key in the environment variable `GEMINI_API_KEY` as shown below:
    ```sh
    export GEMINI_API_KEY=your_api_key
    ```
## Evaluation

1. Download the data from the [Google Drive link](https://drive.google.com/drive/u/2/folders/1gvX3JOXd06CMdCSMJGhwoCgWs5wK-nXb).
2. Run the evaluation script:
    ```sh
    python gemini_eval.py --data_path /path/to/your/data --ground_truth_path /path/to/your/ground_truth_file
    ```

