#!/usr/bin/env python3
import json
import os
import random
import sys
import textwrap
from datetime import date, datetime, timedelta
from pathlib import Path

APP_DIR = Path.home() / ".reading_terminal"
APP_DIR.mkdir(exist_ok=True)
PROGRESS_FILE = APP_DIR / "progress.json"
PARENT_PIN = os.getenv("READING_PARENT_PIN", "")

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
MAGENTA = "\033[95m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"
WHITE = "\033[97m"
BLACK = "\033[30m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_BLUE = "\033[38;5;75m"
BRIGHT_CYAN = "\033[38;5;51m"
BRIGHT_GREEN = "\033[38;5;82m"
BRIGHT_YELLOW = "\033[38;5;226m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;213m"
PURPLE = "\033[38;5;141m"
LIME = "\033[38;5;118m"
TEAL = "\033[38;5;44m"
GRAY = "\033[38;5;245m"
BG_BLUE = "\033[48;5;24m"
BG_GREEN = "\033[48;5;22m"
BG_RED = "\033[48;5;52m"
BG_PURPLE = "\033[48;5;54m"

WIDTH = 68

SIGHT_WORDS = [
    "the", "and", "you", "is", "it", "in", "we", "can", "see", "my",
    "I", "a", "to", "go", "like", "look", "me", "up", "at", "on",
    "he", "she", "dog", "cat", "run", "red", "big", "little", "play", "book",
]

LESSONS = [
    {"sentence": "The dog can run.", "question": "What can the dog do?", "choices": ["Run", "Read", "Cook"], "answer": 0, "focus": ["run"]},
    {"sentence": "I see a red cat.", "question": "What color is the cat?", "choices": ["Red", "Blue", "Green"], "answer": 0, "focus": ["red"]},
    {"sentence": "We go to the park.", "question": "Where do we go?", "choices": ["The park", "The moon", "The store"], "answer": 0, "focus": ["park"]},
    {"sentence": "Mom has a blue cup.", "question": "What does Mom have?", "choices": ["A cup", "A hat", "A ball"], "answer": 0, "focus": ["cup"]},
    {"sentence": "The fish can swim.", "question": "What can the fish do?", "choices": ["Swim", "Jump", "Sing"], "answer": 0, "focus": ["swim"]},
    {"sentence": "Dad can help me.", "question": "Who can help?", "choices": ["Dad", "The cat", "The fish"], "answer": 0, "focus": ["help"]},
    {"sentence": "The sun is hot.", "question": "What is hot?", "choices": ["The sun", "The bed", "The book"], "answer": 0, "focus": ["sun"]},
    {"sentence": "I like my book.", "question": "What do I like?", "choices": ["My book", "My shoe", "My cup"], "answer": 0, "focus": ["book"]},
    {"sentence": "The bird is in a tree.", "question": "Where is the bird?", "choices": ["In a tree", "In a car", "In a box"], "answer": 0, "focus": ["tree"]},
    {"sentence": "The frog can hop.", "question": "What can the frog do?", "choices": ["Hop", "Read", "Bake"], "answer": 0, "focus": ["hop"]},
    {"sentence": "Ben has a big ball.", "question": "What does Ben have?", "choices": ["A ball", "A fish", "A pen"], "answer": 0, "focus": ["ball"]},
    {"sentence": "I can see the moon.", "question": "What can I see?", "choices": ["The moon", "A dog", "A cup"], "answer": 0, "focus": ["moon"]},
]

BUILD_SENTENCES = [
    ["I", "see", "a", "cat."],
    ["The", "dog", "can", "run."],
    ["We", "like", "the", "park."],
    ["Mom", "has", "a", "cup."],
    ["Dad", "can", "help", "me."],
    ["The", "sun", "is", "hot."],
    ["I", "like", "my", "book."],
    ["The", "fish", "can", "swim."],
]

FILL_SENTENCES = [
    ("The dog can ___.", ["run", "cup", "red"], "run"),
    ("I see a ___ cat.", ["red", "swim", "book"], "red"),
    ("The fish can ___.", ["swim", "hat", "big"], "swim"),
    ("We go to the ___.", ["park", "cup", "sun"], "park"),
    ("I like my ___.", ["book", "run", "hot"], "book"),
    ("The sun is ___.", ["hot", "dog", "go"], "hot"),
    ("Mom has a ___.", ["cup", "run", "red"], "cup"),
    ("The frog can ___.", ["hop", "book", "blue"], "hop"),
]

TYPE_WORDS = [
    "cat", "dog", "run", "red", "big", "book", "park", "fish",
    "sun", "mom", "dad", "help", "play", "look", "hop", "cup",
]

COPY_SENTENCES = [
    "I see a cat.",
    "The dog can run.",
    "We like the park.",
    "Mom has a cup.",
    "Dad can help me.",
    "The sun is hot.",
    "I like my book.",
    "The fish can swim.",
]

FIX_SENTENCES = [
    ("i see a cat", "I see a cat."),
    ("the dog can run", "The dog can run."),
    ("we like the park", "We like the park."),
    ("mom has a cup", "Mom has a cup."),
    ("dad can help me", "Dad can help me."),
    ("the sun is hot", "The sun is hot."),
]

VOCAB = [
    ("tiny", "very small", ["very small", "very loud", "very wet"]),
    ("glad", "happy", ["happy", "cold", "slow"]),
    ("quick", "fast", ["fast", "sad", "blue"]),
    ("huge", "very big", ["very big", "very small", "very soft"]),
    ("quiet", "not loud", ["not loud", "very hot", "very fast"]),
]

WORD_FAMILIES = [
    ("-at", ["cat", "hat", "bat"]),
    ("-un", ["sun", "run", "fun"]),
    ("-op", ["hop", "mop", "top"]),
    ("-ig", ["big", "pig", "wig"]),
]

PASSAGES = [
    {
        "title": "The Red Ball",
        "text": "Sam has a red ball. He can toss it.",
        "questions": [("What color is the ball?", ["Red", "Blue", "Green"], "Red")],
    },
    {
        "title": "The Cat",
        "text": "The cat is on the bed. It is soft.",
        "questions": [("Where is the cat?", ["On the bed", "In a tree", "In a car"], "On the bed")],
    },
    {
        "title": "At the Park",
        "text": "Mia is at the park. She can run and play.",
        "questions": [("Where is Mia?", ["At the park", "At school", "At the store"], "At the park")],
    },
]

ACTIVITY_NAMES = {
    "sight_words": "Sight words",
    "read_sentence": "Read + prove it",
    "comprehension": "Reading question",
    "word_family": "Word family",
    "type_words": "Spelling",
    "missing_word": "Missing word",
    "copy_sentence": "Copy a sentence",
    "fix_sentence": "Type a sentence",
    "build_sentence": "Build a sentence",
    "vocabulary": "Vocabulary",
    "passage": "Short passage",
}

DEFAULT_PROGRESS = {
    "version": 4,
    "stars": 0,
    "sentences_read": 0,
    "questions_correct": 0,
    "questions_total": 0,
    "best_streak": 0,
    "daily_streak": 0,
    "last_completed_date": None,
    "days_completed": 0,
    "total_attempts": 0,
    "corrections": 0,
    "skills": {},
    "word_mastery": {},
    "daily_plan": None,
}


def load_progress():
    try:
        existing = json.loads(PROGRESS_FILE.read_text())
        progress = {**DEFAULT_PROGRESS, **existing}
        progress.setdefault("skills", {})
        progress.setdefault("word_mastery", {})
        return progress
    except Exception:
        return dict(DEFAULT_PROGRESS)


def save_progress(progress):
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress, indent=2, sort_keys=True))
    tmp.replace(PROGRESS_FILE)


