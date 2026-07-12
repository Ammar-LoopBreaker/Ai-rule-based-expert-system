# Expert System for Diagnosis
### A Rule-Based Expert System for Computer Troubleshooting

Diagnose common computer problems from user-reported symptoms using classic
**if-then rule matching** and **forward-chaining inference** — built with
pure Python, zero dependencies.


## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [How the Inference Engine Works](#-how-the-inference-engine-works)
- [Knowledge Base](#-knowledge-base)
- [Extending the System](#-extending-the-system)
- [Requirement Checklist](#-requirement-checklist)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)


## Overview

This project is a **rule-based expert system** — a type of AI program that
mimics the decision-making of a human expert by applying a fixed set of
**IF-THEN rules** to a set of known facts (here, user-reported symptoms).

Given a list of symptoms a user is experiencing on their computer, the
system matches them against a curated knowledge base of **22 diagnostic
rules** and returns the most likely diagnosis, ranked by confidence, along
with the reasoning behind each suggestion and a recommended next step.

It runs entirely in the terminal, requires **no external libraries**, and
is structured so the knowledge base, reasoning engine, and user interface
are cleanly separated — a design pattern used by real-world expert systems.


## Features

- **20 known symptoms** covering hardware, software, network, and
  peripheral issues
- **22 if-then rules** mapping symptom combinations to diagnoses
- **Confidence scoring** — ranks diagnoses by how well they match your
  reported symptoms, and tells you which additional symptom would raise
  the confidence further
- **Flexible input** — enter symptoms by number (`1,4,7`) or by name
  (`overheating`)
- **Graceful error handling** — blank input, typos, unknown entries,
  and `Ctrl+C` / `Ctrl+D` are all handled without the program ever
  crashing
- **Fuzzy "Did you mean...?" suggestions** for misspelled symptom names
- **Multi-session loop** — diagnose multiple issues in one run
- **Fully modular** — knowledge, logic, and interface live in separate
  files, so extending the system never requires touching the reasoning
  code


## Demo

```
$ python main.py

================================================================
   RULE-BASED EXPERT SYSTEM — COMPUTER TROUBLESHOOTING ADVISOR
================================================================

----------------------------------------------------------------
KNOWN SYMPTOMS
----------------------------------------------------------------
   1. Computer does not turn on at all (no lights, no fans)
   2. Computer powers on (fans/lights work) but nothing shows on screen
   3. Computer beeps repeatedly during startup
   ...
  20. A specific application crashes repeatedly
----------------------------------------------------------------

> 7,10
  ✔ Added: Computer feels very hot / fan is unusually loud
  ✔ Added: Unusual clicking, grinding, or whirring noises
> done
----------------------------------------------------------------
DIAGNOSIS RESULTS  (2 possible match(es) found)
----------------------------------------------------------------
[1] Cooling Fan Failure / Dust Buildup  (confidence: 100%)
    Reasoning : Overheating paired with unusual noise strongly suggests
    a failing fan or heavy dust buildup restricting airflow.
    Suggested action : Power down and clean dust from vents and fans,
    and replace any fan that produces grinding noises.
    Based on your reported symptom(s): Computer feels very hot / fan is
    unusually loud, Unusual clicking, grinding, or whirring noises
----------------------------------------------------------------
```


## Project Structure

```
expert_system/
├── main.py               # Entry point — console interface & program flow
├── knowledge_base.py      # The "knowledge": symptom catalog + if-then rules
├── inference_engine.py    # The "reasoning": matches symptoms to rules
├── utils.py                # Console I/O helpers + input validation
└── README.md                # Project documentation
```


## Architecture

The system follows the classic **three-layer expert system design**:

```
┌─────────────────────┐      ┌───────────────────────┐      ┌──────────────┐
│   Knowledge Base     │      │   Inference Engine     │      │  Interface    │
│  knowledge_base.py    │ ───▶ │  inference_engine.py    │ ───▶ │  main.py /     │
│                        │      │                          │      │  utils.py       │
│  • Symptom catalog     │      │  • Symptom matching       │      │  • Prompts user  │
│  • If-then rule set     │      │  • Confidence scoring       │      │  • Displays       │
│  • Explanations/advice   │      │  • Ranking logic              │      │    results          │
└─────────────────────┘      └───────────────────────┘      └──────────────┘
```

| Layer | Responsibility | Depends on |
|---|---|---|
| **Knowledge Base** | Stores facts (symptoms) and rules (symptom → diagnosis mappings). Pure data, no logic. | Nothing |
| **Inference Engine** | Pure reasoning: compares reported symptoms to rules and scores/ranks matches. No I/O. | Knowledge Base |
| **Interface** | Handles all user interaction — prompts, validation, and formatted output. | Inference Engine |

This separation means you can, for example, swap the console interface for
a web API or GUI without changing a single line of the reasoning logic.


## Installation

**Requirements:** Python 3.7 or later. No external packages needed.

```bash
# Clone the repository
git clone https://github.com/<your-username>/expert-system-diagnosis.git
cd expert-system-diagnosis/expert_system
```

---

## Usage

Run the program from the `expert_system` directory:

```bash
python main.py
```

Then follow the on-screen prompts:

| Command | Action |
|---|---|
| `1,4,7` | Select symptoms by number (comma-separated) |
| `overheating` | Select a symptom by name |
| `list` | Show the symptom menu again |
| `help` | Show usage instructions |
| `done` | Finish entering symptoms and run the diagnosis |
| `quit` | Exit the program at any time |

---

## How the Inference Engine Works

1. Each rule defines a **required set of symptom codes**.
2. When you report symptoms, the engine checks every rule for overlap:

   ```
   confidence = (matched symptoms) ÷ (symptoms required by the rule)
   ```

3. Rules with **any overlap** are included in the results; a rule where
   *every* required symptom is present scores **100%**.
4. Results are sorted by:
   1. **Highest confidence first**
   2. **Most specific match** (more corroborating symptoms) as a tie-breaker
5. The **top 3 matches** are displayed, each with the diagnosis,
   confidence score, plain-English reasoning, and a suggested fix.
   Partial matches also show which extra symptom would strengthen the
   diagnosis.

This approach means the system degrades gracefully — even an incomplete
or unusual combination of symptoms still returns the closest reasonable
matches instead of a hard failure.

---

## Knowledge Base

<details>
<summary><strong>Click to expand the full list of 22 diagnostic rules</strong></summary>

| Rule ID | Trigger Symptom(s) | Diagnosis |
|---|---|---|
| R01 | No power at all | Power Supply / Power Source Failure |
| R02 | Powers on, no display | Display / GPU / Monitor Connection Issue |
| R03 | Beeping on startup | Hardware POST Failure (RAM/GPU Seating) |
| R04 | Slow performance + low disk space | Low Disk Space Causing Slow Performance |
| R05 | Slow performance + freezing | Insufficient RAM or Malware Infection |
| R06 | Overheating + strange noises | Cooling Fan Failure / Dust Buildup |
| R07 | Overheating + random restarts | Overheating Causing Thermal Shutdown |
| R08 | Blue screen | Driver Conflict or Faulty RAM (BSOD) |
| R09 | No internet | Network Adapter or ISP Connectivity Issue |
| R10 | Wi-Fi drops | Wi-Fi Driver or Router Interference Issue |
| R11 | Strange noises (alone) | Failing Hard Disk Drive (HDD) |
| R12 | Battery not charging | Battery or Charger/Adapter Fault |
| R13 | Random restarts + virus warning | Malware Infection Causing Instability |
| R14 | Random restarts (alone) | Power Supply Instability or Overheating |
| R15 | Slow boot + low disk space | Disk Fragmentation / Startup Overload |
| R16 | Slow boot (alone) | Too Many Startup Programs |
| R17 | Virus warning (alone) | Malware / Virus Infection |
| R18 | Keyboard not working | Keyboard Hardware Fault or Driver Issue |
| R19 | No sound | Audio Driver or Speaker Hardware Issue |
| R20 | Screen flickering | Display Cable or GPU Driver Issue |
| R21 | USB not detected | USB Port or Driver Issue |
| R22 | Software crash | Corrupted Application or Compatibility Issue |

</details>

---

## Extending the System

The modular design makes it easy to grow the knowledge base without
touching any reasoning or interface code.

**To add a new symptom** — add one entry to `SYMPTOMS` in
`knowledge_base.py`:

```python
"gpu_artifacts": "Screen shows visual glitches or graphical artifacts",
```

**To add a new rule** — append a dictionary to `RULES` in
`knowledge_base.py`:

```python
{
    "id": "R23",
    "symptoms": {"gpu_artifacts"},
    "diagnosis": "Failing Graphics Card",
    "explanation": "Visual artifacts typically indicate a dying GPU or "
                    "an overheating graphics chip.",
    "advice": "Update GPU drivers, check temperatures, and test with "
               "another graphics card if possible.",
},
```

No changes are needed in `inference_engine.py` or `main.py` — the engine
automatically picks up new rules and symptoms.

---

## Requirement Checklist

| Requirement | Implementation |
|---|---|
| Define a set of if-then rules linking symptoms to diagnoses | `knowledge_base.py` → `RULES` |
| Create a console interface that prompts the user for symptoms | `main.py` + `utils.get_symptom_selection()` |
| Output a diagnosis along with a brief explanation of the reasoning | `utils.display_results()` |
| Ensure the system handles unexpected inputs gracefully | `utils.py` — blank input, typos, fuzzy suggestions, `Ctrl+C`/`Ctrl+D`, invalid rule base guard |

---

## Roadmap

- [ ] Add a `--symptoms` CLI flag for non-interactive/scripted diagnosis
- [ ] Export results to JSON/PDF for reporting
- [ ] Add unit tests (`pytest`) for the inference engine
- [ ] Optional web interface (Flask/FastAPI) reusing the same engine
- [ ] Support multiple knowledge domains (e.g. car troubleshooting) via
      pluggable rule files

---

## Contributing

Contributions are welcome! To propose a change:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-rule`)
3. Commit your changes (`git commit -m "Add rule for GPU artifacts"`)
4. Push to your branch (`git push origin feature/new-rule`)
5. Open a Pull Request

Please keep new rules consistent with the existing style in
`knowledge_base.py` (clear `explanation` and actionable `advice`).


<div align="center">

Built as a demonstration of classic rule-based expert system design in Python.

</div>
