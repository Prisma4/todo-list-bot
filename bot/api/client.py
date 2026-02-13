from api.base.client import ApiClient
from api.models import TaskCreateRequest, TaskListRequest, TaskCategoryCreateRequest, GetCategoryByNameRequest, \
    GetCategoryByNameResponse, TaskListResponse

from settings import Settings

settings = Settings()

client = ApiClient(
    base_url=settings.base_api_url,
    auth_key=settings.bot_api_auth_token
)

client.register_endpoint(
    name="create_task",
    path="tasks/tasks/",
    request_model=TaskCreateRequest,
    method="POST",
)
client.register_endpoint(
    name="list_tasks",
    path="tasks/tasks/",
    request_model=TaskListRequest,
    response_model=TaskListResponse,
    method="GET",
)
client.register_endpoint(
    name="create_task_category",
    path="tasks/category/",
    request_model=TaskCategoryCreateRequest,
    method="POST",
)
client.register_endpoint(
    name="get_or_create_category_by_name",
    path="tasks/category/get_or_create_category_by_name/",
    request_model=GetCategoryByNameRequest,
    response_model=GetCategoryByNameResponse,
    method="POST",
)
