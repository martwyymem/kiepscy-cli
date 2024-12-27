import os
import subprocess
import re
import random

def load_links(file_path):
    """Load episodes grouped by season from a .txt file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return {}

    seasons = {}
    current_season = None
    url_pattern = re.compile(r'^https?://')

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.upper().startswith("SEZON"):
                current_season = line
                seasons[current_season] = []
            elif line and not url_pattern.match(line):
                # Treat as episode name
                current_name = line
            elif url_pattern.match(line):
                # Treat as URL
                if current_season and current_name:
                    seasons[current_season].append((current_name, line))
                    current_name = None

    print("Loaded seasons and episodes:")
    for season, episodes in seasons.items():
        print(f"{season}:")
        for name, link in episodes:
            print(f"  {name} ({link})")

    return seasons

def display_seasons(seasons):
    """Display a list of seasons for the user to choose from."""
    print("Available Seasons:")
    for i, season in enumerate(seasons.keys(), 1):
        print(f"{i}. {season}")

def display_menu(episodes):
    """Display a menu of episode names for the user to choose from."""
    print("Available Episodes:")
    for i, (name, _) in enumerate(episodes, 1):
        print(f"{i}. {name}")

def play_link(link):
    """Play the selected link using mpv."""
    print(f"Debug: Playing link - {link}")
    try:
        subprocess.run(["mpv", link])
    except FileNotFoundError:
        print("Error: 'mpv' player is not installed or not in PATH.")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\nMain Menu:")
        print("1. Wybierz Sezon")
        print("2. Wybierz Odcinek")
        print("3. Losuj Odcinek")
        print("4. Wyjdź")

        choice = input("Wybierz: ").strip()

        if choice == '1':
            choose_season()
        elif choice == '2':
            choose_episode()
        elif choice == '3':
            randomise_episode()
        elif choice == '4':
            print("Żegnaj w morde jeża!")
            break
        else:
            print("Nieprawidłowa opca.")

def choose_season():
    """Allow the user to choose a season and then an episode to play."""
    txt_file = "links.txt"  # Path to the .txt file containing links

    seasons = load_links(txt_file)
    if not seasons:
        print("Nie wczytano sezonów.")
        return

    display_seasons(seasons)
    choice = input("Wybierz numer Sezonu: ").strip()

    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(seasons):
            selected_season = list(seasons.keys())[index - 1]
            print(f"Selected Season: {selected_season}")

            episodes = seasons[selected_season]
            display_menu(episodes)

            ep_choice = input("Wybierz numer odcina z sezonu: ").strip()
            if ep_choice.isdigit():
                ep_index = int(ep_choice)
                if 1 <= ep_index <= len(episodes):
                    selected_name, selected_link = episodes[ep_index - 1]
                    print(f"Playing: {selected_name}")
                    play_link(selected_link)
                else:
                    print(f"Nie ma takiego odcinka: {ep_index}. Proszę wybrać odcinek między 1, a {len(episodes)}.")
            else:
                print("Nie ma takiego sezonu. Proszę podać właściwy sezon.")
        else:
            print(f"Nie ma takiego odcinka: {ep_index}. Proszę wybrać odcinek między 1, a {len(episodes)}.")
    else:
        print("Nie ma takiego sezonu. Proszę podać właściwy sezon.")

def choose_episode():
    """Allow the user to choose an episode to play from all seasons."""
    txt_file = "links.txt"  # Path to the .txt file containing links

    seasons = load_links(txt_file)
    if not seasons:
        print("Nie wczytano listy odcinków")
        return

    all_episodes = [(name, link) for episodes in seasons.values() for name, link in episodes]
    display_menu(all_episodes)
    choice = input("Podaj numer odcinka: ").strip()

    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(all_episodes):
            selected_name, selected_link = all_episodes[index - 1]
            print(f"Odtwarzanie: {selected_name}")
            play_link(selected_link)
        else:
            print(f"Nie ma takiego odcinka: {ep_index}. Proszę wybrać odcinek między 1, a {len(episodes)}.")
    else:
        print("Nieprawidłowyy wybór, proszę podać właściwą liczbę.")

def randomise_episode():
    """Randomly select and play an episode."""
    txt_file = "links.txt"  # Path to the .txt file containing links

    seasons = load_links(txt_file)
    if not seasons:
        print("Nie wczytano listy odcinków")
        return

    all_episodes = [(name, link) for episodes in seasons.values() for name, link in episodes]
    selected_name, selected_link = random.choice(all_episodes)
    print(f"Losowo wybrany odcinek to: {selected_name}")
    play_link(selected_link)

if __name__ == "__main__":
    main_menu()
