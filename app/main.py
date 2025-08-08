import boto3
from datetime import datetime, time, timedelta
from pytz import timezone, utc
from app.generate_ics import create_ics_from_events
from app.read_excel import read_excel_rows_from_s3

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    input_bucket = 'calendar-input-2025'
    input_key = 'calendar.xlsx'

    output_bucket = 'calendar-web-2025'
    output_key = 'calendars/calendar.ics'


    df = read_excel_rows_from_s3(input_bucket, input_key)

    events = []
    event_time = time(13, 0)
    event_long = timedelta(hours=1)
    timezone_la_paz = timezone('America/La_Paz')

    for i, row in df.iterrows():
        base_date = row['Fecha'].date()
        local_start = timezone_la_paz.localize(datetime.combine(base_date, event_time))
        start_dt = local_start.astimezone(utc)
        end_dt = (local_start + event_long).astimezone(utc)

        event = {
            "uid": f"event-{i}",
            "start": start_dt.strftime("%Y%m%dT%H%M%SZ"),
            "end": end_dt.strftime("%Y%m%dT%H%M%SZ"),
            "summary": f"test event {i}",
            "description": "test description",
            "location": "la paz Bolivia"
        }

        events.append(event)


    ics_content = create_ics_from_events(events)

    with open('/tmp/output.ics', 'w') as f:
        f.write(ics_content)

    s3.upload_file('/tmp/output.ics', output_bucket, output_key)    

    return {
        'status': 'ICS file generated and uploaded',
        'output_url': f'hhtps://{output_bucket}.s3.amazonaws.com/{output_key}',
        'event_count': len(events)
    }