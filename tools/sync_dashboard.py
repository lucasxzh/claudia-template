import os
import datetime

# Configuration
HABITS_DIR = "habits"
DASHBOARD_FILE = os.path.join(HABITS_DIR, "dashboard.md")

def get_habit_status(habit_path):
    tracker_path = os.path.join(habit_path, "tracker.md")
    
    if not os.path.exists(tracker_path):
        return {"streak": 0, "last_date": "N/A", "status": "N/A"}

    with open(tracker_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Filter for table rows (lines starting with | and not header/separator)
    data_rows = [line for line in lines if line.strip().startswith("|") and "---" not in line and "Date" not in line]
    
    if not data_rows:
        return {"streak": 0, "last_date": "None", "status": "New"}

    # Parse rows to find streak
    # Format expected: | YYYY-MM-DD | Status | ...
    # Status expected: ✅, ❌, ⏸️
    
    streak = 0
    # Reverse loop to count streak from most recent entry
    for row in reversed(data_rows):
        parts = [p.strip() for p in row.split("|")]
        if len(parts) < 3: continue
        
        status_icon = parts[2]
        
        if "✅" in status_icon:
            streak += 1
        elif "⏸️" in status_icon:
            continue # Skip paused days, don't break streak
        else:
            break # Break streak on failure or other symbol

    # Get details of the very last entry
    last_row = data_rows[-1]
    last_row_parts = [p.strip() for p in last_row.split("|") if p.strip()]
    last_date = last_row_parts[0] if len(last_row_parts) > 0 else "N/A"
    last_status = last_row_parts[1] if len(last_row_parts) > 1 else "?"

    return {"streak": streak, "last_date": last_date, "status": last_status}

def calculate_system_streak(habits):
    # Collect every single date logged across all habits
    all_dates = set()
    
    for habit in habits:
        tracker_path = os.path.join(HABITS_DIR, habit, "tracker.md")
        if not os.path.exists(tracker_path): continue
        
        with open(tracker_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Extract dates from rows like "| 2023-10-27 | ✅ | ..."
        for line in lines:
            if line.strip().startswith("|") and "---" not in line and "Date" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 1:
                    # Clean the date string
                    date_str = parts[1] if parts[0] == '' else parts[0]
                    # Handle cases where split might leave empty string at start if line starts with |
                    # usually split("|") on "| date |" gives ['', ' date ', '']
                    # Let's be robust: find the part that looks like a date?
                    # Or just assume index 1 if line starts with |
                    # The parts list logic in get_habit_status was: [p.strip() for p in row.split("|")]
                    # For "| 2023-01-01 |", split gives ['', '2023-01-01', '']
                    # So date is at index 1.
                    if len(parts) > 1 and parts[1]: 
                        all_dates.add(parts[1])
    
    # Sort dates and calculate streak
    sorted_dates = sorted(list(all_dates))
    if not sorted_dates: return 0

    date_objs = []
    for d in sorted_dates:
        try:
            date_objs.append(datetime.datetime.strptime(d, "%Y-%m-%d").date())
        except ValueError:
            continue
        
    current_streak = 0
    today = datetime.date.today()
    
    # Check if we have an entry for today or yesterday to keep streak alive
    if today in date_objs:
        current_streak = 1
        check_date = today - datetime.timedelta(days=1)
    elif (today - datetime.timedelta(days=1)) in date_objs:
        check_date = today - datetime.timedelta(days=1)
        # Only count if yesterday exists, start counting from yesterday
        current_streak = 0 
        # Wait, if today is missing but yesterday exists, streak is alive but counter starts at yesterday?
        # Standard logic: Streak is unbroken sequence ending at Today or Yesterday.
        # If Today is missing, Streak = Count ending at Yesterday.
    else:
        return 0 # Streak broken
        
    # Recalculate correctly based on standard logic
    # If today is present, sequence includes today.
    # If today is absent, but yesterday is present, sequence includes yesterday.
    
    last_active_date = None
    if today in date_objs:
        last_active_date = today
    elif (today - datetime.timedelta(days=1)) in date_objs:
        last_active_date = today - datetime.timedelta(days=1)
    
    if not last_active_date:
        return 0
        
    current_streak = 0
    check_date = last_active_date
    while check_date in date_objs:
        current_streak += 1
        check_date -= datetime.timedelta(days=1)
        
    return current_streak

def generate_dashboard():
    if not os.path.exists(HABITS_DIR):
        os.makedirs(HABITS_DIR)

    habits = [d for d in os.listdir(HABITS_DIR) if os.path.isdir(os.path.join(HABITS_DIR, d))]
    
    # Calculate the Meta-Streak
    system_streak = calculate_system_streak(habits)
    
    # Add Visual Feedback for the System Streak
    streak_banner = f"## ⚡ System Consistency: {system_streak} Days"
    if system_streak > 7: streak_banner += " (On Fire! 🔥)"
    
    dashboard_content = [
        "# 📊 Life Dashboard\n",
        streak_banner + "\n", 
        f"*Last Sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "| Habit | Current Streak | Last Logged | Latest Status |",
        "| :--- | :---: | :--- | :---: |"
    ]

    for habit in habits:
        stats = get_habit_status(os.path.join(HABITS_DIR, habit))
        # Add fire emoji for streaks > 3
        streak_display = f"🔥 {stats['streak']}" if stats['streak'] > 3 else str(stats['streak'])
        
        row = f"| **{habit.replace('-', ' ').title()}** | {streak_display} | {stats['last_date']} | {stats['status']} |"
        dashboard_content.append(row)

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(dashboard_content))
    
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    generate_dashboard()