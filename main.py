import sys

from knowledge_base import SYMPTOMS, RULES
from inference_engine import ExpertSystemEngine
from utils import (
    clear_screen,
    print_banner,
    print_divider,
    print_help,
    get_symptom_selection,
    display_results,
    ask_yes_no,
)


def run_session(engine: ExpertSystemEngine):
    """Run a single diagnosis session: collect symptoms, show results."""
    reported_symptoms = get_symptom_selection(SYMPTOMS)

    if not reported_symptoms:
        # User quit before entering anything — nothing more to do.
        return

    print_divider()
    print("Analyzing reported symptoms...")
    results = engine.diagnose(reported_symptoms)
    display_results(results, SYMPTOMS)


def main():
    clear_screen()
    print_banner()
    print("Welcome! This expert system helps diagnose common computer")
    print("problems based on the symptoms you report.\n")
    print_help()

    try:
        engine = ExpertSystemEngine(RULES)
    except ValueError as err:
        # Handles the unexpected case of a misconfigured/empty rule base
        # gracefully instead of letting the program crash with a traceback.
        print(f"Fatal configuration error: {err}")
        sys.exit(1)

    while True:
        run_session(engine)

        print()
        if not ask_yes_no("Would you like to diagnose another issue?"):
            print("\nThank you for using the Expert System. Goodbye!")
            break
        clear_screen()
        print_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Final safety net: Ctrl+C at any point (even outside the input
        # prompts in utils.py) exits cleanly rather than dumping a
        # traceback in the user's face.
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)