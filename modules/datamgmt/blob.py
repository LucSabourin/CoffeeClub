from io import BytesIO
import os
from azure.storage.blob import BlobServiceClient, BlobClient

from classes.errors import ServerError

account = 'coffeechatsblob'
account_url = f'https://{account}.blob.core.windows.net'
credential_key = '68p9tLNaiMxNSY25KwKbZAiIZXChX0bjEDvL9uAJNOyl7aF/7gZLmGEDNbjSaLa709AYTGq7Ofg1+AStCv2UWw=='
store_container = 'matches'

def get_blob_service_client():
    try:
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential_key)
    except:
        raise ServerError()
    else:
        return blob_service_client

def get_blob_client(blob_url, container = store_container):
    # // would not be in folder checking process.
    if '//' in blob_url:
        try:
            blob_client = BlobClient.from_blob_url(blob_url=blob_url,credential=credential_key)
        except:
            raise ServerError()
        else:
            return blob_client
    else:
        url = account_url + '/' + container + '/' + blob_url
        try:
            blob_client = BlobClient.from_blob_url(blob_url=url, credential=credential_key)
        except:
            raise ServerError()
        else:
            return blob_client

def get_file_from_blob(location: str, container = store_container, **kwargs) -> BytesIO:
    """
    """
    blob_client = get_blob_client(location, container)
    try:
        return BytesIO(blob_client.download_blob().content_as_bytes())
    except:
        raise ServerError()

def post_file_to_blob(file_name: str, contents, tags: dict = None, container = store_container, **kwargs) -> str:
    """
    """
    blob_service_client = get_blob_service_client()
    try:
        container_client = blob_service_client.get_container_client(container)
        if container_client.exists() is False:
            container_client.create_container()
    except:
        raise ServerError()

    try:
        blob_client = blob_service_client.get_blob_client(
            container=container,
            blob=file_name
        )
        blob_client.upload_blob(contents)
        if tags is not None:
            blob_client.set_blob_tags(tags=tags)
    except:
        raise ServerError()
    else:
        return blob_client.url

def delete_file_from_blob(location: str, container = store_container, **kwargs) -> None:
    """
    """
    if check_blob_exists(location, container) is True:
        blob_client = get_blob_client(location, container)
        try:
            blob_client.delete_blob()
        except:
            raise ServerError()

def check_blob_exists(location: str, container = store_container, **kwargs) -> bool:
    """
    """
    blob_client = get_blob_client(location, container)
    try:
        return blob_client.exists()
    except:
        raise ServerError()
