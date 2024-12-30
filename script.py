import requests
from termcolor import colored
from collections import Counter

def fetch_game_name(app_id):
    """Fetch the game name for the given Steam App ID."""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get(str(app_id), {}).get('success', False):
            return data[str(app_id)]['data']['name']
        else:
            return None
    except Exception as e:
        return f"Error fetching details: {e}"

def main():
    # Read game IDs from the file
    try:
        with open("game_ids.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        print("Error: game_ids.txt file not found.")
        return

    # Split IDs and process each one
    game_ids = [game_id.strip() for game_id in content.split(",") if game_id.strip().isdigit()]
    duplicates = Counter(game_ids)

    processed_ids = []
    for index, game_id in enumerate(game_ids, start=1):
        game_name = fetch_game_name(game_id)
        if game_name:
            print(f"({index}) {colored(game_id, 'green')} => {colored(game_name, 'red')}")
        else:
            print(f"({index}) {colored(game_id, 'green')} => {colored('Not Found', 'blue')}")
        processed_ids.append((game_id, game_name))

    # Print duplicates section
    print("\nDuplicates =>")
    for app_id, count in duplicates.items():
        if count > 1:
            game_name = next((name for id, name in processed_ids if id == app_id), "Not Found")
            print(f"{colored(f'({app_id})', 'green')} x {count} {colored(f'({game_name})', 'red')}" )

if __name__ == "__main__":
    main()