def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.getenv("TERM"):
        os.system("clear")
    else:
        print("\n" * 2)


def colorize(text, color):
    return f"{color}{text}{RESET}"


def divider(char="━", color=BRIGHT_CYAN):
    print(color + char * WIDTH + RESET)


def rainbow_text(text):
    colors = [BRIGHT_CYAN, PURPLE, PINK, ORANGE, BRIGHT_YELLOW, LIME, BRIGHT_GREEN]
    out = []
    ci = 0
    for ch in text:
        if ch == " ":
            out.append(ch)
        else:
            out.append(colors[ci % len(colors)] + ch)
            ci += 1
    return BOLD + "".join(out) + RESET


def box(lines, *, border=BRIGHT_CYAN, title_text=None, width=WIDTH):
    inner = width - 4
    print(border + "╭" + "─" * (width - 2) + "╮" + RESET)
    if title_text:
        label = f" {title_text} "
        print(border + "│" + RESET + BOLD + label.center(width - 2) + RESET + border + "│" + RESET)
        print(border + "├" + "─" * (width - 2) + "┤" + RESET)
    for raw in lines:
        plain = str(raw)
        for chunk in textwrap.wrap(plain, width=inner) or [""]:
            print(border + "│ " + RESET + chunk.ljust(inner) + " " + border + "│" + RESET)
    print(border + "╰" + "─" * (width - 2) + "╯" + RESET)


def progress_bar(current, total, width=34):
    total = max(1, total)
    current = max(0, min(current, total))
    filled = int(width * current / total)
    bar = BRIGHT_GREEN + "█" * filled + RESET + BRIGHT_BLACK + "░" * (width - filled) + RESET
    pct = int(current * 100 / total)
    return f"{bar} {BRIGHT_YELLOW}{pct:>3}%{RESET}"


def badge(label, color=BRIGHT_CYAN):
    return f"{color}{BOLD}[ {label} ]{RESET}"


