import difflib
import os

def clear_screen():
    """Clear the terminal screen on both Windows and Unix-like systems."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print("=" * 64)
    print("   RULE-BASED EXPERT SYSTEM — COMPUTER TROUBLESHOOTING ADVISOR")
    print("=" * 64)


def print_divider():
    print("-" * 64)


def print_help():
    print_divider()
    print("HOW TO USE THIS SYSTEM")
    print_divider()
    print("  • Enter one or more symptom numbers separated by commas,")
    print("    e.g.  1,4,7")
    print("  • Type the symptom name instead of a number if you prefer,")
    print("    e.g.  overheating")
    print("  • Type 'list'  to see the symptom menu again")
    print("  • Type 'done'  when you have finished entering symptoms")
    print("  • Type 'help'  to see this message again")
    print("  • Type 'quit'  or press Ctrl+C at any time to exit")
    print_divider()


def display_symptom_menu(symptoms: dict):
    """Print a numbered menu of all known symptoms."""
    print_divider()
    print("KNOWN SYMPTOMS")
    print_divider()
    for index, (code, description) in enumerate(symptoms.items(), start=1):
        print(f"  {index:>2}. {description}")
    print_divider()


def _build_lookup_maps(symptoms: dict):
    """Build helper maps to translate user input -> internal symptom code."""
    index_to_code = {str(i): code for i, code in enumerate(symptoms.keys(), start=1)}
    name_to_code = {code.replace("_", " "): code for code in symptoms}
    name_to_code.update({code: code for code in symptoms})  # allow raw codes too
    return index_to_code, name_to_code


def get_symptom_selection(symptoms: dict) -> set:
    """
    Interactively collect symptoms from the user until they type 'done'.

    Handles unexpected input gracefully:
      - blank lines are ignored with a gentle reminder
      - unknown numbers/names trigger a fuzzy "did you mean...?" suggestion
      - mixed valid/invalid entries in one line are handled individually
      - Ctrl+C / Ctrl+D exit cleanly instead of crashing

    Returns:
        A set of valid internal symptom codes chosen by the user.
        Returns an empty set if the user quits before selecting anything.
    """
    index_to_code, name_to_code = _build_lookup_maps(symptoms)
    all_known_names = list(name_to_code.keys())
    selected = set()

    display_symptom_menu(symptoms)
    print("Enter symptom numbers or names (comma-separated).")
    print("Type 'help' for instructions, 'done' when finished, 'quit' to exit.\n")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. No diagnosis was performed.")
            return set()

        if not raw:
            print("  (No input detected — please enter a symptom, or type 'help'.)")
            continue

        lowered = raw.lower()

        if lowered in ("quit", "exit", "q"):
            print("Exiting. No diagnosis was performed.")
            return set()

        if lowered in ("help", "?"):
            print_help()
            continue

        if lowered in ("list", "menu"):
            display_symptom_menu(symptoms)
            continue

        if lowered == "done":
            if not selected:
                print("  You haven't entered any symptoms yet. "
                      "Please enter at least one, or type 'quit' to exit.")
                continue
            return selected

        # Process one or more comma-separated entries on this line
        entries = [e.strip() for e in raw.split(",") if e.strip()]
        for entry in entries:
            code = index_to_code.get(entry)
            if code is None:
                code = name_to_code.get(entry.lower())

            if code:
                if code in selected:
                    print(f"  • '{symptoms[code]}' is already noted.")
                else:
                    selected.add(code)
                    print(f"  ✔ Added: {symptoms[code]}")
                continue

            # Unknown entry — try to help with a fuzzy suggestion
            suggestion = difflib.get_close_matches(entry.lower(), all_known_names, n=1, cutoff=0.6)
            if suggestion:
                print(f"  ✘ '{entry}' was not recognized. Did you mean "
                      f"'{suggestion[0]}'? Please re-enter it exactly, "
                      f"or type 'list' to see valid options.")
            else:
                print(f"  ✘ '{entry}' was not recognized. Type 'list' to "
                      f"see valid symptom numbers/names.")

        if selected:
            print(f"  (Currently selected: {len(selected)} symptom(s). "
                  f"Type 'done' when finished.)")


def display_results(results, symptoms: dict):
    """Pretty-print a list of DiagnosisResult objects."""
    print_divider()
    if not results:
        print("No matching diagnosis was found for the reported symptoms.")
        print("This could mean the issue is outside this system's rule base, "
              "or the symptoms don't align with a known fault pattern.")
        print("Recommendation: consult a qualified technician for a deeper "
              "hardware/software inspection.")
        print_divider()
        return

    print(f"DIAGNOSIS RESULTS  ({len(results)} possible match(es) found)")
    print_divider()

    for rank, result in enumerate(results[:3], start=1):  # show top 3
        print(f"[{rank}] {result.diagnosis}  (confidence: {result.confidence_percent})")
        print(f"    Reasoning : {result.explanation}")
        print(f"    Suggested action : {result.advice}")

        matched_desc = ", ".join(symptoms[c] for c in result.matched_symptoms)
        print(f"    Based on your reported symptom(s): {matched_desc}")

        if result.missing_symptoms:
            missing_desc = ", ".join(symptoms[c] for c in result.missing_symptoms)
            print(f"    (Confidence would be higher if this symptom were also "
                  f"present: {missing_desc})")
        print()

    print_divider()


def ask_yes_no(prompt: str) -> bool:
    """Ask a yes/no question, gracefully re-prompting on invalid input."""
    while True:
        try:
            answer = input(f"{prompt} (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return False

        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer 'y' or 'n'.")