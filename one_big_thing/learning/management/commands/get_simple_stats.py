from django.core.management import BaseCommand

from one_big_thing.learning.api_views import get_learning_breakdown_data


class Command(BaseCommand):
    help = "Print summed stats from the data breakdown API"

    def handle(self, *args, **kwargs):
        signups = get_learning_breakdown_data()
        number_of_sign_ups = sum([a["number_of_sign_ups"] for a in signups])
        completed_first_evaluation = sum([a["completed_first_evaluation"] for a in signups])
        completed_second_evaluation = sum([a["completed_second_evaluation"] for a in signups])
        completed_1_hours_of_learning = sum([a["completed_1_hours_of_learning"] for a in signups])
        completed_2_hours_of_learning = sum([a["completed_2_hours_of_learning"] for a in signups])
        completed_3_hours_of_learning = sum([a["completed_3_hours_of_learning"] for a in signups])
        completed_4_hours_of_learning = sum([a["completed_4_hours_of_learning"] for a in signups])
        completed_5_hours_of_learning = sum([a["completed_5_hours_of_learning"] for a in signups])
        completed_6_hours_of_learning = sum([a["completed_6_hours_of_learning"] for a in signups])
        completed_7_plus_hours_of_learning = sum([a["completed_7_plus_hours_of_learning"] for a in signups])
        total_time_completed = sum([a["total_time_completed"] for a in signups])
        number_of_completed_sign_ups = sum(
            [1 if a["grade"] and a["profession"] and a["department"] else 0 for a in signups]
        )
        self.stdout.write(f"number_of_sign_ups: {number_of_sign_ups}")
        self.stdout.write(f"completed_first_evaluation: {completed_first_evaluation}")
        self.stdout.write(f"completed_second_evaluation: {completed_second_evaluation}")
        self.stdout.write(f"completed_1_hours_of_learning: {completed_1_hours_of_learning}")
        self.stdout.write(f"completed_2_hours_of_learning: {completed_2_hours_of_learning}")
        self.stdout.write(f"completed_3_hours_of_learning: {completed_3_hours_of_learning}")
        self.stdout.write(f"completed_4_hours_of_learning: {completed_4_hours_of_learning}")
        self.stdout.write(f"completed_5_hours_of_learning: {completed_5_hours_of_learning}")
        self.stdout.write(f"completed_6_hours_of_learning: {completed_6_hours_of_learning}")
        self.stdout.write(f"completed_7_plus_hours_of_learning: {completed_7_plus_hours_of_learning}")
        self.stdout.write(f"total_time_completed: {total_time_completed}")
        self.stdout.write(f"number_of_completed_sign_ups: {number_of_completed_sign_ups}")
