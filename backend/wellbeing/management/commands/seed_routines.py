from django.core.management.base import BaseCommand

from wellbeing.models import Routine, RoutineStep


class Command(BaseCommand):
    help = "Creates the default FocusFlow routines"

    def handle(self, *args, **options):

        routines = [
            {
                "title": "Gentle Morning Start",
                "description": "A simple morning routine for days when energy is low and getting started feels difficult.",
                "mode": "recovery",
                "routine_type": "morning",
                "steps": [
                    {
                        "title": "Sit up and drink some water",
                        "description": "Start with one small action. You do not need to think about the whole morning yet.",
                        "duration_minutes": 2,
                    },
                    {
                        "title": "Wash face and brush teeth",
                        "description": "Keep this simple. The goal is to feel a little more awake.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Get dressed",
                        "description": "Choose something comfortable rather than spending too long deciding what to wear.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Eat something",
                        "description": "Have a simple breakfast or snack before moving on with the day.",
                        "duration_minutes": 10,
                    },
                ],
            },
            {
                "title": "Steady Morning Routine",
                "description": "A structured morning routine for days when energy and focus are fairly steady.",
                "mode": "steady",
                "routine_type": "morning",
                "steps": [
                    {
                        "title": "Get up and open the curtains",
                        "description": "Bring some light into the room and start the day.",
                        "duration_minutes": 2,
                    },
                    {
                        "title": "Wash and get dressed",
                        "description": "Complete your basic morning hygiene and get ready.",
                        "duration_minutes": 10,
                    },
                    {
                        "title": "Have breakfast",
                        "description": "Eat something before starting your main tasks.",
                        "duration_minutes": 15,
                    },
                    {
                        "title": "Check today's priorities",
                        "description": "Look at your tasks and identify what matters most today.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Focused Study Start",
                "description": "A short study routine to make starting work feel more manageable.",
                "mode": "balanced",
                "routine_type": "study",
                "steps": [
                    {
                        "title": "Choose one task",
                        "description": "Pick one specific piece of work to start with rather than thinking about everything at once.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Clear your study space",
                        "description": "Remove anything that is likely to distract you and keep only what you need.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Open the materials you need",
                        "description": "Open the document, lecture, website or code you need for the task.",
                        "duration_minutes": 2,
                    },
                    {
                        "title": "Start with the smallest action",
                        "description": "Do the first small action that moves the task forward.",
                        "duration_minutes": 10,
                    },
                ],
            },
            {
                "title": "Low Energy Study Routine",
                "description": "A lighter study routine for days when concentration is difficult.",
                "mode": "low_energy",
                "routine_type": "study",
                "steps": [
                    {
                        "title": "Choose something small",
                        "description": "Pick a task that feels possible with the energy you have today.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Prepare only what you need",
                        "description": "Get the minimum materials needed to begin.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Work on one small part",
                        "description": "Focus only on the next small part rather than finishing the whole task.",
                        "duration_minutes": 10,
                    },
                    {
                        "title": "Decide what happens next",
                        "description": "Choose whether to continue, take a break or leave yourself a clear starting point for later.",
                        "duration_minutes": 2,
                    },
                ],
            },
            {
                "title": "Progress Study Session",
                "description": "A study routine for days when you have enough energy to make strong progress.",
                "mode": "progress",
                "routine_type": "study",
                "steps": [
                    {
                        "title": "Choose your main priority",
                        "description": "Select the most important study task for the session.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Break it into sections",
                        "description": "Identify the next few clear pieces of work.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Work without switching tasks",
                        "description": "Stay with the chosen task rather than moving between different pieces of work.",
                        "duration_minutes": 25,
                    },
                    {
                        "title": "Review your progress",
                        "description": "Check what you completed and decide the next step.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Quick Room Reset",
                "description": "A short cleaning routine for making a room feel more manageable.",
                "mode": "steady",
                "routine_type": "cleaning",
                "steps": [
                    {
                        "title": "Collect rubbish",
                        "description": "Pick up obvious rubbish first.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Collect things that belong elsewhere",
                        "description": "Put items that need moving into one place rather than walking around repeatedly.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Clear one surface",
                        "description": "Choose one visible surface and clear it.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Put away what you can",
                        "description": "Return the collected items to their homes.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Low Energy Cleaning Reset",
                "description": "A minimal cleaning routine for days when there is not much energy available.",
                "mode": "low_energy",
                "routine_type": "cleaning",
                "steps": [
                    {
                        "title": "Pick up rubbish",
                        "description": "Only focus on obvious rubbish.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Put dirty dishes together",
                        "description": "Collect cups, plates and other dishes in one place.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Clear one small area",
                        "description": "Choose one surface or small space. Stop after that if needed.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Simple Cooking Routine",
                "description": "A step-by-step routine for making cooking feel less overwhelming.",
                "mode": "balanced",
                "routine_type": "cooking",
                "steps": [
                    {
                        "title": "Decide what you are making",
                        "description": "Choose the meal before starting to take ingredients out.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Get ingredients together",
                        "description": "Put the ingredients you need in one place.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Prepare ingredients",
                        "description": "Wash, chop or measure what you need before cooking.",
                        "duration_minutes": 10,
                    },
                    {
                        "title": "Cook the meal",
                        "description": "Follow the recipe or your usual method one step at a time.",
                        "duration_minutes": 20,
                    },
                    {
                        "title": "Do a small clean-up",
                        "description": "Put away ingredients and clear the main preparation area.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Easy Meal Routine",
                "description": "A low-energy routine for getting something to eat without making cooking into a large task.",
                "mode": "low_energy",
                "routine_type": "cooking",
                "steps": [
                    {
                        "title": "Choose the easiest suitable meal",
                        "description": "Pick something simple rather than trying to make the perfect meal.",
                        "duration_minutes": 2,
                    },
                    {
                        "title": "Get everything together",
                        "description": "Bring the ingredients and equipment you need to one place.",
                        "duration_minutes": 3,
                    },
                    {
                        "title": "Prepare the meal",
                        "description": "Keep the preparation as simple as possible.",
                        "duration_minutes": 10,
                    },
                    {
                        "title": "Put the main things away",
                        "description": "Do only the essential clean-up afterwards.",
                        "duration_minutes": 5,
                    },
                ],
            },
            {
                "title": "Gentle Evening Wind Down",
                "description": "A calm evening routine to help close the day and make tomorrow easier.",
                "mode": "recovery",
                "routine_type": "evening",
                "steps": [
                    {
                        "title": "Put away the essentials",
                        "description": "Put away only the things that would make tomorrow morning harder.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Prepare something for tomorrow",
                        "description": "Choose one helpful thing, such as clothes, your bag or breakfast.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Wash and get comfortable",
                        "description": "Complete your basic evening hygiene and change into comfortable clothes.",
                        "duration_minutes": 10,
                    },
                    {
                        "title": "Switch to something calming",
                        "description": "Choose a quiet activity that helps you move away from work and tasks.",
                        "duration_minutes": 15,
                    },
                ],
            },
            {
                "title": "Evening Reset",
                "description": "A short routine for closing the day and preparing for tomorrow.",
                "mode": "steady",
                "routine_type": "evening",
                "steps": [
                    {
                        "title": "Check tomorrow",
                        "description": "Look at tomorrow's main commitments and tasks.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Prepare clothes and essentials",
                        "description": "Put together anything you need for the morning.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Quick tidy",
                        "description": "Clear the most visible clutter without starting a full cleaning session.",
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Get ready for bed",
                        "description": "Complete your evening hygiene and begin winding down.",
                        "duration_minutes": 10,
                    },
                ],
            },
        ]

        created_count = 0
        updated_count = 0

        for routine_data in routines:
            steps = routine_data.pop("steps")

            routine, created = Routine.objects.update_or_create(
                title=routine_data["title"],
                created_by=None,
                defaults={
                    "description": routine_data["description"],
                    "mode": routine_data["mode"],
                    "routine_type": routine_data["routine_type"],
                    "active": True,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            # Recreate the steps so rerunning the command
            # does not create duplicate steps.
            routine.steps.all().delete()

            for order, step in enumerate(steps, start=1):
                RoutineStep.objects.create(
                    routine=routine,
                    title=step["title"],
                    description=step["description"],
                    duration_minutes=step["duration_minutes"],
                    order=order,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {len(routines)} routines "
                f"({created_count} created, {updated_count} updated)."
            )
        )