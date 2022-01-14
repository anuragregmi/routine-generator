import itertools

from typing import List, Union

from .resource import ClassPeriod, Timing, TeacherAssignment, Routine


class RoutineGenerator:
    def __init__(
        self,
        assignments: List[TeacherAssignment],
        periods: List[ClassPeriod]
    ):
        self.assignments: List[TeacherAssignment] = assignments
        self.periods: List[TeacherAssignment] = periods

        self.routine: Routine = Routine()

    def validate_routine(self) -> bool:
        """Check valitidy of routine

        Perform different levels of quality checks to routine

        Returns:
            True if quality check passes False otherwise
        """

        if not any(self.routine.values()):
            # routine contains no assignments
            return False

        teacher_assignment_group: itertools.groupby = itertools.groupby(
            sorted(self.routine.values(), key=lambda x: x.subject.name if x else ''))
        teacher_assignment: TeacherAssignment
        teacher_assignment_count: dict = dict()

        # compare with input assignments (some assignments may be missing here)
        for teacher_assignment, teacher_assignments in teacher_assignment_group:
            teacher_assignment_count[teacher_assignment] = len(
                list(teacher_assignments))

        return not any(
            map(
                lambda assignment: (
                    teacher_assignment_count.get(
                        assignment
                    ) != assignment.period_per_week
                ),
                self.assignments
            )
        )

    def is_assignment_valid(self, period: ClassPeriod, teacher_assignment: TeacherAssignment) -> bool:
        """Check whether the teacher assignment is valid for given period

        Args:
            period: Timing of period assign teacher to
            teacher_assignment: TeacherAssignment object to assignin

        Retuns:
            True if assignment is valid False otherwise
        """
        teachers_booked_timings: List[Timing] = self.routine.get_booked_timings(
            teacher_assignment.teacher)

        # assignment for that day
        booked_assignment_days: List[TeacherAssignment] = [
            assignment for class_period, assignment in self.routine.items() if (
                class_period.period.day == period.period.day and class_period.clas == period.clas
            )
        ]

        teacher_assignments: List[TeacherAssignment] = [
            assignment for assignment in self.routine.values() if assignment == teacher_assignment
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
        self, period_index: int = 0,
    ) -> bool:
        """Generates routine recursively

        Args: 
            period_index: index of period in periods

        Returns:
            True if routine was generated successfully False otherwise
            Output is stored in self.routine


        """

        if period_index == len(self.periods):
            return self.validate_routine()

        period = self.periods[period_index]

        assignments_for_that_class = [
            assignment for assignment in self.assignments if assignment.clas == period.clas
        ]

        for assignment in assignments_for_that_class + [None]:
            if (assignment is None) or self.is_assignment_valid(period, assignment):
                self.routine[period] = assignment

                if self.generate_routine(period_index + 1):
                    return True
                else:
                    del self.routine[period]

        return False


def get_routines(
    periods: List[ClassPeriod],
    assignments: List[TeacherAssignment]
) -> Union[Routine, None]:
    """Generate routine and print it

    Args:
        periods: List of ClassPeriods to assign
        assignments: List of TeacherAssignment instances to chose from
    """
    generator = RoutineGenerator(assignments, periods)

    if generator.generate_routine():
        return generator.routine
    else:
        return None
