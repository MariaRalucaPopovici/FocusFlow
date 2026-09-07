from django.core.management.base import BaseCommand
from wellbeing.models import Strategy

# Fills in short_tip on strategies that already exist (matched by title).
SHORT_TIP_UPDATES = [
    {"title": "The 2-Minute Start", "short_tip": "Commit to just 2 minutes to get started"},
    {"title": "Make It Smaller: Turn an Overwhelming Task Into Tiny Steps", "short_tip": "Turn a big task into one small, specific step"},
    {"title": "Body Doubling", "short_tip": "Work alongside someone else, in person or on a call"},
    {"title": "Save Distractions for the Break", "short_tip": "Jot down stray thoughts, deal with them on your break"},
    {"title": "Time Blocking", "short_tip": "Give every task its own slot in your calendar"},
    {"title": "Urgent vs Important", "short_tip": "Do what's urgent and important first"},
    {"title": "Brain Dump", "short_tip": "Write down everything on your mind to clear space"},
    {"title": "The Drop Zone", "short_tip": "One spot for keys, wallet, letters - not just anywhere"},
]

# New strategies, sourced from the two uploaded PDFs.
NEW_STRATEGIES = [
    {
        "title": "Guided Meditation Apps",
        "description": "Apps like Headspace, Calm, and Insight Timer offer short guided meditations to quiet your mind and improve concentration - even five minutes can help you reset before starting work.",
        "short_tip": "Try a 5-min guided meditation to reset your focus",
        "category": "recovery",
        "energy_level": "any",
        "duration_minutes": 5,
        "resource_url": "https://www.headspace.com",
        "active": True,
    },
    {
        "title": "Background Noise for Focus (myNoise)",
        "description": "mynoise.net lets you mix ambient sounds - rain, cafe chatter, white noise - to mask distractions and help you settle into focus.",
        "short_tip": "Mix background sounds to mask distractions",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://mynoise.net",
        "active": True,
    },
    {
        "title": "Focusmate: Virtual Body Doubling",
        "description": "Focusmate pairs you with a stranger over video for a scheduled work session. You don't have to talk - just both being visible and accountable is often enough to get started.",
        "short_tip": "Book a virtual co-working session with a stranger",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://www.focusmate.com",
        "active": True,
    },
    {
        "title": "HabitShare: Track Habits With a Friend",
        "description": "HabitShare lets you track daily habits and share your progress with a friend for accountability, turning habit-building into something visible instead of invisible.",
        "short_tip": "Track a habit and share progress with a friend",
        "category": "organisation",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://habitshareapp.com",
        "active": True,
    },
    {
        "title": "Flora: Gamify Your Focus",
        "description": "Flora plants a virtual tree when you start a focus session - if you leave the app before time's up, the tree dies. A small, gentle incentive to stay on task.",
        "short_tip": "Plant a virtual tree that dies if you get distracted",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://flora.appfinca.com",
        "active": True,
    },
    {
        "title": "Monotasking",
        "description": "Do one thing at a time. Switching between tasks costs you more focus than it feels like - picking a single task and sticking with it for a set period reduces mental noise.",
        "short_tip": "Do one thing at a time, nothing else",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Don't Put Down, Put Away",
        "description": "When you pick something up, put it back in its home (or the drop zone) rather than setting it down somewhere temporary. It takes the same effort now and saves a bigger tidy-up later.",
        "short_tip": "Put items back in their home, not just down",
        "category": "routine",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Write Everything Down",
        "description": "Don't rely on memory for appointments, ideas, or things to do. Write them down immediately - on your phone, in a notebook, wherever you'll actually look again.",
        "short_tip": "Write it down immediately, don't trust memory",
        "category": "organisation",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "'Ey, Might As Well'",
        "description": "Once you've done one small thing, use momentum: 'ey, might as well do this other small thing too'. Starting is the hardest part - each small win makes the next one easier.",
        "short_tip": "Use momentum: one small task leads to the next",
        "category": "starting",
        "energy_level": "low",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Add Spice to Boring Tasks",
        "description": "If an important task isn't stimulating anymore, make it more fun - turn it into a game, add music, or plan to tell a friend the interesting bits you learn along the way.",
        "short_tip": "Make a boring task more fun or stimulating",
        "category": "starting",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
        {
        "title": "FlowSavvy: Auto-Scheduling Calendar",
        "description": "FlowSavvy is a free calendar app that holds both fixed events (lectures, appointments) and flexible tasks, then automatically time-blocks your tasks around your events based on priority and due date. Tasks can repeat, and you can personalise with tags and colours.",
        "short_tip": "Let a calendar app auto-schedule your tasks around events",
        "category": "organisation",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://flowsavvy.app",
        "active": True,
    },
    {
        "title": "Forest: Stay Off Your Phone",
        "description": "Forest plants a virtual tree whenever you start a focus session; leave the app to check your phone and the tree dies. A visual, gamified way to resist the pull of your phone while you work.",
        "short_tip": "Plant a tree that dies if you check your phone",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://forestapp.cc",
        "active": True,
    },
        {
        "title": "Talk Yourself Through It",
        "description": "Say out loud what you're doing as you do it - e.g. 'coffee, coffee, coffee' on the way to make one. It sounds silly, but it keeps ADHD brains anchored to the task instead of drifting off mid-action.",
        "short_tip": "Say what you're doing out loud to stay on track",
        "category": "starting",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Photograph It",
        "description": "Take a photo or screenshot instead of trying to remember something - a parking spot, a receipt, a whiteboard note. Digital memory is more reliable than working memory on a bad day.",
        "short_tip": "Snap a photo instead of trying to remember",
        "category": "organisation",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Start With the Easy Bit",
        "description": "Do the easiest part of your to-do list first. Initiating anything is the hardest part - an early win makes your brain more willing to tackle the harder task next.",
        "short_tip": "Do the easiest task first to build momentum",
        "category": "starting",
        "energy_level": "low",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Know Your Best Focus Hours",
        "description": "Notice when you naturally focus best and plan demanding work for then. If you have a predictable slump (e.g. mid-afternoon), use that time for admin or a walk instead of fighting it.",
        "short_tip": "Schedule hard tasks for your natural focus hours",
        "category": "organisation",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Pre-Work Ritual",
        "description": "Build a short, repeatable routine before you start work - set up your space, make a drink, put on a specific playlist, reply to anything urgent first. The ritual itself signals to your brain that focus time is starting.",
        "short_tip": "Build a short ritual that signals focus time is starting",
        "category": "starting",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Eliminate Distractions First",
        "description": "Before you start, clear your desk, block notifications, and find a quiet space. Removing distractions in advance means you don't have to rely on willpower once you're already working.",
        "short_tip": "Clear your desk and block notifications before starting",
        "category": "focus",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
    {
        "title": "Habit Stacking",
        "description": "Attach a new habit to one you already do automatically - e.g. 'after I pour my coffee, I check my to-do list'. Anchoring a new habit to an existing one makes it far more likely to stick.",
        "short_tip": "Attach a new habit to one you already do automatically",
        "category": "routine",
        "energy_level": "any",
        "duration_minutes": None,
        "resource_url": "https://jamesclear.com/habit-stacking",
        "active": True,
    },
    {
        "title": "Tidy Section by Section",
        "description": "Break tidying into small sections rather than 'clean the room'. Tick each section off your to-do list as you finish it - the small wins add up and stop the task from feeling endless.",
        "short_tip": "Break tidying into small sections, tick each one off",
        "category": "routine",
        "energy_level": "low",
        "duration_minutes": None,
        "resource_url": "",
        "active": True,
    },
]


class Command(BaseCommand):
    help = "Fills in short_tip on existing strategies and adds new strategies sourced from research PDFs."

    def handle(self, *args, **options):
        updated = 0
        for data in SHORT_TIP_UPDATES:
            count = Strategy.objects.filter(title=data["title"]).update(short_tip=data["short_tip"])
            updated += count

        created = 0
        for data in NEW_STRATEGIES:
            title = data["title"]
            obj, was_created = Strategy.objects.update_or_create(
                title=title,
                defaults=data,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Updated short_tip on {updated} existing strategies."))
        self.stdout.write(self.style.SUCCESS(f"Processed {len(NEW_STRATEGIES)} new strategies ({created} newly created, rest already existed)."))