import itertools

from typing import List

from .resource import ClassPeriod, Timing, TeacherAssignment, Routine


def validate_routine(routine: Routine) -> bool:
    """Check valitidy of routine

    Perform different levels of quality checks to routine

    Args:
        routine: Routine instance

    Returns:
        True if quality check passes False otherwise
    """

    if not any(routine.values()):
        # routine contains no assignments
        return False

    teacher_assignment_group: itertools.groupby = itertools.groupby(
        sorted(routine.values(), key=lambda x: x.subject.name if x else ''))
    teacher_assignment: TeacherAssignment

    # compare with input assignments (some assignments may be missing here)
    for teacher_assignment, teacher_assignments in teacher_assignment_group:
        if teacher_assignment and len(list(teacher_assignments)) != teacher_assignment.period_per_week:
            return False
    return True


def is_assignment_valid(period: ClassPeriod, teacher_assignment: TeacherAssignment, routine: Routine) -> bool:
    """Check whether the teacher assignment is valid for given period

    Args:
        period: Timing of period assign teacher to
        teacher_assignment: TeacherAssignment object to assignin
        routine: Reference of existing routine instance

    Retuns:
        True if assignment is valid False otherwise
    """
    teachers_booked_timings: List[Timing] = routine.get_booked_timings(
        teacher_assignment.teacher)

    # assignment for that day
    booked_assignment_days: List[TeacherAssignment] = [
        assignment for class_period, assignment in routine.items() if (
            class_period.period.day == period.period.day and class_period.clas == period.clas
        )
    ]

    teacher_assignments: List[TeacherAssignment] = [
        assignment for assignment in routine.values() if assignment == teacher_assignment
    ]

    if len(teacher_assignments) >= teacher_assignment.period_per_week:
        return False

    if not teacher_assignment.teacher.is_available(period.period):
        # not available for teacher's shift
        False

    if teacher_assignment in booked_assignment_days:
        # There is one period of this subject already in same day
        return False

    if period.period in teachers_booked_timings:
        # Teacher is booked for that timing
        return False

    return True


def generate_routine(
    routine: Routine, period_index: int,
    assignments: List[TeacherAssignment],
    periods: List[ClassPeriod]
) -> bool:
    """Generates routine recursively

    Args: 
        routine: Routine instance to store result
        period_index: index of period in periods
        assignments: List of TeacherAssignment instances to chose from
        periods: List of timings to assign

    Returns:
        True if routine was generated successfully False otherwise

    """
    if period_index == len(periods):
        return validate_routine(routine)

    period = periods[period_index]

    assignments_for_that_class = [
        assignment for assignment in assignments if assignment.clas == period.clas
    ]

    for assignment in assignments_for_that_class + [None]:

        if (assignment is None) or is_assignment_valid(period, assignment, routine):
            routine[period] = assignment

            if generate_routine(routine, period_index + 1, assignments, periods):
                return True
    return False


def get_routines(periods: List[ClassPeriod], assignments: List[TeacherAssignment]) -> None:
    """Generate routine and print it

    Args:
        periods: List of ClassPeriods to assign
        assignments: List of TeacherAssignment instances to chose from
    """

    routine: Routine = Routine()

    if generate_routine(routine, 0, assignments, periods):
        print(routine)
    else:
        print("no solutions found")
