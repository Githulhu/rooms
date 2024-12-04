# Begrüßungsschleife bei Beginn des Spiels
def greeting():
    print("Willkommen in deinem Abenteuer!")
    print("Du befindest dich in einem verlassenen, verfallenen Haus.")
    print("Finde einen Weg nach draußen!")
    print("Viel Erfolg!\n")

# Räume und deren Eigenschaften
rooms = {
    "foyer": {
        "description": """Du befindest dich im Foyer des alten Hauses. Es ist dunkel, muffig und stickig. 
        Ein alter Kronleuchter hängt von der Decke, und die Tapeten lösen sich von den Wänden. 
        Es gibt Türen in Richtung Norden und Osten. Ein Schlüssel liegt auf einem kleinen Tisch.""",
        "items": ["Schlüssel"],
        "exits": {"norden": "library", "osten": "kitchen"},
        "pois": {
            "kronleuchter": "Ein alter, staubiger Kronleuchter hängt von der Decke.",
            "schrank": "Ein reich verzierter Schrank, der verschlossen ist."
        },
        "diary_in_closet": True  # Zustandsvariable für den Schrank
    },
    "library": {
        "description": """Du befindest dich offensichtlich in einer Bibliothek. Überall sind Bücherregale, in denen verstaubte Bücher stehen.
        Es gibt nur die eine Tür in Richtung Süden, zum Foyer. Ein Buch scheint besonders abgenutzt zu sein.""",
        "items": ["Buch"],
        "exits": {"süden": "foyer"},
        "pois": {"bücherregal": "Ein großes Bücherregal voller verstaubter Bücher."}
    },
    "kitchen": {
        "description": """Dem Geruch nach zu urteilen, befindest du dich in der Küche. Über allem liegt der Gestank von verdorbenem Essen. 
        Fette Fliegen summen, ein Wasserhahn tropft träge in eine rostige Spüle. 
        Es gibt Türen in Richtung Westen, zurück zum Foyer und Norden, die scheinbar in einen Wintergarten führt. Ein Messer liegt auf der Arbeitsfläche.""",
        "items": ["Messer"],
        "exits": {"westen": "foyer", "norden": "garden"},
        "pois": {"wasserhahn": "Ein alter Wasserhahn, der träge in eine rostige Spüle tropft."}
    },
    "garden": {
        "description": """Es ist kalt, zugig und es stinkt nach Unkraut, Kompost und Humus. Du bist eindeutig im Wintergarten.
        Es gibt eine Tür in Richtung Süden zur Küche. Eine Gartenschere liegt auf dem Boden.""",
        "items": ["Gartenschere"],
        "exits": {"süden": "kitchen"},
        "pois": {"brunnen": "Ein alter Brunnen, der im Zentrum des Wintergartens steht."}
    }
}

# Interaktionen zwischen Gegenständen und POIs
interactions = {
    "foyer": {
        "schlüssel": {
            "schrank": {
                "message": "Du benutzt den Schlüssel, um den reich verzierten Schrank zu öffnen. Im Inneren findest du ein altes Tagebuch.",
                "add_items": ["Tagebuch"],
                "remove_items": ["Schlüssel"],
                "update_poi": "Ein reich verzierter Schrank, der nun geöffnet ist. Das Tagebuch liegt darin."
            }
        }
    }
}

# Aktueller Raum und Inventar des Spielers
current_room = "foyer"
inventory = []

# Funktion zur Beschreibung des aktuellen Raums
def describe_room():
    room = rooms[current_room]
    print(room["description"])
    
    if current_room == "foyer":
        if room["diary_in_closet"]:
            print("Ein reich verzierter Schrank, der verschlossen ist und ein Tagebuch enthält.")
        else:
            print("Ein reich verzierter Schrank, der nun geöffnet ist und kein Tagebuch mehr enthält.")

# Funktion zur Verwaltung des Inventars
def add_to_inventory(item):
    inventory.append(item)
    print(f"Du hast {item} aufgenommen.")

def remove_from_inventory(item):
    if item in inventory:
        inventory.remove(item)
        print(f"Du hast {item} aus deinem Inventar entfernt.")
    else:
        print(f"{item} ist nicht in deinem Inventar.")

def show_inventory():
    if inventory:
        print("Deine Tasche enthält:")
        for item in inventory:
            print(f" - {item}")
    else:
        print("Dein Inventar ist leer.")

