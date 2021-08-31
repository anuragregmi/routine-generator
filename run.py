import dataclasses
from typing import List

from src.utils import get_routines
from src.resource import Subject, Teacher, TeacherAssignment, Timing


def main() -> None:
    """Prepare data and call generate_routines"""
    MATH: Subject = Subject("Math")
    ENGLISH: Subject = Subject("English")
    C: Subject = Subject("C")
    DL: Subject = Subject("DL")
    PST: Subject = Subject("PST")
    PHYSICS: Subject = Subject("PHYSICS")
    FIT: Subject = Subject("FIT")

    regular_periods_for_a_day: List[Timing] = [
        Timing(0, "07:00", "08:30"),
        Timing(0, "08:30", "10:00"),
        Timing(0, "11:00", "12:30"),
        Timing(0, "12:30", "14:00"),
    ]

    # college periods for a week
    periods: List[Timing] = [
        dataclasses.replace(period, day=day)
        for period in regular_periods_for_a_day for day in range(0, 7)
    ]

    availabilities: List[Timing] = [
        Timing(day, "07:00", "15:00") for day in range(0, 7)
    ]

    teacher1 = Teacher("Teacher1", availabilities)
    teacher2 = Teacher("Teacher2", availabilities)
    teacher3 = Teacher("Teacher3", availabilities)
    teacher4 = Teacher("Teacher4", availabilities)
    teacher5 = Teacher("Teacher5", availabilities)
    teacher6 = Teacher("Teacher6", availabilities)
    teacher7 = Teacher("Teacher7", availabilities)

    subject_teachers = [
        TeacherAssignment(teacher1, PHYSICS, 4),
        TeacherAssignment(teacher2, ENGLISH, 2),
        TeacherAssignment(teacher3, MATH, 4),
        TeacherAssignment(teacher4, C, 4),
        TeacherAssignment(teacher5, DL, 4),
        TeacherAssignment(teacher6, PST, 3),
        TeacherAssignment(teacher7, FIT, 3)
    ]

    get_routines(periods, subject_teachers)


if __name__ == "__main__":
    main()
