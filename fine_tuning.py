import os
import openai
import time


def upload_training_file(file_path):
    """
    Uploads the chatterbot training dataset (in JSONL format) to OpenAI.
    Each JSON object should have a "prompt" with a learner's sentence (possibly with errors)
    and a "completion" with the corrected sentence and explanation.
    Returns the file ID needed to start the fine-tuning process.
    """
    with open(file_path, "rb") as f:
        response = openai.File.create(
            file=f,
            purpose="fine-tune"
        )
    return response["id"]


def create_fine_tune_job(training_file_id, model="davinci", n_epochs=4):
    """
    Creates a fine-tuning job for chatterbot using the uploaded training file.
    Parameters:
      - training_file_id: The file ID returned from uploading the dataset.
      - model: The base model to fine-tune (using "davinci" here, but can be adjusted).
      - n_epochs: Number of passes over the dataset.
    Returns the response from the fine-tuning creation request.
    """
    response = openai.FineTune.create(
        training_file=training_file_id,
        model=model,
        n_epochs=n_epochs
    )
    return response


def poll_fine_tune_job(fine_tune_job_id, interval=60):
    """
    Polls the fine-tuning job status every 'interval' seconds.
    The function prints the status and returns once the job has succeeded or failed.
    """
    while True:
        job_status = openai.FineTune.retrieve(fine_tune_job_id)
        status = job_status["status"]
        print("Job status:", status)
        if status in ["succeeded", "failed"]:
            break
        time.sleep(interval)
    return job_status


def main():
    # Ensure your OpenAI API key is stored in an environment variable named "OPENAI_API_KEY"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define the path to your chatterbot training dataset file
    training_file_path = "chatterbot_training_data.jsonl"

    # Step 1: Upload the training file to OpenAI
    print("Uploading training data for chatterbot...")
    training_file_id = upload_training_file(training_file_path)
    print("Training file uploaded. File ID:", training_file_id)

    # Step 2: Create a fine-tuning job using the uploaded training file
    print("Creating fine-tuning job...")
    fine_tune_response = create_fine_tune_job(training_file_id, model="davinci", n_epochs=4)
    fine_tune_job_id = fine_tune_response["id"]
    print("Fine-tuning job created with ID:", fine_tune_job_id)

    # Step 3: Poll the fine-tuning job status until completion
    print("Polling fine-tuning job status...")
    final_status = poll_fine_tune_job(fine_tune_job_id, interval=60)

    # Step 4: Check if the fine-tuning was successful and display the resulting model name
    if final_status["status"] == "succeeded":
        print("Fine-tuning job succeeded.")
        print("Your fine-tuned chatterbot model is:", final_status["fine_tuned_model"])
    else:
        print("Fine-tuning job failed. Final status details:", final_status)


if __name__ == "__main__":
    main()