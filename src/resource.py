import datetime
import itertools

from dataclasses import dataclass
from collections.abc import MutableMapping
from typing import Dict, Iterator, List, Union

ORIGIN = datetime.date(2016, 1, 1)  # 2016-1-1 happens to be sunday as well


@dataclass(frozen=True)
class Timing:
    """Represents time period between two time

    Attributes:
        day: Day number (0 for sunday and 6 for saturday)
        start: Start time in iso format HH:[MM:[SS]]
        end: End time in iso format HH:[MM:[SS]]
    """
    day: int
    start: str
    end: str

    @property
    def start_datetime(self):
        """Datetime combining origin date and start time"""
        return datetime.datetime.combine(
            ORIGIN + datetime.timedelta(days=self.day),
            datetime.time.fromisoformat(self.start)
        )

    @property
    def end_datetime(self):
        """Datetime combining origin date and end time"""
        return datetime.datetime.combine(
            ORIGIN + datetime.timedelta(days=self.day),
            datetime.time.fromisoformat(self.end)
        )

    def __eq__(self, o: 'Timing') -> bool:
        return self.start_datetime == o.start_datetime and self.end_datetime == o.end_datetime

    def __gt__(self, o: 'Timing') -> bool:
        return self.start_datetime > o.start_datetime

    def __str__(self):
        return f"Day: {self.day} ({self.start} - {self.end})"


@dataclass(frozen=True)
class Subject:
    """Subject

    Attributes:
        name: Name of subject
    """
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Class:
    """Represents a class room

    Unit class where subjects and teachers are assigned.
    For eg. (Grade 5 Section A) is a class

    Attributes: 
        name: Name of a class
    """
    name: str

    def __str__(self):
        return self.name


@dataclass
class Teacher:
    """Represents a Teacher

    Attributes:
        name: Name of teacher
        availabilities: Available timings for the teacher
            for example, [Timing(1, "10:00", "18:00"), Timing(2, "10:00", "18:00"),]
    """
    name: str
    availabilities: List[Timing]

    def is_available(self, timing: Timing) -> bool:
        """
        Checks whether the teacher is available for givin timing

        Args:
            timing: Timing to check

        Returns:
            True if available else False
        """
        available_timing: Timing

        return any((
            timing.start_datetime >= available_timing.start_datetime and
            timing.end_datetime <= available_timing.end_datetime
        ) for available_timing in self.availabilities)

    def __hash__(self):
        return hash(f"name-{self.name}")

    def __eq__(self, o: 'Teacher') -> bool:
        return hash(self) == hash(o)

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class ClassPeriod:
    """A period assigned to a class

    Attributes: 
        clas: Class object
        period: Timing assigned to the class
    """
    clas: Class
    period: Timing


@dataclass(frozen=True)
class TeacherAssignment:
    """Teacher assigned to subject and class

    Attributes:
        teacher: Teacher instance
        subject: Subject instance
        period_per_week: number of periods per week
    """

    clas: Class
    teacher: Teacher
    subject: Subject
    period_per_week: int

    def __str__(self):
        return f"{self.teacher} - {self.subject}"


class Routine(MutableMapping):
    """Represents routine

    It gets all dictionary like features, plus some additional methods

    Attributes:
        store: wrapped dictionary to object
        teacher_booking: mapping of teacher to assigned timings for that teacher

    """

    def __init__(self, *args, **kwargs) -> None:
        self.store: Dict[ClassPeriod, TeacherAssignment] = {}
        self.teacher_booking: Dict[Teacher, List[Timing]] = {}
        self.store.update(dict(*args, **kwargs))

    def __getitem__(self, key: ClassPeriod) -> Union[TeacherAssignment, None]:
        return self.store[key]

    def __setitem__(self, key: ClassPeriod, value: Union[TeacherAssignment, None]) -> None:
        if value is not None:
            self.teacher_booking[value.teacher] = self.teacher_booking.get(
                value.teacher, []) + [key.period]
        self.store[key] = value

    def __delitem__(self, key: ClassPeriod) -> None:
        assignment: TeacherAssignment = self.store[key]
        if assignment:
            self.teacher_booking.get(assignment.teacher, []).remove(key.period)
        del self.store[key]

    def __iter__(self) -> Iterator:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def get_booked_timings(self, teacher: Teacher) -> List[Timing]:
        """get booked timings of a teacher in this routine

        Args:
            teacher: Teacher instance

        Returns:
            List of Timing assigned to teacher
        """
        return self.teacher_booking.get(teacher, [])

    def console_out(self) -> str:
        """returns string to print on console"""
        daywise: itertools.groupby = itertools.groupby(
            sorted(self.keys(), key=lambda x: x.period.day), key=lambda x: x.period.day)
        output: List[str] = []

        for day, periods_ in daywise:
            periods = list(periods_)
            string = "%-5s |" + ("%-50s\t|" * len(periods))
            output.append(
                (
                    string
                    % tuple(
                        (
                            [str(day)]
                            + [f'{self[period]} [{period}]' for period in periods]
                        )
                    )
                )
            )

        return "\n".join(output)

    def get_json(self) -> List[dict]:
        """Returns JSON serializable routine"""
        classwise: itertools.groupby = itertools.groupby(
            sorted(
                self.keys(), key=lambda x: x.clas.name
            ), key=lambda x: x.clas.name)

        classes: List[dict] = []

        for clas, periods in classwise:
            daywise: itertools.groupby = itertools.groupby(
                sorted(periods, key=lambda x: x.period.day), key=lambda x: x.period.day)

            days: List[dict] = []

            for day, periods_ in daywise:
                days.append({
                    "day": day,
                    **{f"{p.period.start}-{p.period.end}": str(self[p] or '') for p in periods_}
                })

            classes.append({
                "class": clas,
                "days": days,
                "headings": list(map(lambda x: {"field": x, "title": x}, days[0].keys()))
            })

        return classes
