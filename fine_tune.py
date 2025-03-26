"""
fine_tune.py

Script to fine-tune an OpenAI model using your prepared JSONL dataset.
"""

import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_training_file(file_path):
    """
    Uploads a JSONL dataset to OpenAI for fine-tuning using the new interface.
    """
    # Open the file in binary mode and upload using the File.create method.
    with open(file_path, "rb") as file_data:
        response = client.files.create(file=file_data, purpose="fine-tune")
    return response.id


def create_fine_tune_job(training_file_id, model, n_epochs=3):
    """
    Creates a fine-tuning job using the new FineTuningJob endpoint.
    """
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model="gpt-4o-mini-2024-07-18"
    )

    return response


def poll_fine_tune_job(fine_tune_job_id, interval=30):
    """
    Polls the fine-tuning job status every 'interval' seconds.
    Returns the final job status.
    """
    while True:
        job_status = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
        status = job_status.status
        print("Fine-tuning job status:", status)
        if status in ["succeeded", "failed", "cancelled"]:
            return job_status
        time.sleep(interval)


def main():
    dataset_path = "/Users/michaelpignatelli/Documents/GitHub/ChatterBot/lingua_activities_chat.jsonl"  # Dataset from data_preparation.py

    # 1) Upload the dataset
    file_id = upload_training_file(dataset_path)
    print("Uploaded training file. File ID:", file_id)

    # 2) Create a fine-tuning job
    # fine_tune_response = create_fine_tune_job(file_id, model="gpt-4o-mini-2024-07-18", n_epochs=3)
    # fine_tune_job_id = fine_tune_response.id
    fine_tune_job_id = "ftjob-cmmq68LLeaiqrhKmpJDcY10D"
    print("Fine-tuning job created. ID:", fine_tune_job_id)

    # 3) Poll the job status
    final_status = poll_fine_tune_job(fine_tune_job_id, interval=30)
    if final_status.status == "succeeded":
        print("Fine-tuning succeeded.")
        print("Your fine-tuned model is:", final_status.fine_tuned_model)
    else:
        print("Fine-tuning failed. Details:", final_status)


if __name__ == "__main__":
    main()
