from datetime import datetime
from typing import Optional

from dateutil.parser import parse, ParserError

from api.client import client
from api.models import GetCategoryByNameResponse


async def create_task(
        task_text: str,
        user_id: int,
        category_name: Optional[str] = None,
        scheduled_at: Optional[datetime] = None,
):
    if task_text:
        if category_name:
            response: GetCategoryByNameResponse = await client.get_or_create_category_by_name(
                {"user_id": user_id, "name": category_name})
            category = response.id
        else:
            category = None

        if scheduled_at is not None:
            scheduled_at = scheduled_at.isoformat()

        data = {"user_id": user_id, "content": task_text, "category": category,
                "scheduled_at": scheduled_at}
        await client.create_task(data)


async def parse_date(s: str) -> datetime:
    s = s.strip()

    today = datetime.today()
    default = today.replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        dt = parse(s, dayfirst=False, yearfirst=False, default=default, fuzzy=False)

        if dt.year == 1900:
            dt = dt.replace(year=today.year)

        return dt
    except ParserError as e:
        raise ValueError(f"Could not parse date/time: {s!r}") from e
    except OverflowError:
        raise ValueError(f"Date/time value out of range: {s!r}")
