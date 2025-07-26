#!/usr/bin/env python3

import os
import datetime
from typing import Optional, List, Tuple, cast
from tzlocal import get_localzone
from icalendar import Calendar, Event, Component

# Config
ICS_FILE: str = os.path.expanduser(
    "~/.local/share/evolution/calendar/system/calendar.ics"
)
ALERT_IF_IN_NEXT_MINUTES: int = 10
ALERT_POPUP_BEFORE_SECONDS: int = 20
NERD_FONT_FREE: str = "󱁕"
NERD_FONT_MEETING: str = "󰤙"

# Type aliases
FormattedEvent = Tuple[datetime.datetime, datetime.datetime, str, int]
CalendarEvent = Tuple[datetime.datetime, datetime.datetime, Event]


def load_calendar(path: str) -> Component:
    with open(path, "r") as f:
        return Calendar.from_ical(f.read())


def get_upcoming_events(
    cal: Component,
    now_time: datetime.datetime,
    today_end_time: datetime.datetime,
    minutes: Optional[int] = None,
) -> List[CalendarEvent]:
    events: List[CalendarEvent] = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event = cast(Event, component)
            dtstart = event.get("dtstart").dt
            dtend = event.get("dtend").dt

            # Ensure datetime is timezone-aware
            if not isinstance(dtstart, datetime.datetime):
                continue

            # Skip all-day events
            if isinstance(event.get("dtstart").dt, datetime.date) and not isinstance(
                event.get("dtstart").dt, datetime.datetime
            ):
                continue

            now_seconds = now_time.timestamp()
            today_end_seconds = today_end_time.timestamp()
            dtstart_seconds = dtstart.timestamp()
            dtend_seconds = dtend.timestamp()

            if minutes is None:
                if now_seconds <= dtstart_seconds <= today_end_seconds:
                    events.append((dtstart, dtend, event))
            else:
                diff_mins = int((dtstart_seconds - now_seconds) // 60)
                if (
                    0 <= diff_mins <= minutes
                    or dtstart_seconds <= now_seconds <= dtend_seconds
                ):
                    events.append((dtstart, dtend, event))

    events.sort(key=lambda x: x[0])
    return events


def format_event(event: CalendarEvent) -> FormattedEvent:
    dtstart, dtend, comp = event
    summary: str = str(comp.get("summary"))
    attendees = comp.get("attendee", [])
    count: int = (
        len(attendees) if isinstance(attendees, list) else (1 if attendees else 0)
    )
    return dtstart, dtend, summary, count


def main() -> None:
    now: datetime.datetime = datetime.datetime.now(tz=get_localzone())
    end_today: datetime.datetime = now.replace(hour=23, minute=59, second=59)

    cal: Component = load_calendar(ICS_FILE)
    events: List[CalendarEvent] = get_upcoming_events(
        cal, now, end_today, minutes=ALERT_IF_IN_NEXT_MINUTES
    )

    for i, event in enumerate(events):
        dtstart, dtend, summary, attendee_count = format_event(event)

        seconds_until: int = int((dtstart.timestamp() - now.timestamp()))
        minutes_until: int = seconds_until // 60

        if minutes_until < ALERT_IF_IN_NEXT_MINUTES:
            print(
                f"{NERD_FONT_MEETING} {dtstart.strftime('%H:%M')} {summary} ({minutes_until} minutes)"
            )

            # Show popup-like behavior (basic print)
            if (
                ALERT_POPUP_BEFORE_SECONDS
                < seconds_until
                < (ALERT_POPUP_BEFORE_SECONDS + 10)
            ):
                print("\n=== UPCOMING MEETING DETAILS ===")
                print(f"Title: {summary}")
                print(f"Start: {dtstart}")
                print(f"End: {dtend}")
                print(f"Attendees: {attendee_count}")
                print("=" * 32)
            break
    else:
        print(NERD_FONT_FREE)


if __name__ == "__main__":
    main()
