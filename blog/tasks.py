from django.core.management import call_command
from django.conf import settings
from typing import Union
import requests
import logging
from celery import shared_task


@shared_task
def task_fetch_daily():
    call_command('fetch_posts_comments')


def build_url(endpoint, resource_id=None):
    base_url = settings.REMOTE_JSON_URL
    if resource_id:
        return f'{base_url}{endpoint}/{resource_id}/'
    else:
        return f'{base_url}{endpoint}/'


@shared_task
def sync_post_with_remote(data: Union[int, dict], action="POST"):
    object_id = data.get("id") if isinstance(data, dict) else data
    model_name = "post"
    url = build_url(model_name + "s", object_id)
    _make_remote_request(object_id, model_name, url, action, data)


@shared_task
def sync_comment_with_remote(data: Union[int, dict], action="POST"):
    object_id = data.get("id") if isinstance(data, dict) else data
    model_name = "comment"
    url = build_url(model_name + "s", object_id)
    _make_remote_request(object_id, model_name, url, action, data)


def _make_remote_request(object_id, model_name, url, action, data):
    if action not in ["DELETE", "POST", "PUT", "PATCH"]:
        logging.error(f"Unsupported action: {action}")
        return

    if action == "DELETE":
        if not object_id:
            logging.error("Object ID is required for DELETE action")
            return
        response = requests.delete(url)
    elif action in ["POST", "PUT", "PATCH"]:
        if not isinstance(data, dict):
            logging.error("Data must be a dictionary for non-DELETE actions")
            return
        if action == "POST":
            response = requests.post(url, json=data)
        elif action == "PUT":
            response = requests.put(url, json=data)
        elif action == "PATCH":
            response = requests.patch(url, json=data)

    if response.status_code == 200:
        logging.info(f"SUCCESS to {action} {model_name} with data {data} in the remote API")
    elif response.status_code == 201:
        logging.info(f"SUCCESS to {action} {model_name} with data {data} in the remote API")
    else:
        logging.error(f"FAILURE to {action} {model_name} in the remote API: {response.status_code}")
