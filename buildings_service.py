import json

from utilities import validate_json, check_keys_match
from jsonschema import ValidationError

from service import Service


class BuildingsService(Service):
    def __init__(self, bucket):
        super().__init__(bucket)

    def upload_file(self, upload_file_name):
        """
        Upload a file to an S3 bucket.
        :param upload_file_name: str, Name of the file to upload
        """
        if validate_json(upload_file_name, self.config["schema_file"]):
            with open(upload_file_name, 'r') as json_file:
                data = json.load(json_file)
            object_name_in_s3 = (data["country"]+'/'+ data["city"] + '/'+
                                 data["street_address"] + '/' + data["file_name"])
            self.upload_file_to_s3(upload_file_name, object_name_in_s3)
        else:
            raise Exception("Invalid JSON file")


    def download_file(self, download_file_path: str, parameters: dict):
        """
        Download a file from an S3 bucket.

        :param download_file_name: Name of the file to download
        :param parameters: dict, location parameters for search in s3
        """
        #TODO: validate parameters
        try:
            check_keys_match(self.config["schema_file"], parameters)
            object_name_in_s3 = (
                    parameters["country"] + '/' +
                    parameters["city"] + '/' +
                    parameters["street_address"] + '/' +
                    parameters["file_name"]
            )
            self.download_file_from_s3(object_name_in_s3, download_file_path)
        except ValidationError as e:
            raise ValueError(f"Validation error: {e.message}")

