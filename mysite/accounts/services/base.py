from collections import namedtuple
from datetime import date, datetime, timedelta
from typing import List

from django.db.models import QuerySet


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ChartStatistic:
    Chart = namedtuple('Chart', 'labels values')

    def __init__(self, queryset: QuerySet, date_field_name: str, start: date, end: date):
        self._queryset = queryset
        self.field = date_field_name

        now = datetime.now().date()
        if start > now or end > now or start > end:
            raise ValueError()

        self._start = start
        self._end = end

    def set_period(self, start, end):
        self._start = start
        self._end = end

    def create(self) -> Chart:
        return self.Chart(self._format_dates(self.dates), self.values)

    def _format_dates(self, dates: List[date]) -> List[str]:
        return [f"{date.day}.{date.month}" for date in dates]

    @property
    def dates(self) -> List[date]:
        return [self._start + timedelta(days=i) for i in range((self._end - self._start).days + 1)]

    @property
    def values(self) -> List[float]:
        # if self._queryset.model == Post:
        return [
            self._queryset.filter(**{self.field + "__date": date}).count()
            for date in self.dates
        ]
        # elif self._queryset.model == Comment and self.field == "count":
        #     return self._queryset.count()
