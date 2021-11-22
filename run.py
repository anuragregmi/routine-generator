import dataclasses
import json

from typing import List

from src.utils import get_routines
from src.resource import Class, ClassPeriod, Routine, Subject, Teacher, TeacherAssignment, Timing


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

    class_A = Class("A")
    class_B = Class("B")
    class_C = Class("C")
    class_D = Class("D")

    class_periods = (list(map(lambda t: ClassPeriod(class_A, t), periods)) +
                     list(map(lambda t: ClassPeriod(class_B, t), periods)) +
                     list(map(lambda t: ClassPeriod(class_C, t), periods)) +
                     list(map(lambda t: ClassPeriod(class_D, t), periods))
                     )

    subject_teachers = [
        TeacherAssignment(class_A, teacher1, PHYSICS, 4),
        TeacherAssignment(class_A, teacher2, ENGLISH, 2),
        TeacherAssignment(class_A, teacher3, MATH, 4),
        TeacherAssignment(class_A, teacher4, C, 4),
        TeacherAssignment(class_A, teacher5, DL, 4),
        TeacherAssignment(class_A, teacher6, PST, 3),
        TeacherAssignment(class_A, teacher7, FIT, 3),

        TeacherAssignment(class_B, teacher1, PHYSICS, 4),
        TeacherAssignment(class_B, teacher2, ENGLISH, 2),
        TeacherAssignment(class_B, teacher3, MATH, 4),
        TeacherAssignment(class_B, teacher4, C, 4),
        TeacherAssignment(class_B, teacher5, DL, 4),
        TeacherAssignment(class_B, teacher6, PST, 3),
        TeacherAssignment(class_B, teacher7, FIT, 3),

        TeacherAssignment(class_C, teacher1, PHYSICS, 4),
        TeacherAssignment(class_C, teacher2, ENGLISH, 2),
        TeacherAssignment(class_C, teacher3, MATH, 4),
        TeacherAssignment(class_C, teacher4, C, 4),
        TeacherAssignment(class_C, teacher5, DL, 4),
        TeacherAssignment(class_C, teacher6, PST, 3),
        TeacherAssignment(class_C, teacher7, FIT, 3),

        TeacherAssignment(class_D, teacher1, PHYSICS, 4),
        TeacherAssignment(class_D, teacher2, ENGLISH, 2),
        TeacherAssignment(class_D, teacher3, MATH, 4),
        TeacherAssignment(class_D, teacher4, C, 4),
        TeacherAssignment(class_D, teacher5, DL, 4),
        TeacherAssignment(class_D, teacher6, PST, 3),
        TeacherAssignment(class_D, teacher7, FIT, 3),

    ]

    routine: Routine = get_routines(class_periods, subject_teachers)
    if routine:
        with open('routine.json', 'w') as output_file:
            json.dump(routine.get_json(), output_file)


if __name__ == "__main__":
    main()
