# Claudia — AI Habit Coach Template

A habit tracking system powered by an AI accountability partner. Open the project in your preferred AI code assistant and start chatting — your coach will guide you through logging habits, reflecting on patterns, and maintaining streaks.

## How It Works

1. **Open this project in Cursor or Claude Code** and start a conversation.
2. Your coach reads the dashboard, asks about your day, and logs your habits.
3. Streaks, statuses, and patterns are tracked automatically.

## Project Structure

```
habits/
├── dashboard.md              # Auto-generated overview of all habits
├── daily-journal/            # Example habit: daily journaling
│   ├── context.md            # Rules and interaction protocols
│   ├── tracker.md            # Date/status log
│   └── entries/              # Individual journal entries (by month)
└── morning-run/              # Example habit: morning exercise
    ├── context.md            # Rules and interaction protocols
    ├── tracker.md            # Date/status log
    └── journal.md            # Freeform notes and reflections
tools/
└── sync_dashboard.py         # Syncs tracker data → dashboard.md
.cursor/
└── rules/
    └── context.md            # Agent persona and behavior rules
```

## Adding a New Habit (You can just ask AI to do this)

1. Create a folder under `habits/` (e.g. `habits/meditation/`).
2. Add a `context.md` defining the habit's purpose, frequency, and rules.
3. Add an empty `tracker.md` with the table header:
   ```
   | Date | Status | Note |
   | :--- | :---: | :--- |
   ```
4. Optionally add a `journal.md` for freeform notes.
5. Tell your coach about the new habit — it will pick it up automatically.

## Status Key

- ✅ Done
- ❌ Missed
- ⏸️ Skipped (e.g. rest day, sick)

## Customization

- **Agent persona:** Edit `.cursor/rules/context.md` to change the coach's tone, philosophy, or interaction style.
- **Habit rules:** Each habit's `context.md` controls how the agent interacts with that specific habit (frequency, backup protocols, coaching output, etc.).
- **Dashboard sync:** `tools/sync_dashboard.py` runs automatically after updates. No configuration needed.
