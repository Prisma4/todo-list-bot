from collections import defaultdict
from typing import List

from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from api.client import client
from api.models import TaskListResponse
from states import BotStates
from utils.functions import create_task, parse_date


async def go_to_tasks(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.TASKS)


async def go_to_add_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.ADD_TASK_CATEGORY)


async def go_to_add_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(BotStates.ADD_CATEGORY)


async def get_tasks_data(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict:
    try:
        tasks_data: List[TaskListResponse] = await client.list_tasks(
            params={"user_id": event_from_user.id}
        )
    except Exception as e:
        return {"tasks": f"Error loading tasks: {str(e)}"}

    if not tasks_data or not isinstance(tasks_data, list):
        return {"tasks": "No tasks yet."}

    by_category = defaultdict(list)

    for task in tasks_data:
        category = task.category

        if not category:
            category_name = "Uncategorized"
        else:
            category_name = category.name

        by_category[category_name].append(task)

    lines = ["My tasks:"]

    for category, tasks in sorted(by_category.items()):
        lines.append(f"\n{category}:")
        for task in tasks:
            content = task.content
            date_str = ""
            if created_at := task.created_at:
                date_str += f" · {created_at.strftime('%H:%M %m.%d.%Y')}"
            if due_date := task.scheduled_at:
                date_str += f" · due {due_date.strftime('%H:%M %m.%d.%Y')}"

            line = f"  • {content}{date_str}"
            lines.append(line)

    if len(lines) == 1:
        text = "No tasks yet."
    else:
        text = "\n".join(lines)

    return {"tasks": text}


async def get_new_task_data(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> dict:
    task_text = dialog_manager.dialog_data.get("temp_task_text")
    category_name = dialog_manager.dialog_data.get("temp_category", None)
    return {
        "category": category_name,
        "content": task_text,
    }


async def save_new_category(message: Message, widget: ManagedTextInput, manager: DialogManager, value: str):
    category_name = value.strip()
    await client.get_or_create_category_by_name({"user_id": message.from_user.id, "name": category_name})
    await manager.switch_to(BotStates.TASKS)


async def save_task_category(message: Message, widget: ManagedTextInput, manager: DialogManager, value: str):
    category_name = value.strip()
    manager.dialog_data["temp_category"] = category_name
    await manager.switch_to(BotStates.ADD_TASK_TEXT)


async def skip_task_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["task_category"] = None
    await manager.switch_to(BotStates.ADD_TASK_TEXT)


async def save_task_text(message: Message, widget: ManagedTextInput, manager: DialogManager, value: str):
    task_text = value.strip()
    if task_text:
        manager.dialog_data["temp_task_text"] = task_text
        await manager.switch_to(BotStates.ADD_TASK_SCHEDULE)
    else:
        await manager.switch_to(BotStates.TASKS)


async def save_task_schedule(message: Message, widget: ManagedTextInput, manager: DialogManager, value: str):
    schedule_at = await parse_date(value)
    manager.dialog_data["scheduled_at"] = schedule_at
    await manager.switch_to(BotStates.CREATE_TASK)


async def skip_task_schedule(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["scheduled_at"] = None
    await manager.switch_to(BotStates.CREATE_TASK)


async def save_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    task_text = manager.dialog_data.pop("temp_task_text")
    category_name = manager.dialog_data.pop("temp_category", None)
    scheduled_at = manager.dialog_data.pop("scheduled_at", None)
    await create_task(task_text, callback.from_user.id, category_name, scheduled_at)
    await manager.switch_to(BotStates.TASKS)
