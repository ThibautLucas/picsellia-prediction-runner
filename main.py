from picsellia import Client
import os
import random
import argparse
import time

def init_client() -> Client:
    if "api_token" not in os.environ:
        raise Exception("You must set an api_token to run this image")
    
    api_token = os.environ["api_token"]

    if "host" not in os.environ:
        host = "https://app.picsellia.com"
    else:
        host = os.environ["host"]

    if "organization_id" not in os.environ:
        organization_id = None
    else:
        organization_id = os.environ["organization_id"]


    return Client(
        api_token=api_token, host=host, organization_id=organization_id
    )

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() in image_extensions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download dataset from Picsellia")
    parser.add_argument("--deployment_name", required=True, help="Deployment name")
    parser.add_argument("--dataset_id", required=True, help="Dataset ID to download")

    args = parser.parse_args()

    print(args.dataset_id)

    client = init_client()
    deployment = client.get_deployment(args.deployment_name)
    dataset = client.get_dataset_version_by_id(args.dataset_id)

    if not os.path.isdir(os.path.join('data', dataset.name, dataset.version)):
        os.makedirs(os.path.join('data', dataset.name, dataset.version))
    dataset.download(os.path.join('data', dataset.name, dataset.version))


    while True: 
        try:
            wait = random.randint(1,5)
            time.sleep(wait)

            fpath = None
            while fpath is None or not is_image_file(fpath):
                fpath = random.choice(os.listdir(os.path.join('data', dataset.name, dataset.version)))
                print(fpath)
            abs_path = os.path.join('data', dataset.name, dataset.version, fpath)
            prediction = deployment.predict(abs_path, tags=["predicted", "auto", dataset.name])
            print(f"Prediction sent 🥑 after {wait} s.")
        except Exception as e:
            print(f"An error occured: {e}")


