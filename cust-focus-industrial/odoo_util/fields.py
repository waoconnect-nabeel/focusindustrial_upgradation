import calendar
from datetime import date, datetime

import pytz

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import DATE_LENGTH
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


##################################################
#                 Tested on v12                  #
##################################################
# Converts datetime object to a date in the users timezone
def datetime_to_local_date(record, value):
    return fields.Datetime.context_timestamp(record, value).date()
fields.Datetime.datetime_to_tz_date = staticmethod(datetime_to_local_date)


# Convert date object to datetime in users timezone
def date_to_local_datetime(record, value):
    dt = fields.Datetime.context_timestamp(record, fields.Datetime.to_datetime(value))
    return dt.replace(tzinfo=None)
fields.Datetime.date_to_local_datetime = staticmethod(date_to_local_datetime)


##################################################
# WARNING: Needs to be checked and ported to v12 #
##################################################
def datetime_from_string_as_local(record, value):
    if not value:
        return False
    return fields.Datetime.context_timestamp(record, fields.Datetime.from_string(value))
fields.Datetime.from_string_as_local = staticmethod(datetime_from_string_as_local)


def datetime_to_string_local(record, value, local_lang=False, format=False):
    if not value:
        return False

    date_time = datetime_from_string_as_local(record, value)

    if local_lang:
        lang = record.env['ir.qweb.field'].user_lang()
        return date_time.strftime((u"%s %s" % (lang.date_format, lang.time_format)))[:-3]
    elif format:
        return date_time.strftime(format)
    else:
        return fields.Datetime.to_string(date_time)
fields.Datetime.to_string_local = staticmethod(datetime_to_string_local)

# Convert naive datetime object in users timezone to a UTC datetime.
#  eg. 2019/07/02 9am (No tz info) becomes 2019/07/01 11pm (UTC)
# Returns: datetime object
def convert_datetime_to_user_tz(record, d):
    tz_name = record._context.get('tz') or record.env.user.tz
    context_tz = pytz.timezone(tz_name)
    return context_tz.localize(fields.Datetime.to_datetime(d)).astimezone(pytz.utc)
fields.Datetime.convert_datetime_to_user_tz = staticmethod(convert_datetime_to_user_tz)


def datetime_to_string_local_date(record, value, local_lang=False):
    if not value:
        return False

    date = datetime_from_string_as_local(record, value)

    if local_lang:
        lang = record.env['ir.qweb.field'].user_lang()
        return date.strftime((u"%s" % lang.date_format))
    else:
        return fields.Date.to_string(date)
fields.Datetime.to_string_local_date = staticmethod(datetime_to_string_local_date)

# tested on v12
def end_of_month(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])
fields.Date.end_of_month = staticmethod(end_of_month)


def odoo_fields(self):
    return fields
models.Model.odoo_fields = odoo_fields