def title(text, subtitle=None):
    clear()
    print()
    divider("═", BRIGHT_CYAN)
    left_pad = max(0, (WIDTH - len(text) - 4) // 2)
    print(" " * left_pad + PURPLE + BOLD + "◆ " + BRIGHT_YELLOW + text + PURPLE + " ◆" + RESET)
    if subtitle:
        print(GRAY + wrap(subtitle, WIDTH - 6).center(WIDTH) + RESET)
    divider("═", BRIGHT_CYAN)


def section(label, color=BRIGHT_CYAN):
    print("\n" + color + BOLD + f"◆ {label.upper()}" + RESET)
    print(color + "─" * min(WIDTH, len(label) + 18) + RESET)


def wrap(text, width=70):
    return "\n".join(textwrap.wrap(text, width=width))


def success(text):
    print(BRIGHT_GREEN + BOLD + "  ✓ " + text + RESET)


def warning(text):
    print(BRIGHT_YELLOW + BOLD + "  ! " + text + RESET)


def error(text):
    print(RED + BOLD + "  ✗ " + text + RESET)


def today_str():
    return date.today().isoformat()


class EndSession(Exception):
    """Exit safely without marking an unfinished activity complete."""


READING_SKILLS = {
    "sight_words", "read_sentence", "comprehension",
    "missing_word", "vocabulary", "passage", "word_family",
}
TYPING_SKILLS = {
    "type_words", "copy_sentence", "fix_sentence", "build_sentence",
}


def new_session_stats():
    return {
        "completed": 0,
        "first_try": 0,
        "attempts": 0,
        "corrections": 0,
        "stars_start": 0,
        "by_skill": {},
    }


def get_session_stats(progress):
    plan = progress.get("daily_plan") or {}
    stats = plan.setdefault("session_stats", new_session_stats())
    stats.setdefault("by_skill", {})
    return stats


def grade_from_percent(percent):
    if percent is None:
        return "N/A"
    if percent >= 90:
        return "A"
    if percent >= 80:
        return "B"
    if percent >= 70:
        return "C"
    if percent >= 60:
        return "D"
    return "Needs Practice"


def category_grade(stats, skills):
    completed = 0
    first = 0
    for skill in skills:
        data = stats.get("by_skill", {}).get(skill, {})
        completed += int(data.get("completed", 0))
        first += int(data.get("first_try", 0))
    if not completed:
        return None, "N/A", 0, 0
    percent = round(first * 100 / completed)
    return percent, grade_from_percent(percent), first, completed


def show_session_report(progress, *, finished=False):
    plan = progress.get("daily_plan") or {}
    stats = get_session_stats(progress) if plan else new_session_stats()
    completed = int(stats.get("completed", 0))
    first = int(stats.get("first_try", 0))
    overall_pct = round(first * 100 / completed) if completed else None
    overall_grade = grade_from_percent(overall_pct)
    reading_pct, reading_grade, _, reading_done = category_grade(stats, READING_SKILLS)
    typing_pct, typing_grade, _, typing_done = category_grade(stats, TYPING_SKILLS)
    total_steps = len(plan.get("activities", []))
    step = int(plan.get("step", 0))
    stars_start = int(stats.get("stars_start", progress.get("stars", 0)))
    stars_earned = max(0, int(progress.get("stars", 0)) - stars_start)

    subtitle = "Lesson complete! Here are today's grades." if finished else "Finished for now. Your work is saved."
    title("SESSION REPORT CARD", subtitle)
    print()
    status = "COMPLETE" if finished else "SAVED"
    status_color = BRIGHT_GREEN if finished else ORANGE
    print(f"{badge(status, status_color)}  {badge(plan.get('label', 'TODAY'), PURPLE)}")
    if total_steps:
        print("  " + progress_bar(min(step, total_steps), total_steps))

    def pct_text(value):
        return "N/A" if value is None else f"{value}%"

    box([
        f"Overall grade       : {overall_grade} ({pct_text(overall_pct)})",
        f"Reading grade       : {reading_grade} ({pct_text(reading_pct)})",
        f"Typing/Spelling     : {typing_grade} ({pct_text(typing_pct)})",
        f"Activities finished : {completed} / {total_steps or completed}",
        f"First-try wins      : {first} / {completed}",
        f"Corrections made    : {stats.get('corrections', 0)}",
        f"Stars earned        : {stars_earned}",
    ], border=status_color, title_text="TODAY'S GRADES")
    if not finished and total_steps and step < total_steps:
        print(YELLOW + f"\n  Next time: resume at activity {step + 1} of {total_steps}." + RESET)


def parent_menu(progress):
    if not PARENT_PIN:
        print(YELLOW + "\nParent controls are disabled. Set READING_PARENT_PIN before starting the program." + RESET)
        return False
    pin = input("Parent PIN: ").strip()
    if pin != PARENT_PIN:
        print(RED + "Wrong PIN." + RESET)
        return False

    print("\nParent controls:")
    print("  1. Save and exit")
    print("  2. Reset today's homework from the beginning")
    print("  3. Return to homework")
    while True:
        choice = input("Choose 1, 2, or 3: ").strip()
        if not choice:
            warning("Enter alone does not work. Choose 1, 2, or 3.")
            continue
        if choice == "1":
            save_progress(progress)
            print(GREEN + "\nProgress saved. The unfinished activity was not marked complete." + RESET)
            raise EndSession()
        if choice == "2":
            progress["daily_plan"] = make_daily_plan((progress.get("daily_plan") or {}).get("mode", "1"), progress.get("stars", 0))
            save_progress(progress)
            print(GREEN + "\nToday's homework was reset." + RESET)
            raise SystemExit(0)
        if choice == "3":
            return True
        warning("Choose 1, 2, or 3.")


def ask(progress, prompt, *, lower=False):
    while True:
        value = input(prompt).strip()
        if value.lower() == ":parent":
            parent_menu(progress)
            continue
        if value.upper() == "END":
            raise EndSession()
        if value == "":
            warning("You must type an answer. Enter alone does not work.")
            continue
        return value.lower() if lower else value


def require_command(progress, command="NEXT", prompt=None):
    """NEXT screens accept Enter. START still requires START. END safely exits."""
    command = command.upper()
    if prompt is None:
        prompt = "\nPress ENTER for the next activity: " if command == "NEXT" else f"\nType {command} to continue: "
    while True:
        value = input(BRIGHT_CYAN + BOLD + prompt + RESET).strip()
        if value.lower() == ":parent":
            parent_menu(progress)
            continue
        if value.upper() == "END":
            raise EndSession()
        if command == "NEXT" and value == "":
            return
        if value.upper() == command:
            return
        if not value:
            warning(f"Type {command} to continue.")
            continue
        warning(f"Press ENTER or type {command} to continue, or END to finish for now." if command == "NEXT" else f"Type {command} to continue, or END to finish for now.")


def press_to_continue(progress, prompt=None):
    """Simple child-friendly navigation: ENTER continues; END saves and exits."""
    message = prompt or "\nPress ENTER to continue: "
    while True:
        value = input(BRIGHT_CYAN + BOLD + message + RESET).strip()
        if value.lower() == ":parent":
            parent_menu(progress)
            continue
        if value.upper() == "END":
            raise EndSession()
        # For navigation, ENTER is all the child needs.
        if value == "":
            return
        # If they type something by mistake, don't punish them—just continue.
        return


def skill_record(progress, skill, first_try):
    data = progress["skills"].setdefault(skill, {"completed": 0, "first_try": 0, "attempts": 0})
    data["completed"] += 1
    data["first_try"] += int(first_try)

    if progress.get("daily_plan"):
        stats = get_session_stats(progress)
        stats["completed"] = int(stats.get("completed", 0)) + 1
        stats["first_try"] = int(stats.get("first_try", 0)) + int(first_try)
        item = stats["by_skill"].setdefault(skill, {"completed": 0, "first_try": 0, "attempts": 0})
        item["completed"] += 1
        item["first_try"] += int(first_try)


def record_attempt(progress, skill):
    progress["total_attempts"] += 1
    data = progress["skills"].setdefault(skill, {"completed": 0, "first_try": 0, "attempts": 0})
    data["attempts"] += 1
    if progress.get("daily_plan"):
        stats = get_session_stats(progress)
        stats["attempts"] = int(stats.get("attempts", 0)) + 1
        item = stats["by_skill"].setdefault(skill, {"completed": 0, "first_try": 0, "attempts": 0})
        item["attempts"] += 1


def record_mastery(progress, word, correct_first_try):
    item = progress["word_mastery"].setdefault(word.lower(), {"seen": 0, "first_try": 0})
    item["seen"] += 1
    item["first_try"] += int(correct_first_try)


def add_stars(progress, n):
    progress["stars"] += n
    save_progress(progress)


def show_step_banner(progress):
    plan = progress.get("daily_plan") or {}
    activities = plan.get("activities", [])
    step = int(plan.get("step", 0))
    if activities and step < len(activities):
        current_name = ACTIVITY_NAMES.get(activities[step].get("type"), "Activity")
        print()
        print(f"{badge(f'STEP {step + 1}/{len(activities)}', PURPLE)}  {badge(current_name.upper(), BRIGHT_CYAN)}")
        print("  " + progress_bar(step, len(activities)))
        print(GRAY + "  Read it • press ENTER when done • type END to save and stop" + RESET)


PLAN_VERSION = 5

PLAN_CHOICES = {
    "1": ("FULL LESSON", [
        "sight_words", "read_sentence", "comprehension", "type_words",
        "missing_word", "copy_sentence", "build_sentence", "passage",
    ]),
    "2": ("READING", ["sight_words", "read_sentence", "comprehension", "passage"]),
    "3": ("TYPING + SPELLING", ["type_words", "copy_sentence", "fix_sentence", "build_sentence"]),
    "4": ("WORDS", ["sight_words", "word_family", "type_words", "missing_word"]),
    "5": ("STORY TIME", ["read_sentence", "vocabulary", "passage"]),
    "6": ("QUICK MIX", ["sight_words", "comprehension", "type_words", "copy_sentence"]),
}


def make_activity(activity_type, rng, seed):
    if activity_type == "sight_words":
        return {"type": activity_type, "words": rng.sample(SIGHT_WORDS, 5)}
    if activity_type in {"read_sentence", "comprehension"}:
        return {"type": activity_type, "lesson": rng.randrange(len(LESSONS))}
    if activity_type == "word_family":
        return {"type": activity_type, "index": rng.randrange(len(WORD_FAMILIES))}
    if activity_type == "type_words":
        return {"type": activity_type, "words": rng.sample(TYPE_WORDS, 3)}
    if activity_type == "missing_word":
        return {"type": activity_type, "index": rng.randrange(len(FILL_SENTENCES))}
    if activity_type == "copy_sentence":
        return {"type": activity_type, "index": rng.randrange(len(COPY_SENTENCES))}
    if activity_type == "fix_sentence":
        return {"type": activity_type, "index": rng.randrange(len(FIX_SENTENCES))}
    if activity_type == "build_sentence":
        return {"type": activity_type, "index": rng.randrange(len(BUILD_SENTENCES)), "seed": seed + 99}
    if activity_type == "vocabulary":
        return {"type": activity_type, "index": rng.randrange(len(VOCAB))}
    if activity_type == "passage":
        return {"type": activity_type, "index": rng.randrange(len(PASSAGES)), "seed": seed + 199}
    raise ValueError(activity_type)


def make_daily_plan(mode="1", stars_start=0):
    day = today_str()
    seed = int(day.replace("-", "")) + int(mode) * 1000
    rng = random.Random(seed)
    label, activity_types = PLAN_CHOICES[mode]
    activities = [make_activity(kind, rng, seed + i * 17) for i, kind in enumerate(activity_types)]
    stats = new_session_stats()
    stats["stars_start"] = int(stars_start)
    return {
        "version": PLAN_VERSION,
        "date": day,
        "mode": mode,
        "label": label,
        "step": 0,
        "activities": activities,
        "session_stats": stats,
        "started_at": datetime.now().isoformat(timespec="seconds"),
    }


def ensure_daily_plan(progress, mode=None):
    plan = progress.get("daily_plan")
    valid = bool(plan and plan.get("date") == today_str() and plan.get("version") == PLAN_VERSION)
    if not valid:
        if mode is None:
            return None
        progress["daily_plan"] = make_daily_plan(mode, progress.get("stars", 0))
        save_progress(progress)
    return progress.get("daily_plan")


def is_today_complete(progress):
    return progress.get("last_completed_date") == today_str()


def normalize_kid_sentence(text):
    """Compare young-reader sentences without punctuation or capitalization requirements."""
    cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
    return " ".join(cleaned.split())


def require_kid_sentence(progress, prompt, correct, skill, *, hint=None):
    attempts = 0
    expected = normalize_kid_sentence(correct)
    while True:
        typed = ask(progress, prompt)
        attempts += 1
        record_attempt(progress, skill)
        if normalize_kid_sentence(typed) == expected:
            if attempts == 1:
                success("Correct!")
            else:
                success("Good correction!")
                progress["corrections"] += 1
                if progress.get("daily_plan"):
                    stats = get_session_stats(progress)
                    stats["corrections"] = int(stats.get("corrections", 0)) + 1
            save_progress(progress)
            return attempts == 1
        error("Not yet. Try the words again.")
        if hint:
            print(YELLOW + hint + RESET)


def require_exact(progress, prompt, correct, skill, *, case_sensitive=True, hint=None):
    attempts = 0
    while True:
        typed = ask(progress, prompt, lower=not case_sensitive)
        attempts += 1
        record_attempt(progress, skill)
        expected = correct if case_sensitive else correct.lower()
        if typed == expected:
            if attempts == 1:
                success("Correct on the first try!")
            else:
                success("Corrected — now it is locked in!")
                progress["corrections"] += 1
                if progress.get("daily_plan"):
                    stats = get_session_stats(progress)
                    stats["corrections"] = int(stats.get("corrections", 0)) + 1
            save_progress(progress)
            return attempts == 1
        error("Not yet. Try again — this activity cannot be skipped.")
        if hint:
            print(YELLOW + hint + RESET)


def choose_until_correct(progress, prompt, choices, correct, skill, rng=None):
    rng = rng or random
    displayed = list(choices)
    rng.shuffle(displayed)
    attempts = 0

    while True:
        print()
        for i, choice in enumerate(displayed, 1):
            print(f"  {i}. {choice}")
        answer = ask(progress, prompt)
        if answer not in [str(i) for i in range(1, len(displayed) + 1)]:
            print(YELLOW + f"Type a number from 1 to {len(displayed)}." + RESET)
            continue
        attempts += 1
        record_attempt(progress, skill)
        progress["questions_total"] += 1
        selected = displayed[int(answer) - 1]
        if selected == correct:
            progress["questions_correct"] += 1
            if attempts == 1:
                success("Correct!")
            else:
                success("Corrected — keep going!")
                progress["corrections"] += 1
                if progress.get("daily_plan"):
                    stats = get_session_stats(progress)
                    stats["corrections"] = int(stats.get("corrections", 0)) + 1
            save_progress(progress)
            return attempts == 1
        error("Not correct yet. Read it again and choose another answer.")
        save_progress(progress)


def activity_sight_words(progress, item):
    title("SIGHT WORDS", "Read each word out loud. Press ENTER when you finish.")
    show_step_banner(progress)
    for i, word in enumerate(item["words"], 1):
        print(f"\n{i}/{len(item['words'])}  {BOLD}{MAGENTA}{word.upper()}{RESET}")
        press_to_continue(progress, "   Press ENTER after you read it: ")
        record_mastery(progress, word, True)
    skill_record(progress, "sight_words", True)
    add_stars(progress, 2)


def activity_read_sentence(progress, item):
    lesson = LESSONS[item["lesson"]]
    title("READ A SENTENCE", "Read it out loud. No typing needed.")
    show_step_banner(progress)
    print("\n" + BOLD + BRIGHT_CYAN + wrap(lesson["sentence"]) + RESET)
    print("\nRead the whole sentence out loud.")
    if lesson.get("focus"):
        print(GRAY + "\nEasy words to notice: " + ", ".join(lesson["focus"]) + RESET)
    press_to_continue(progress, "\nPress ENTER when you are done reading: ")
    for word in lesson.get("focus", []):
        record_mastery(progress, word, True)
    progress["sentences_read"] += 1
    skill_record(progress, "read_sentence", True)
    add_stars(progress, 2)

def activity_comprehension(progress, item):
    lesson = LESSONS[item["lesson"]]
    title("PICK THE ANSWER", "Read the short sentence and choose the right answer.")
    show_step_banner(progress)
    print("\nRead this sentence:\n")
    print(BOLD + BRIGHT_CYAN + wrap(lesson["sentence"]) + RESET)
    print("\n" + BOLD + lesson["question"] + RESET)
    correct = lesson["choices"][lesson["answer"]]
    rng = random.Random(today_str() + ":comprehension")
    first = choose_until_correct(progress, "\nAnswer: ", lesson["choices"], correct, "comprehension", rng)
    skill_record(progress, "comprehension", first)
    add_stars(progress, 3 if first else 2)


def activity_word_family(progress, item):
    ending, words = WORD_FAMILIES[item["index"]]
    title("WORD FAMILY", "Read the words out loud. No typing needed.")
    show_step_banner(progress)
    print(f"\nToday's word family is {BOLD}{MAGENTA}{ending}{RESET}\n")
    for word in words:
        print(f"  {BOLD}{BLUE}{word.upper()}{RESET}")
        record_mastery(progress, word, True)
    press_to_continue(progress, "\nPress ENTER when you finish reading the words: ")
    skill_record(progress, "word_family", True)
    add_stars(progress, 2)

def activity_type_words(progress, item):
    title("TYPE THE WORD", "Three short words. Each one must be correct.")
    show_step_banner(progress)
    all_first = True
    for i, word in enumerate(item["words"], 1):
        print(f"\n{i}/{len(item['words'])}  {BOLD}{BLUE}{word.upper()}{RESET}")
        first = require_exact(progress, "Type it: ", word, "type_words", case_sensitive=False)
        record_mastery(progress, word, first)
        all_first = all_first and first
    skill_record(progress, "type_words", all_first)
    add_stars(progress, 3 if all_first else 2)


def activity_missing_word(progress, item):
    sentence, choices, answer = FILL_SENTENCES[item["index"]]
    title("MISSING WORD", "Type the word that fits.")
    show_step_banner(progress)
    print("\n" + BOLD + BRIGHT_CYAN + sentence + RESET)
    print("\nWord bank: " + "   ".join(choices))
    first = require_exact(progress, "\nType the missing word: ", answer, "missing_word", case_sensitive=False, hint=f"Word bank: {', '.join(choices)}")
    record_mastery(progress, answer, first)
    skill_record(progress, "missing_word", first)
    add_stars(progress, 3 if first else 2)


def activity_copy_sentence(progress, item):
    sentence = COPY_SENTENCES[item["index"]]
    title("COPY IT", "Type the words. No capital letter or period is required.")
    show_step_banner(progress)
    print("\nType these words:\n")
    print(BOLD + BRIGHT_CYAN + sentence + RESET)
    first = require_kid_sentence(progress, "\nType the sentence: ", sentence, "copy_sentence", hint="Just type the same words. Punctuation does not matter.")
    progress["sentences_read"] += 1
    skill_record(progress, "copy_sentence", first)
    add_stars(progress, 4 if first else 3)


def activity_fix_sentence(progress, item):
    wrong, correct = FIX_SENTENCES[item["index"]]
    title("TYPE THE SENTENCE", "Type the words in order. Punctuation and capitals do not matter.")
    show_step_banner(progress)
    print("\nType this sentence:\n")
    print(BOLD + YELLOW + wrong + RESET)
    first = require_kid_sentence(progress, "\nSentence: ", correct, "fix_sentence", hint="Type the same words in the same order.")
    skill_record(progress, "fix_sentence", first)
    add_stars(progress, 4 if first else 3)


def activity_build_sentence(progress, item):
    original = BUILD_SENTENCES[item["index"]]
    correct = " ".join(original)
    scrambled = original[:]
    rng = random.Random(item["seed"])
    while scrambled == original:
        rng.shuffle(scrambled)
    title("BUILD IT", "Put the easy words in the right order. No punctuation needed.")
    show_step_banner(progress)
    print("\nScrambled words:\n")
    print("   " + "   ".join(scrambled))
    first = require_kid_sentence(progress, "\nSentence: ", correct, "build_sentence", hint="Use every word once. Capitals and punctuation do not matter.")
    skill_record(progress, "build_sentence", first)
    add_stars(progress, 5 if first else 4)


def activity_vocabulary(progress, item):
    word, meaning, choices = VOCAB[item["index"]]
    title("VOCABULARY", "Choose the meaning of the word.")
    show_step_banner(progress)
    print(f"\nWhat does {BOLD}{MAGENTA}{word.upper()}{RESET} mean?")
    rng = random.Random(today_str() + ":vocab")
    first = choose_until_correct(progress, "\nAnswer: ", choices, meaning, "vocabulary", rng)
    record_mastery(progress, word, first)
    skill_record(progress, "vocabulary", first)
    add_stars(progress, 3 if first else 2)


def activity_passage(progress, item):
    passage = PASSAGES[item["index"]]
    title("SHORT STORY", "Read two short sentences, then answer one question.")
    show_step_banner(progress)
    print(f"\n{BOLD}{passage['title']}{RESET}\n")
    print(BRIGHT_CYAN + wrap(passage["text"]) + RESET)
    print("\nRead the full passage out loud.")
    all_first = True
    rng = random.Random(item["seed"])
    for qnum, (question, choices, answer) in enumerate(passage["questions"], 1):
        print(f"\n{BOLD}Question {qnum}: {question}{RESET}")
        first = choose_until_correct(progress, "\nAnswer: ", choices, answer, "passage", rng)
        all_first = all_first and first
    progress["sentences_read"] += max(1, passage["text"].count("."))
    skill_record(progress, "passage", all_first)
    add_stars(progress, 6 if all_first else 4)


ACTIVITY_FUNCS = {
    "sight_words": activity_sight_words,
    "read_sentence": activity_read_sentence,
    "comprehension": activity_comprehension,
    "word_family": activity_word_family,
    "type_words": activity_type_words,
    "missing_word": activity_missing_word,
    "copy_sentence": activity_copy_sentence,
    "fix_sentence": activity_fix_sentence,
    "build_sentence": activity_build_sentence,
    "vocabulary": activity_vocabulary,
    "passage": activity_passage,
}


def update_daily_streak(progress):
    today = date.today()
    last_raw = progress.get("last_completed_date")
    if last_raw == today.isoformat():
        return
    if last_raw:
        try:
            last = date.fromisoformat(last_raw)
        except ValueError:
            last = None
    else:
        last = None

    if last == today - timedelta(days=1):
        progress["daily_streak"] = int(progress.get("daily_streak", 0)) + 1
    else:
        progress["daily_streak"] = 1
    progress["best_streak"] = max(int(progress.get("best_streak", 0)), progress["daily_streak"])
    progress["last_completed_date"] = today.isoformat()
    progress["days_completed"] = int(progress.get("days_completed", 0)) + 1


def finish_daily_homework(progress):
    update_daily_streak(progress)
    plan = progress.get("daily_plan") or {}
    plan["completed_at"] = datetime.now().isoformat(timespec="seconds")
    plan["step"] = len(plan.get("activities", []))
    save_progress(progress)
    show_session_report(progress, finished=True)



def run_locked_homework(progress):
    plan = progress.get("daily_plan")
    if not plan:
        return
    activities = plan["activities"]

    while int(plan.get("step", 0)) < len(activities):
        step = int(plan.get("step", 0))
        item = activities[step]
        func = ACTIVITY_FUNCS[item["type"]]
        func(progress, item)

        # Only advance after the activity function has verified completion.
        plan["step"] = step + 1
        progress["daily_plan"] = plan
        save_progress(progress)

        if plan["step"] < len(activities):
            print("\n" + badge(f"LOCKED IN {plan['step']}/{len(activities)}", BRIGHT_GREEN)); print("  " + progress_bar(plan["step"], len(activities)))
            press_to_continue(progress, "\nPress ENTER for the next activity: ")

    finish_daily_homework(progress)


def show_progress(progress):
    title("PROGRESS DASHBOARD")
    total = progress["questions_total"]
    correct = progress["questions_correct"]
    percent = int((correct / total) * 100) if total else 0

    print()
    box([
        f"★ Stars earned       : {progress['stars']}",
        f"◆ Days completed     : {progress['days_completed']}",
        f"🔥 Current streak     : {progress['daily_streak']} day(s)",
        f"🏆 Best streak        : {progress['best_streak']} day(s)",
        f"▣ Sentences read     : {progress['sentences_read']}",
        f"✓ Questions correct  : {correct} / {total}",
        f"◉ Overall quiz score : {percent}%",
        f"↻ Total attempts     : {progress['total_attempts']}",
        f"✎ Corrections made   : {progress['corrections']}",
    ], border=PURPLE, title_text="PLAYER STATS")

    if progress["skills"]:
        print("\n" + BOLD + "SKILL MASTERY" + RESET)
        for skill, data in sorted(progress["skills"].items()):
            completed = data.get("completed", 0)
            first = data.get("first_try", 0)
            rate = int((first / completed) * 100) if completed else 0
            label = ACTIVITY_NAMES.get(skill, skill.replace("_", " ").title())
            mini_width = 16
            filled = int(mini_width * rate / 100)
            mini = BRIGHT_GREEN + "█" * filled + RESET + BRIGHT_BLACK + "░" * (mini_width - filled) + RESET
            print(f"  {BRIGHT_CYAN}{label:<22}{RESET} {mini} {BRIGHT_YELLOW}{rate:>3}%{RESET}  {GRAY}{first}/{completed}{RESET}")

    if progress["word_mastery"]:
        weak = []
        for word, data in progress["word_mastery"].items():
            seen = data.get("seen", 0)
            first = data.get("first_try", 0)
            if seen and first < seen:
                weak.append((first / seen, word, first, seen))
        weak.sort()
        if weak:
            print("\n" + BOLD + "WORDS TO REVIEW" + RESET)
            for _, word, first, seen in weak[:10]:
                print(f"  {word:<15} {first}/{seen} correct first try")

    press_to_continue(progress, "\nPress ENTER for the next activity: ")


def extra_practice(progress, activity_type):
    # Extra practice is intentionally optional, but each chosen activity itself is non-skippable.
    seed = random.randrange(1_000_000)
    rng = random.Random(seed)
    if activity_type == "sight_words":
        item = {"type": "sight_words", "words": rng.sample(SIGHT_WORDS, 5)}
    elif activity_type == "read_sentence":
        item = {"type": "read_sentence", "lesson": rng.randrange(len(LESSONS))}
    elif activity_type == "comprehension":
        item = {"type": "comprehension", "lesson": rng.randrange(len(LESSONS))}
    elif activity_type == "word_family":
        item = {"type": "word_family", "index": rng.randrange(len(WORD_FAMILIES))}
    elif activity_type == "type_words":
        item = {"type": "type_words", "words": rng.sample(TYPE_WORDS, 3)}
    elif activity_type == "missing_word":
        item = {"type": "missing_word", "index": rng.randrange(len(FILL_SENTENCES))}
    elif activity_type == "copy_sentence":
        item = {"type": "copy_sentence", "index": rng.randrange(len(COPY_SENTENCES))}
    elif activity_type == "fix_sentence":
        item = {"type": "fix_sentence", "index": rng.randrange(len(FIX_SENTENCES))}
    elif activity_type == "build_sentence":
        item = {"type": "build_sentence", "index": rng.randrange(len(BUILD_SENTENCES)), "seed": seed}
    elif activity_type == "vocabulary":
        item = {"type": "vocabulary", "index": rng.randrange(len(VOCAB))}
    elif activity_type == "passage":
        item = {"type": "passage", "index": rng.randrange(len(PASSAGES)), "seed": seed}
    else:
        return
    ACTIVITY_FUNCS[activity_type](progress, item)
    save_progress(progress)
    press_to_continue(progress, "\nPress ENTER for the next activity: ")


def choose_today(progress):
    while True:
        existing = ensure_daily_plan(progress)
        if existing and int(existing.get("step", 0)) < len(existing.get("activities", [])):
            title("TODAY'S READING", "Your unfinished lesson is saved.")
            step = int(existing.get("step", 0))
            total = len(existing.get("activities", []))
            print()
            print(f"{badge('RESUME', ORANGE)}  {badge(existing.get('label', 'LESSON'), PURPLE)}")
            print("  " + progress_bar(step, total))
            print(f"\n  {BRIGHT_CYAN}1{RESET}  Resume lesson")
            print(f"  {PURPLE}2{RESET}  See progress")
            print(f"  {RED}0{RESET}  End session")
            choice = input(BRIGHT_CYAN + BOLD + "\nkid@reading $ " + RESET).strip()
            if not choice:
                warning("Enter alone does not work. Choose 1, 2, or 0.")
                continue
            if choice == "1":
                return existing
            if choice == "2":
                show_progress(progress)
                continue
            if choice == "0":
                raise EndSession()
            warning("Choose 1, 2, or 0.")
            continue

        # Completed or stale plans do not lock the user into a previous choice.
        progress["daily_plan"] = None
        save_progress(progress)
        title("WHAT DO YOU WANT TO DO TODAY?", "Pick one lesson. Once it starts, its activities cannot be skipped.")
        print()
        menu = [
            ("1", "FULL LESSON", "8 activities"),
            ("2", "READING", "4 activities"),
            ("3", "TYPING + SPELLING", "4 activities"),
            ("4", "WORDS", "4 activities"),
            ("5", "STORY TIME", "3 activities"),
            ("6", "QUICK MIX", "4 activities"),
        ]
        colors = [BRIGHT_CYAN, PURPLE, PINK, ORANGE, BRIGHT_YELLOW, LIME]
        for idx, (key, label, detail) in enumerate(menu):
            col = colors[idx]
            print(f"  {col}{BOLD}{key}{RESET}  {col}◆{RESET} {label:<20} {GRAY}{detail}{RESET}")
        print(f"  {BRIGHT_GREEN}{BOLD}7{RESET}  {BRIGHT_GREEN}◆{RESET} PROGRESS")
        print(f"  {RED}{BOLD}0{RESET}  {RED}◆{RESET} END")
        print(GRAY + "\n  Pick a lesson with a number. Inside the lesson, ENTER moves through reading screens." + RESET)
        choice = input(BRIGHT_CYAN + BOLD + "\nkid@reading $ " + RESET).strip()
        if not choice:
            warning("Enter alone does not work. Choose a number.")
            continue
        if choice in PLAN_CHOICES:
            plan = make_daily_plan(choice, progress.get("stars", 0))
            progress["daily_plan"] = plan
            save_progress(progress)
            return plan
        if choice == "7":
            show_progress(progress)
            continue
        if choice == "0":
            raise EndSession()
        warning("Choose 1 through 7, or 0 to end.")


def after_complete_menu(progress):
    while True:
        print()
        print(f"  {BRIGHT_CYAN}{BOLD}1{RESET}  Choose another lesson")
        print(f"  {PURPLE}{BOLD}2{RESET}  Progress dashboard")
        print(f"  {RED}{BOLD}0{RESET}  End for today")
        choice = input(BRIGHT_CYAN + BOLD + "\nkid@reading $ " + RESET).strip()
        if not choice:
            warning("Enter alone does not work. Choose 1, 2, or 0.")
            continue
        if choice == "1":
            progress["daily_plan"] = None
            save_progress(progress)
            return True
        if choice == "2":
            show_progress(progress)
            continue
        if choice == "0":
            return False
        warning("Choose 1, 2, or 0.")


def main():
    progress = load_progress()
    try:
        while True:
            plan = choose_today(progress)
            total = len(plan.get("activities", []))
            step = int(plan.get("step", 0))
            title(plan.get("label", "TODAY'S LESSON"), f"{total} short activities. Press ENTER to move through reading parts.")
            print()
            state = f"RESUME {step + 1}/{total}" if step else "READY"
            print(f"{badge(state, ORANGE)}  {badge('NO SKIPPING', PURPLE)}")
            print("  " + progress_bar(step, total))
            box([
                "PRESS ENTER TO START AND GO TO THE NEXT ACTIVITY",
                "READING ACTIVITIES DO NOT REQUIRE TYPING",
                "ONLY REAL QUESTIONS NEED AN ANSWER",
                "TYPE END ANY TIME TO SAVE AND STOP",
                "RESTARTING RETURNS TO THE UNFINISHED ACTIVITY",
            ], border=PURPLE, title_text="SIMPLE RULES")
            press_to_continue(progress, "\nPress ENTER to begin, or type END to stop: ")
            run_locked_homework(progress)
            if not after_complete_menu(progress):
                clear()
                print(BRIGHT_GREEN + BOLD + "\nGreat work today! Your grades and progress are saved.\n" + RESET)
                return

    except EndSession:
        save_progress(progress)
        if progress.get("daily_plan"):
            show_session_report(progress, finished=False)
        else:
            clear()
            print(BRIGHT_CYAN + BOLD + "\nSession ended. No work was lost.\n" + RESET)
        return
    except (KeyboardInterrupt, EOFError):
        save_progress(progress)
        if progress.get("daily_plan"):
            show_session_report(progress, finished=False)
        else:
            print(YELLOW + "\n\nProgress saved." + RESET)
        raise SystemExit(0)


if __name__ == "__main__":
    main()
