from datetime import datetime

def create_ics_from_events(events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//my calendar//Calendar Feed//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    for event in events:
        lines += [
            "BEGIN:VEVENT",
            f"UID:{event['uid']}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{event['start']}",
            f"DTEND:{event['end']}",
            f"SUMMARY:{event['summary']}",
            f"DESCRIPTION:{event['description']}",
            f"LOCATION:{event['location']}",
            "END:VEVENT"
        ]

    lines.append('END:VCALENDAR') 

    return "\n".join(lines)   
