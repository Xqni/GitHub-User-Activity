import requests
import json
import csv


EVENTSFILE = "events.json"
CSVFILE = "events.csv"


def get_status_code(response):
    return response.status_code


# Displays GitHub activity
def display_info(username):
    # Get events from API
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    # Check status
    if get_status_code(response) != 200:
        print(f"\n - No GitHub activity for {username}\n")
        return

    # Get JSON from response
    response = response.json()

    # Check if list is empty
    if response == []:
        print(f"\n - No GitHub activity for {username}\n")
        return

    # First, group events by type
    _, events = sort_events(response)

    # Load verb mappings from CSV into a dictionary
    verb_map = {}
    with open(CSVFILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            verb_map[row[0]] = row[1]  # row[0]: Event type, row[1]: Verb

    # Display info
    print(f"\nGitHub activity for {username.capitalize()}")
    for event_group in events:
        for event_type, event_list in event_group.items():
            verb = verb_map.get(event_type)
            count = len(event_list)
            if count > 0:
                repo_name = event_list[0].get(
                    "repo", {}).get("name", "a repository")
                print(f" - {verb} {count} times to {repo_name}")
    print()


# Sort events
def sort_events(response):
    events_by_type = {}

    for event in response:
        event_type = event["type"]
        if event_type not in events_by_type:
            events_by_type[event_type] = []
        events_by_type[event_type].append(event)

    # Convert to list of dictionaries
    events = [{event_type: events_list}
              for event_type, events_list in events_by_type.items()]

    with open(EVENTSFILE, "w") as f:
        json.dump(events, f, indent=4)

    return list(events_by_type.keys()), events


def main():
    print("Welcome, type a username to see GitHub activity.\n- Type 'quit' or 'q' to exit.\n")
    try:
        while True:
            username = input("github-activity: ").strip()
            username = username.lower()
            if username in ["quit", "q"]:
                print(" - User Interruption. Exiting program\n")
                break

            # if username is not quit/q
            display_info(username)
            continue

    # Ctrl+C
    except KeyboardInterrupt:
        print("\n - User Interruption. Exiting program\n")


if __name__ == "__main__":
    main()
