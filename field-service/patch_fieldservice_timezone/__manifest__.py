# Copyright (C) 2018 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Patch - Field Service Timezones",
    "summary": "patch_fieldservice_timezone module",
    "description": """
This patch fixes the timezone issues in the fieldservice_recurring module.
The issue is that the rruleset doesn't take into account timezone of the user, and so the ruels are based on UTC.
This causes problems with things like weekdays being on the wrong day.
E.g:
- User wants every MONDAY at 1am so creates a recurring order starting from 02/01 (Monday) 1am, with a frequency set that has a frequency of Use Days of Week and Monday checked
- Server time is used which starts the rrule from datetime of 01/01 3pm
- Rrule finds Monday for this start datetime as 02/01 3pm
- When the rule is used to get the date and create the order, 02/01 3pm is saved as the start date
- This displayed in the user's timezone will be 03/01 1am which is TUESDAY

The fix for this issue is to convert the datetime start into the users timezone for getting the rruleset, and then converting back into utc when creating the order.
*** Set OdooBot tz to user's tz for this patch to work ***
    """,
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "category": "Field Service",
    "author": "Inspired Software Pty Ltd",
    "website": "http://www.inspiredsoftware.com.au",
    "depends": ["fieldservice_recurring"],
    "data": [
    ],
    "demo": [
    ],
    "application": False,
    'installable': True,
    'auto_install': True,
}
