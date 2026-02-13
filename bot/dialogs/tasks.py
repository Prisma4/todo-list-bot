from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import TextInput

from handlers.tasks import go_to_tasks, go_to_add_task, go_to_add_category, get_tasks_data, save_category, \
    save_task_category, save_task_text, save_task_schedule, skip_task_category, skip_task_schedule, create_task, \
    get_new_task_data
from states import BotStates

start_window = Window(
    Const("Welcome! What would you like to do?"),
    Button(Const("View my tasks"), id="my_tasks", on_click=go_to_tasks),
    state=BotStates.START,
)

tasks_window = Window(
    Format("{tasks}"),
    Row(
        Button(Const("Add new task"), id="add_task", on_click=go_to_add_task),
        Button(Const("Add new category"), id="add_category", on_click=go_to_add_category),
    ),
    state=BotStates.TASKS,
    getter=get_tasks_data,
)

add_task_category_window = Window(
    Const("Enter category name (existing or new)"),
    TextInput(
        id="task_category_input",
        on_success=save_task_category,
    ),
    Row(
        Button(
            Const("Skip category"),
            id="skip_category",
            on_click=skip_task_category,
        ),
    ),
    state=BotStates.ADD_TASK_CATEGORY,
)


add_task_schedule_window = Window(
    Const("Enter schedule time"),
    TextInput(
        id="task_schedule_input",
        on_success=save_task_schedule,
    ),
    Row(
        Button(
            Const("Skip schedule"),
            id="skip_schedule",
            on_click=skip_task_schedule,
        ),
    ),
    state=BotStates.ADD_TASK_SCHEDULE,
)

add_task_text_window = Window(
    Const("Enter task text:"),
    TextInput(id="task_text_input", on_success=save_task_text),
    state=BotStates.ADD_TASK_TEXT,
)

add_category_window = Window(
    Const("Enter new category name:"),
    TextInput(id="category_input", on_success=save_category),
    state=BotStates.ADD_CATEGORY,
)

create_task_window = Window(
    Format("Create task in category {category} with text {content}?"),
    Row(
        Button(
            Const("Create"),
            id="create_task",
            on_click=create_task,
        ),
        Button(
            Const("Back"),
            id="back_to_task_list",
            on_click=go_to_tasks,
        )
    ),
    state=BotStates.CREATE_TASK,
    getter=get_new_task_data
)

main_dialog = Dialog(
    start_window,
    tasks_window,
    add_task_category_window,
    add_task_text_window,
    add_task_schedule_window,
    add_category_window,
    create_task_window
)
