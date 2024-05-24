from django.db import models
import json

# Create your models here.


class Chat(models.Model):
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username}: {self.message}"


class Scenario(models.Model):
    scenario = models.TextField()

    def __str__(self):
        return self.scenario


class Role(models.Model):
    scenario = models.ForeignKey(
        Scenario, related_name="role", on_delete=models.CASCADE
    )
    role = models.TextField()

    def __str__(self):
        return self.role


class Context(models.Model):
    scenario = models.ForeignKey(
        Scenario, related_name="context", on_delete=models.CASCADE
    )
    context = models.TextField()

    def __str__(self):
        return self.context


class Personality(models.Model):
    scenario = models.ForeignKey(
        Scenario, related_name="personality", on_delete=models.CASCADE
    )
    personality = models.TextField()

    def __str__(self):
        return self.personality


class Reminders(models.Model):
    scenario = models.ForeignKey(
        Scenario, related_name="reminders", on_delete=models.CASCADE
    )
    reminder = models.TextField()

    def __str__(self):
        return self.reminder


# A Scenario has one FeedbackRubric.
# A FeedbackRubric has many Objectives.
# Objective, GoodBehavior, and BadBehavior Models:

# An Objective belongs to a FeedbackRubric.
# Each Objective has many GoodBehavior and BadBehavior.


class FeedbackRubric(models.Model):
    scenario = models.OneToOneField(
        Scenario, related_name="feedback_rubric", on_delete=models.CASCADE
    )

    def to_json(self):
        objectives = self.objectives.all()
        rubric = []
        for obj in objectives:
            rubric.append(
                {
                    "objective": obj.objective,
                    "Good behaviors": [
                        gb.good_behavior for gb in obj.good_behaviors.all()
                    ],
                    "Areas to improve": [
                        bb.bad_behavior for bb in obj.bad_behaviors.all()
                    ],
                }
            )
        return json.dumps(rubric)


class Objective(models.Model):
    feedback_rubric = models.ForeignKey(
        FeedbackRubric, related_name="objectives", on_delete=models.CASCADE
    )
    objective = models.TextField()


class GoodBehavior(models.Model):
    objective = models.ForeignKey(
        Objective, related_name="good_behaviors", on_delete=models.CASCADE
    )
    good_behavior = models.TextField()


class BadBehavior(models.Model):
    objective = models.ForeignKey(
        Objective, related_name="bad_behaviors", on_delete=models.CASCADE
    )
    bad_behavior = models.TextField()
