# ---------------------------------------------------------------------------
# 1. SYMPTOM CATALOG
# ---------------------------------------------------------------------------
# Domain: Computer Troubleshooting
# Each symptom has a short internal "code" (used by the rules) and a
# human-friendly description (shown to the user).
SYMPTOMS = {
    "no_power":            "Computer does not turn on at all (no lights, no fans)",
    "no_display":          "Computer powers on (fans/lights work) but nothing shows on screen",
    "beeping_sounds":      "Computer beeps repeatedly during startup",
    "slow_performance":    "Computer / applications run very slowly",
    "frequent_freezing":   "System freezes or becomes unresponsive frequently",
    "blue_screen":         "Blue Screen of Death (BSOD) or system crash with error screen",
    "overheating":         "Computer feels very hot / fan is unusually loud",
    "no_internet":         "No internet connection at all",
    "wifi_drops":          "Wi-Fi connects but disconnects repeatedly",
    "strange_noises":      "Unusual clicking, grinding, or whirring noises",
    "battery_not_charging": "Laptop battery does not charge",
    "random_restarts":     "Computer restarts on its own randomly",
    "slow_boot":           "Computer takes a very long time to start up",
    "disk_full_warning":   "Low disk space / storage full warnings",
    "virus_warning":       "Antivirus alerts or suspicious pop-ups appear",
    "keyboard_not_working": "Some or all keyboard keys do not respond",
    "no_sound":            "No sound from speakers or headphones",
    "screen_flickering":   "Screen flickers on and off intermittently",
    "usb_not_detected":    "USB devices are not detected when plugged in",
    "software_crash":      "A specific application crashes repeatedly",
}

