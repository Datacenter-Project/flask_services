import uuid 
from google.cloud import storage

def upload_blob_from_filename(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def upload_blob_from_string(bucket_name, source_file_str, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    # source_file = source_file.decode('utf-8')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_file_str)

    print(
        "File uploaded to {}.".format(
            destination_blob_name
        )
    )

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

if __name__ == "__main__":
    # input_image_path = 'sample_input_image.png'
    input_image_path = 'detect_handwriting_OCR-detect-handwriting_SMALL.png'
    
    # detect_text(input_image_path)
    # detect_document(input_image_path)
    destination_blob_name = str(uuid.uuid4())
    print(str(destination_blob_name))
    # upload_blob_from_filename("datacenter_project_bucket", input_image_path, input_image_path)
    # download_blob("datacenter_project_bucket", input_image_path, 'temp.png')
    with open(input_image_path, 'rb') as fin:
        upload_blob_from_file("datacenter_project_bucket", fin, destination_blob_name)