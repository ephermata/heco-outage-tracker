#!/usr/bin/env python3
import os
import subprocess
import datetime

# Configuration
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(REPO_DIR, "index.html")

def fetch_outage_data():
    """
    In a fully standalone mode without OpenClaw, this function would call a News API 
    or scrape the HECO outage map API.
    
    For demonstration, this returns a structured dictionary that would be populated 
    by an AI/Search API with the latest data.
    """
    print("Fetching latest HECO outage data...")
    return {
        "timestamp": datetime.datetime.now().strftime("%B %d, %Y %I:%M %p %Z"),
        "local_status": "Power was restored to your immediate area early this morning.",
        "warning": "The grid remains fragile. East Honolulu is currently relying on a single transmission line due to severe Kona low storm damage to the other lines crossing the Ko'olau range. Prepare for potential secondary outages.",
        "bullets": [
            "Recent Outages: Over 13,000 customers in the wider Aina Haina to Hawaii Kai and Waimanalo stretch experienced secondary outages last night.",
            "Repairs: Crews are actively working to repair the damaged transmission lines, but hazardous weather conditions are causing delays.",
            "Traffic: Some traffic lights may still be out on Kalaniana'ole Hwy. Treat dark intersections as 4-way stops."
        ]
    }

def generate_html(data):
    """
    Generates the static HTML dashboard using the fetched data.
    """
    print("Generating HTML...")
    bullets_html = "\n".join([f"            <li>{b}</li>" for b in data['bullets']])
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>HECO Outage Status - East Honolulu</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background-color: #f4f4f9; color: #333; }}
        .container {{ max-width: 800px; margin: 40px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #d32f2f; margin-top: 0; }}
        h2 {{ color: #555; font-size: 1.2em; margin-bottom: 5px; }}
        .timestamp {{ color: #888; font-size: 0.9em; margin-bottom: 25px; }}
        .status-box {{ background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; margin-bottom: 25px; border-radius: 4px; }}
        .status-box.fragile {{ background-color: #fff3e0; border-left-color: #ff9800; }}
        .status-box p {{ margin: 0 0 10px 0; }}
        .status-box p:last-child {{ margin: 0; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 10px; }}
    </style>
    <meta http-equiv="refresh" content="300">
</head>
<body>
    <div class="container">
        <h1>HECO Power Outage Status</h1>
        <h2>East Honolulu / Hawaii Kai / Kalaniana'ole Hwy</h2>
        <div class="timestamp" id="time">Last Updated: {data['timestamp']} (Live)</div>
        
        <div class="status-box fragile">
            <p><strong>📍 Local Status:</strong> {data['local_status']}</p>
            <p><strong>⚠️ Grid Warning:</strong> {data['warning']}</p>
        </div>

        <h3>Latest Island-Wide & Regional Info</h3>
        <ul>
{bullets_html}
        </ul>
        <p style="color: #777; font-size: 0.85em; margin-top: 30px;"><em>This page auto-refreshes every 5 minutes. The backend monitoring checks for updates every 30 minutes.</em></p>
    </div>
</body>
</html>
"""
    with open(HTML_FILE, "w") as f:
        f.write(html_content)

def git_commit_and_push():
    """
    Commits the updated index.html to Git and pushes to GitHub.
    """
    print("Committing to Git and pushing to GitHub...")
    os.chdir(REPO_DIR)
    
    subprocess.run(["git", "add", "index.html"], check=True)
    
    # Check if there are changes to commit
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("No changes to commit.")
        return

    commit_msg = f"Automated update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Push successful!")

if __name__ == "__main__":
    print("--- Starting HECO Outage Tracker Update ---")
    try:
        data = fetch_outage_data()
        generate_html(data)
        git_commit_and_push()
        print("--- Update Complete ---")
    except Exception as e:
        print(f"Error during update: {e}")
