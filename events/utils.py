from datetime import timedelta

# from django.contrib.humanize.templatetags import humanize
from django.utils.formats import localize
from django.utils.translation import ungettext as ng, ugettext_lazy as _


def localize_timedelta(delta: timedelta) -> str:
    ret = []
    num_years = int(delta.days / 365)
    if num_years > 0:
        delta -= timedelta(days=num_years * 365)
        ret.append(ng('%d year', '%d years', num_years) % num_years)

    if delta.days > 0:
        ret.append(ng('%d day', '%d days', delta.days) % delta.days)

    num_hours = int(delta.seconds / 3600)
    if num_hours > 0:
        delta -= timedelta(hours=num_hours)
        ret.append(ng('%d hour', '%d hours', num_hours) % num_hours)

    num_minutes = int(delta.seconds / 60)
    if num_minutes > 0:
        delta -= timedelta(minutes=num_minutes)
        ret.append(ng('%d minute', '%d minutes', num_minutes) % num_minutes)

    num_seconds = delta.seconds
    if num_seconds > 0:
        delta -= timedelta(seconds=num_seconds)
        ret.append(ng('%d second', '%d seconds', num_seconds) % num_seconds)

    num_miliseconds = int(delta.microseconds / 1000)
    if num_miliseconds > 0:
        ret.append(ng('%d ms', '%d ms', num_miliseconds) % num_miliseconds)

    if not len(ret):
        ret.append(ng('%d second', '%d seconds', 0) % 0)

    return ' '.join(ret)


def localize_duration(start, end):
    ret = []
    if start.date() == end.date():
        ret.append(localize(start.date()))
        ret.append(_('from %s') % localize(start.time()))
        ret.append(_('to %s') % localize(end.time()))
    else:
        ret.append(_('from %s') % localize(start))
        ret.append(_('to %s') % localize(end))
    return ' '.join(ret)