# ---------------------------------------------------------------------------
# 2. RULE BASE
# ---------------------------------------------------------------------------
# Each rule is a dictionary with:
#   id          : unique rule identifier (for traceability/debugging)
#   symptoms    : the set of symptom codes that must ALL be present for a
#                 perfect (100%) match. Partial matches are still reported
#                 by the inference engine with a lower confidence score.
#   diagnosis   : the name of the probable problem
#   explanation : a short, plain-English justification for the diagnosis
#   advice      : a practical next step for the user
#
# Rules with more required symptoms are more SPECIFIC. When multiple rules
# match, the inference engine ranks more specific, fully-matched rules
# above single-symptom, generic ones.
RULES = [
    {
        "id": "R01",
        "symptoms": {"no_power"},
        "diagnosis": "Power Supply / Power Source Failure",
        "explanation": "The system shows absolutely no sign of power (no lights, "
                        "no fans, no sound), which almost always points to the "
                        "power supply unit, power cable, or wall outlet rather "
                        "than a software issue.",
        "advice": "Check the power cable and outlet, try a different socket, and "
                   "inspect the power supply unit (PSU) for faults.",
    },
    {
        "id": "R02",
        "symptoms": {"no_display"},
        "diagnosis": "Display / GPU / Monitor Connection Issue",
        "explanation": "The machine is receiving power (fans and lights are active) "
                        "but nothing appears on screen, which usually indicates a "
                        "loose video cable, faulty monitor, or graphics card fault.",
        "advice": "Reseat the monitor cable, test with another monitor, and check "
                   "that the graphics card is properly seated.",
    },
    {
        "id": "R03",
        "symptoms": {"beeping_sounds"},
        "diagnosis": "Hardware POST Failure (RAM / GPU Seating Issue)",
        "explanation": "Repeated beeps during startup are BIOS/UEFI POST error "
                        "codes, most commonly caused by improperly seated RAM "
                        "or a graphics card.",
        "advice": "Power off, reseat the RAM modules and graphics card, and "
                   "restart. Consult your motherboard manual for the exact beep code.",
    },
    {
        "id": "R04",
        "symptoms": {"slow_performance", "disk_full_warning"},
        "diagnosis": "Low Disk Space Causing Slow Performance",
        "explanation": "A near-full disk drastically slows down the operating "
                        "system because it has little room for virtual memory "
                        "and temporary files.",
        "advice": "Free up disk space by removing unused files/programs, or "
                   "consider upgrading to a larger drive.",
    },
    {
        "id": "R05",
        "symptoms": {"slow_performance", "frequent_freezing"},
        "diagnosis": "Insufficient RAM or Malware Infection",
        "explanation": "Slowness combined with frequent freezing typically means "
                        "the system is running out of memory or is being "
                        "burdened by malicious background processes.",
        "advice": "Check RAM usage in Task Manager, close unused programs, run a "
                   "full antivirus scan, and consider a RAM upgrade.",
    },
    {
        "id": "R06",
        "symptoms": {"overheating", "strange_noises"},
        "diagnosis": "Cooling Fan Failure / Dust Buildup",
        "explanation": "Overheating paired with unusual noise strongly suggests "
                        "a failing fan or heavy dust buildup restricting airflow.",
        "advice": "Power down and clean dust from vents and fans, and replace "
                   "any fan that produces grinding noises.",
    },
    {
        "id": "R07",
        "symptoms": {"overheating", "random_restarts"},
        "diagnosis": "Overheating Causing Thermal Shutdown",
        "explanation": "Random restarts combined with excessive heat indicate the "
                        "system is protecting itself by shutting down when a "
                        "thermal limit is reached.",
        "advice": "Improve ventilation, clean/replace fans, reapply thermal "
                   "paste, and avoid blocking air vents.",
    },
    {
        "id": "R08",
        "symptoms": {"blue_screen"},
        "diagnosis": "Driver Conflict or Faulty RAM (BSOD)",
        "explanation": "Blue Screen of Death errors are most often caused by "
                        "incompatible/corrupted drivers or failing memory modules.",
        "advice": "Update or roll back recently changed drivers and run a memory "
                   "diagnostic tool (e.g., Windows Memory Diagnostic).",
    },
    {
        "id": "R09",
        "symptoms": {"no_internet"},
        "diagnosis": "Network Adapter or ISP Connectivity Issue",
        "explanation": "A total loss of internet access, with no other symptoms, "
                        "usually points to the network adapter, router, or the "
                        "internet service provider.",
        "advice": "Restart the router/modem, check cables, and verify the network "
                   "adapter is enabled in device settings.",
    },
    {
        "id": "R10",
        "symptoms": {"wifi_drops"},
        "diagnosis": "Wi-Fi Driver or Router Interference Issue",
        "explanation": "Intermittent Wi-Fi disconnects typically stem from an "
                        "outdated wireless driver, router placement, or signal "
                        "interference rather than a total hardware failure.",
        "advice": "Update the Wi-Fi driver, move closer to the router, and check "
                   "for interference from other electronic devices.",
    },
    {
        "id": "R11",
        "symptoms": {"strange_noises"},
        "diagnosis": "Failing Hard Disk Drive (HDD)",
        "explanation": "Clicking or grinding noises on their own (without "
                        "overheating) are a classic warning sign of a "
                        "mechanical hard drive nearing failure.",
        "advice": "Back up your data immediately and run a disk health check "
                   "(e.g., CHKDSK or a S.M.A.R.T. utility).",
    },
    {
        "id": "R12",
        "symptoms": {"battery_not_charging"},
        "diagnosis": "Battery or Charger/Adapter Fault",
        "explanation": "A battery that will not charge is generally caused by a "
                        "worn-out battery, a faulty charging cable, or a damaged "
                        "charging port.",
        "advice": "Test with a different charger/cable, clean the charging port, "
                   "and consider a battery replacement if the laptop is old.",
    },
    {
        "id": "R13",
        "symptoms": {"random_restarts", "virus_warning"},
        "diagnosis": "Malware Infection Causing System Instability",
        "explanation": "Random restarts alongside active virus/malware alerts "
                        "suggest malicious software is destabilizing the system.",
        "advice": "Disconnect from the internet, run a full antivirus/anti-malware "
                   "scan, and update your security software.",
    },
    {
        "id": "R14",
        "symptoms": {"random_restarts"},
        "diagnosis": "Power Supply Instability or Overheating",
        "explanation": "Random restarts on their own are most commonly linked to "
                        "an unstable power supply or mild overheating.",
        "advice": "Check PSU health, monitor CPU/GPU temperatures, and ensure "
                   "adequate ventilation.",
    },
    {
        "id": "R15",
        "symptoms": {"slow_boot", "disk_full_warning"},
        "diagnosis": "Disk Fragmentation / Startup Overload",
        "explanation": "A slow boot combined with low disk space usually means "
                        "the startup disk is overloaded or fragmented.",
        "advice": "Free up disk space, disable unnecessary startup programs, and "
                   "run disk optimization/defragmentation.",
    },
    {
        "id": "R16",
        "symptoms": {"slow_boot"},
        "diagnosis": "Too Many Startup Programs",
        "explanation": "A slow boot on its own is most often caused by an "
                        "excessive number of programs launching at startup.",
        "advice": "Open Task Manager (Startup tab) and disable non-essential "
                   "startup applications.",
    },
    {
        "id": "R17",
        "symptoms": {"virus_warning"},
        "diagnosis": "Malware / Virus Infection",
        "explanation": "Active antivirus alerts or suspicious pop-ups directly "
                        "indicate the presence of malicious software.",
        "advice": "Run a full system scan with updated antivirus software and "
                   "avoid clicking on unknown pop-ups or links.",
    },
    {
        "id": "R18",
        "symptoms": {"keyboard_not_working"},
        "diagnosis": "Keyboard Hardware Fault or Driver Issue",
        "explanation": "Unresponsive keys point to either a hardware fault in "
                        "the keyboard or an outdated/corrupted keyboard driver.",
        "advice": "Try an external keyboard to isolate the issue, and update or "
                   "reinstall the keyboard driver.",
    },
    {
        "id": "R19",
        "symptoms": {"no_sound"},
        "diagnosis": "Audio Driver or Speaker Hardware Issue",
        "explanation": "A total lack of sound is usually caused by a muted/"
                        "misconfigured audio device, an outdated driver, or "
                        "faulty speakers.",
        "advice": "Check volume/mute settings, update the audio driver, and test "
                   "with headphones to isolate a speaker fault.",
    },
    {
        "id": "R20",
        "symptoms": {"screen_flickering"},
        "diagnosis": "Display Cable or GPU Driver Issue",
        "explanation": "Intermittent flickering is commonly caused by a loose "
                        "display cable or an outdated/corrupted graphics driver.",
        "advice": "Reseat the display cable and update the graphics card driver.",
    },
    {
        "id": "R21",
        "symptoms": {"usb_not_detected"},
        "diagnosis": "USB Port or Driver Issue",
        "explanation": "Devices not being detected over USB typically indicates a "
                        "faulty port, damaged cable, or outdated USB driver.",
        "advice": "Try a different USB port/cable and update USB controller "
                   "drivers via Device Manager.",
    },
    {
        "id": "R22",
        "symptoms": {"software_crash"},
        "diagnosis": "Corrupted Application or Compatibility Issue",
        "explanation": "A single application crashing repeatedly, while the rest "
                        "of the system works fine, points to a corrupted "
                        "installation or a compatibility problem with that app.",
        "advice": "Reinstall the application, check for updates, and verify it "
                   "is compatible with your operating system version.",
    },
]