# Funktion zur Verwaltung von Gegenständen und POIs
def pick_up_item(item):
    normalized_item = item.strip().lower()
    normalized_items = [i.lower() for i in rooms[current_room]["items"]]
    
    if normalized_item in normalized_items:
        exact_item = rooms[current_room]["items"][normalized_items.index(normalized_item)]
        rooms[current_room]["items"].remove(exact_item)
        add_to_inventory(exact_item)
        
        # Überprüfe, ob das Tagebuch aus dem Schrank genommen wird
        if current_room == "foyer" and normalized_item == "tagebuch":
            rooms[current_room]["diary_in_closet"] = False
    else:
        print("Dieser Gegenstand befindet sich nicht im Raum.")

def examine_poi(poi):
    normalized_poi = poi.strip().lower()
    if normalized_poi in rooms[current_room]["pois"]:
        print(rooms[current_room]["pois"][normalized_poi])
    else:
        print("Dieser Punkt ist hier nicht zu finden.")

def use_item_with_poi(item, poi):
    normalized_item = item.strip().lower()
    normalized_poi = poi.strip().lower()
    
    normalized_inventory = [i.lower() for i in inventory]
    if normalized_item not in normalized_inventory:
        print(f"Du hast keinen {item}.")
        return
    
    if normalized_poi not in rooms[current_room]["pois"]:
        print(f"Hier gibt es keinen {poi}.")
        return
    
    room_interactions = interactions.get(current_room, {})
    item_interactions = room_interactions.get(normalized_item, {})
    interaction = item_interactions.get(normalized_poi, None)
    
    if interaction:
        print(interaction["message"])
        
        for new_item in interaction.get("add_items", []):
            rooms[current_room]["items"].append(new_item)
        
        for remove_item in interaction.get("remove_items", []):
            if remove_item in inventory:
                inventory.remove(remove_item)
        
        if "update_poi" in interaction:
            rooms[current_room]["pois"][normalized_poi] = interaction["update_poi"]
    else:
        print("Du kannst das nicht tun.")

def move_player(direction):
    global current_room
    if direction in rooms[current_room]["exits"]:
        current_room = rooms[current_room]["exits"][direction]
    else:
        print("Ungültige Richtung. Versuche 'norden', 'osten', 'süden', 'westen'.")

# Neue Funktionen für die Modularisierung
def start_game():
    greeting()

def describe_current_room():
    describe_room()

def handle_command(command, argument):
    if command == "inventar":
        handle_show_inventory()
    elif command == "raum":
        handle_describe_room()
    elif command == "nimm":
        handle_pick_up_item(argument)
    elif command == "drop":
        handle_remove_from_inventory(argument)
    elif command == "untersuche":
        handle_examine_poi(argument)
    elif command == "benutze":
        handle_use_item_with_poi(argument)
    elif command in ["norden", "osten", "süden", "westen"]:
        handle_move_player(command)
    else:
        handle_invalid_command()

def handle_show_inventory():
    show_inventory()

def handle_describe_room():
    describe_room()

def handle_pick_up_item(item):
    pick_up_item(item)

def handle_remove_from_inventory(item):
    remove_from_inventory(item)

def handle_examine_poi(poi):
    examine_poi(poi)

def handle_use_item_with_poi(argument):
    item_poi = argument.split(" mit ", 1)
    if len(item_poi) == 2:
        use_item_with_poi(item_poi[0], item_poi[1])
    else:
        print("Ungültiger Befehl. Versuche 'benutze [Gegenstand] mit [Punkt]'.")

def handle_move_player(direction):
    global room_changed
    move_player(direction)
    room_changed = True

def handle_invalid_command():
    print("Ungültiger Befehl. Versuche 'nimm [Gegenstand]', 'drop [Gegenstand]', 'untersuche [Punkt]', 'benutze [Gegenstand] mit [Punkt]', 'inventar', 'raum' oder eine Richtung (norden, osten, süden, westen).")

# Hauptspielschleife
def game():
    start_game()
    global room_changed
    room_changed = True

    while True:
        if room_changed:
            describe_current_room()
            room_changed = False
        
        command = input("\nWas möchtest du tun? ").strip().lower()
        command_parts = command.split(" ", 1)
        base_command = command_parts[0]
        argument = command_parts[1] if len(command_parts) > 1 else ""

        handle_command(base_command, argument)
        print("\n")

# Starte das Spiel
game()
