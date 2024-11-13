import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from time import sleep

@dataclass
class Character:
    name: str
    char_class: str
    health: int
    max_health: int
    strength: int
    agility: int
    magic: int
    inventory: List[str]
    current_location: str
    story_choices: List[str]
    quests_completed: List[str]
    active_quests: List[str]
    quest_progress: Dict[str, int]

class CrystalKingdoms:
    def __init__(self):
        self.player: Optional[Character] = None
        self.final = False
        self.fighting_skekso = False
        self.game_running = True
        self.character_classes = {
            "warrior": {"health": 100, "strength": 8, "agility": 5, "magic": 2},
            "mage": {"health": 70, "strength": 3, "agility": 4, "magic": 9},
            "rogue": {"health": 80, "strength": 5, "agility": 8, "magic": 4}
        }
        self.items = {
            "health_potion": {"type": "consumable", "effect": "heal", "value": 30},
            "magic_scroll": {"type": "consumable", "effect": "magic_boost", "value": 5},
            "crystal_shard": {"type": "key_item", "effect": "story"},
            "ancient_sword": {"type": "weapon", "effect": "strength_boost", "value": 3},
            "elven_heirloom": {"type": "key_item", "effect": "story"},
            "purified_crystal": {"type": "key_item", "effect": "story"}
        }
        self.locations = {
            "crystal_cave": {
                "description": "A luminous cave filled with glowing crystals.",
                "enemies": ["Crystal Guardian", "Shadow Lurker"],
                "items": ["crystal_shard", "health_potion"],
                "npcs": [{"name": "Wise Crystalreach Sage", "quests": ["Cleanse the Corrupted Crystals"]}]
            },
            "haunted_forest": {
                "description": "An eerie forest where shadows move on their own.",
                "enemies": ["Dark Wisp", "Corrupted Treant"],
                "items": ["magic_scroll", "ancient_sword", "elven_heirloom"],
                "npcs": [
                    {"name": "Elven Ranger", "quests": ["Purge the Dark Forces", "Retrieve Stolen Elven Heirloom"]}
                ]
            },
            "corrupted_castle": {
                "description": "Once majestic, now twisted by dark magic.",
                "enemies": ["Dark Knight", "Shadow Mage"],
                "items": ["health_potion", "crystal_shard"],
                "npcs": [{"name": "Fallen Prince", "quests": ["Reclaim the Corrupted Throne"]}]
            }
        }
        self.enemies = {
            "Crystal Guardian": {"health": 50, "strength": 5, "agility": 4, "name": "Crystal Guardian"},
            "Shadow Lurker": {"health": 30, "strength": 7, "agility": 6, "name": "Shadow Lurker"},
            "Dark Wisp": {"health": 40, "strength": 4, "agility": 8, "name": "Dark Wisp"},
            "Corrupted Treant": {"health": 60, "strength": 6, "agility": 3, "name": "Corrupted Treant"},
            "Dark Knight": {"health": 70, "strength": 8, "agility": 5, "name": "Dark Knight"},
            "Shadow Mage": {"health": 45, "strength": 3, "agility": 4, "name": "Shadow Mage"},
            "Emperor SkekSo": {"health": 300, "strength": 15, "agility": 7, "name": "Emperor SkekSo"}
        }
        self.quest_data = {
            "Cleanse the Corrupted Crystals": {
                "requires": [],
                "enemy_kills": {"Crystal Guardian": 2},
                "items_needed": ["crystal_shard"],
                "reward": "purified_crystal",
                "progress_max": 2
            },
            "Purge the Dark Forces": {
                "requires": ["Cleanse the Corrupted Crystals"],
                "enemy_kills": {"Dark Wisp": 3, "Corrupted Treant": 1},
                "items_needed": [],
                "reward": "magic_scroll",
                "progress_max": 4
            },
            "Retrieve Stolen Elven Heirloom": {
                "requires": ["Purge the Dark Forces"],
                "enemy_kills": {},
                "items_needed": ["elven_heirloom"],
                "reward": "ancient_sword",
                "progress_max": 1
            },
            "Reclaim the Corrupted Throne": {
                "requires": ["Retrieve Stolen Elven Heirloom"],
                "enemy_kills": {"Dark Knight": 1, "Shadow Mage": 1, "Emperor SkekSo": 1},
                "items_needed": ["purified_crystal"],
                "reward": None,
                "progress_max": 2
            }
        }

    def start_game(self):
        """Initialize and start the game"""
        print("\n" + "="*50)
        print("Welcome to The Crystal Kingdoms!")
        print("="*50)
        print("\nIn a realm where three kingdoms once maintained peace through sacred crystals,")
        print("darkness now spreads across the land. As a brave adventurer, you must restore")
        print("balance to the kingdoms and choose your path carefully...")
        print("\nYour choices and completed quests will determine your ultimate destiny.")
        
        self.create_character()
        self.game_loop()

    def create_character(self):
        """Create a new character"""
        print("\n=== Character Creation ===")
        name = input("Enter your character's name: ").strip()
        char_class = self.choose_class()
        stats = self.character_classes[char_class]
        self.player = Character(
            name=name,
            char_class=char_class,
            health=stats['health'],
            max_health=stats['health'],
            strength=stats['strength'],
            agility=stats['agility'],
            magic=stats['magic'],
            inventory=["health_potion"],
            current_location="crystal_cave",
            story_choices=[],
            quests_completed=[],
            active_quests=[],
            quest_progress={}
        )
        print(f"\nWelcome, {name} the {char_class.title()}!")
        print(f"\nYou begin your journey in the Crystal Cave...")

    def choose_class(self):
        """Let the player choose their character class"""
        print("\nAvailable Classes:")
        for class_name, stats in self.character_classes.items():
            print(f"\n{class_name.title()}:")
            for stat, value in stats.items():
                print(f"  {stat.title()}: {value}")
        
        while True:
            choice = input("\nChoose your class (warrior/mage/rogue): ").lower()
            if choice in self.character_classes:
                return choice
            print("Invalid class choice. Please try again.")

    def game_loop(self):
        """Main game loop"""
        while self.game_running and not self.check_game_over():
            self.show_status()
            self.handle_player_turn()
            sleep(1.5)

    def show_status(self):
        """Display current game status"""
        print("\n" + "="*50)
        print(f"Location: {self.player.current_location.replace('_', ' ').title()}")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Inventory: {', '.join(item.replace('_', ' ').title() for item in self.player.inventory) or 'Empty'}")
        
        # Display Active Quests with detailed progress
        if self.player.active_quests:
            print("\n=== Active Quests ===")
            for quest in self.player.active_quests:
                quest_data = self.quest_data[quest]
                progress = self.player.quest_progress.get(quest, 0)
                max_progress = quest_data["progress_max"]
                print(f"\n- {quest} ({progress}/{max_progress})")
                
                # Show enemy kills needed
                if quest_data["enemy_kills"]:
                    print("  Required kills:")
                    for enemy, count in quest_data["enemy_kills"].items():
                        current_kills = min(progress, count)  # Estimate kills based on progress
                        print(f"  - {enemy}: {current_kills}/{count}")
                
                # Show items needed
                if quest_data["items_needed"]:
                    print("  Required items:")
                    for item in quest_data["items_needed"]:
                        has_item = item in self.player.inventory
                        status = "✓" if has_item else "✗"
                        print(f"  - {item.replace('_', ' ')}: {status}")
                
                # Show reward if any
                if quest_data["reward"]:
                    print(f"  Reward: {quest_data['reward'].replace('_', ' ')}")
        
        # Display Completed Quests
        if self.player.quests_completed:
            print("\n=== Completed Quests ===")
            for quest in self.player.quests_completed:
                print(f"✓ {quest}")
        
        # Display Available Quests (not taken but prerequisites met)
        available_quests = [
            quest for quest, data in self.quest_data.items()
            if quest not in self.player.active_quests 
            and quest not in self.player.quests_completed
            and all(req in self.player.quests_completed for req in data["requires"])
        ]
        if available_quests:
            print("\n=== Available Quests ===")
            for quest in available_quests:
                print(f"! {quest}")
        
        print("="*50)
        print("\nActions:")
        print("1. Explore")
        print("2. Use item")
        print("3. Move to new location")
        print("4. Rest")
        print("5. Talk to NPCs")
        print("6. Quit game")
        if self.final:
            print("7. Fight Emperor SkekSo")

    def handle_player_turn(self):
        """Handle player's turn"""
        actions = {
            "1": self.explore,
            "2": self.use_item,
            "3": self.change_location,
            "4": self.rest,
            "5": self.talk_to_npcs,
            "6": self.quit_game,
            "7": self.fight_skekso
        }
        
        choice = input("\nWhat would you like to do? (1-6): ")
        if choice == '7' and not self.final:
            choice = '8'
        if choice in actions:
            actions[choice]()
        else:
            print("\nInvalid choice. Please try again.")

    def handle_item_effect(self, item: str):
        if item:
            used = False
            item_data = self.items[item]
            if item_data["type"] == "consumable":
                if item_data["effect"] == "heal":
                    self.player.health = min(self.player.max_health, self.player.health + item_data["value"])
                    print(f"\nHealed for {item_data['value']} health!")
                    used = True
                elif item_data["effect"] == "magic_boost":
                    self.player.magic += item_data["value"]
                    print(f"\nMagic increased by {item_data['value']}!")
                    used = True
            elif item_data["type"] == "weapon":
                self.player.strength += item_data["value"]
                print(f"\nStrength increased by {item_data['value']}!")
                used = True
            elif item_data["type"] == "key_item":
                throw_away = input("\nYou cannot use this item, do you wish to throw it away? WARNING: YOU CANNOT UNDO THIS ACTION (y/n): ")
                if throw_away[0] == 'y':
                    used = True
            if used:
                self.player.inventory.remove(item)
    
    def explore(self):
        location = self.locations[self.player.current_location]
        print(f"\n{location['description']}")
        if random.random() < 0.7:  # 70% chance of an event
            if random.random() < 0.6:  # 60% chance of combat
                self.combat(random.choice(location['enemies']))
            else:
                self.find_item()
        else:
            print("\nYou explore the area but find nothing of interest.")

    def combat(self, enemy_name: str):
        enemy = self.enemies[enemy_name].copy()
        enemy['current_health'] = enemy['health']
        if not self.fighting_skekso:
            print(f"\nYou encounter a {enemy_name}!")
        else:
            print("\nOMG ITS SKEKSO")
        
        while enemy['current_health'] > 0 and self.player.health > 0:
            self.display_health(enemy)
            fled = self.do_combat_action(enemy)
            if fled:
                break

        if enemy['current_health'] <= 0:
            print(f"\nYou defeated the {enemy_name}!")
            # Update quest progress for enemy kills
            for quest in self.player.active_quests:
                quest_data = self.quest_data[quest]
                if enemy_name in quest_data["enemy_kills"]:
                    self.player.quest_progress[quest] = min(
                        quest_data["progress_max"],
                        self.player.quest_progress.get(quest, 0) + 1
                    )
                    current_progress = self.player.quest_progress[quest]
                    max_progress = quest_data["progress_max"]
                    print(f"\nQuest progress updated: {quest} ({current_progress}/{max_progress})")
                    
            self.check_all_quests()

    def display_health(self, enemy):
        print(f"\nYour Health: {self.player.health}/{self.player.max_health}")
        print(f"{enemy['name']} Health: {enemy['current_health']}/{enemy['health']}")

    def do_combat_action(self, enemy):
        print("\nCombat Options:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Flee")
        
        choice = input("Choose your action (1-4): ")
        
        if choice == "1":
            self.attack(enemy)
        elif choice == "2":
            self.defend()
        elif choice == "3":
            self.use_item()
        elif choice == "4":
            if self.flee():
                return True
        else:
            print("Invalid choice! Turn skipped.")

        # Enemy turn
        if enemy['current_health'] > 0:
            damage = max(0, enemy['strength'] - random.randint(0, 3))
            self.player.health -= damage
            print(f"\n{enemy['name']} deals {damage} damage to you!")
        return False

    def attack(self, enemy):
        damage = self.player.strength + random.randint(1, 6)
        enemy['current_health'] -= damage
        print(f"\nYou deal {damage} damage!")

    def defend(self):
        self.player.health = min(self.player.max_health, 
                               self.player.health + random.randint(5, 10))
        print("\nYou take a defensive stance and recover some health!")

    def use_item(self):
        if self.player.inventory:
            choice = self.choose_item()
            if choice == -1:
                print('\nCancelling...')
                return
            try:
                self.handle_item_effect(self.player.inventory[choice])
            except IndexError:
                print('\nPlease enter a valid number!')
                self.use_item()
        else:
            print('\nYour inventory is empty!')

    def choose_item(self):
        print("\nInventory:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.replace('_', ' ').title()}")
        try:
            return int(input("\nChoose item to use (0 to cancel): ")) - 1
        except ValueError:
            print("\nPlease enter a number!")
            return self.choose_item()

    def flee(self):
        if random.random() < self.player.agility * 0.1:
            print("\nYou successfully fled!")
            return True
        print("\nYou couldn't escape!")
        return False

    def find_item(self):
        location = self.locations[self.player.current_location]
        if location['items']:
            item = random.choice(location['items'])
            print(f"\nYou found a {item.replace('_', ' ')}!")
            self.player.inventory.append(item)
            
            # Check if the found item completes any quests
            for quest in self.player.active_quests:
                quest_data = self.quest_data[quest]
                if item in quest_data["items_needed"]:
                    print(f"This item is needed for the quest: {quest}")
            
            self.check_all_quests()

    def change_location(self):
        print("\nAvailable locations:")
        for i, location in enumerate(self.locations, 1):
            print(f"{i}. {location.replace('_', ' ').title()}")
        try:
            choice = int(input("\nChoose location to travel to (0 to cancel): ")) - 1
            if 0 <= choice < len(self.locations):
                new_location = list(self.locations)[choice]
                if new_location != self.player.current_location:
                    self.player.current_location = new_location
                    print(f"\nTraveled to {new_location.replace('_', ' ').title()}")
                    self.player.story_choices.append(new_location)
                else:
                    print("\nYou're already here!")
        except ValueError:
            print("Please enter a valid number!")

    def rest(self):
        if random.random() < 0.8:
            self.player.health = min(self.player.max_health, self.player.health + 20)
            print(f"\nYou rest peacefully and recover 20 health.")
        else:
            print("\nYour rest is interrupted by strange noises...")
            self.explore()

    def talk_to_npcs(self):
        location = self.locations[self.player.current_location]
        if location['npcs']:
            print("\nNPCs:")
            for i, npc in enumerate(location['npcs'], 1):
                print(f"{i}. {npc['name']}")
            try:
                choice = int(input("\nChoose NPC to talk to (0 to cancel): ")) - 1
                if 0 <= choice < len(location['npcs']):
                    self.handle_npc_interaction(location['npcs'][choice])
                else:
                    print("Invalid NPC choice!")
            except ValueError:
                print("Please enter a valid number!")
        else:
            print("\nThere are no NPCs to talk to here.")

    def handle_npc_interaction(self, npc: dict):
        print(f"\nYou approach {npc['name']}.")

        # Check for completable quests first
        completable_quests = [
            quest for quest in self.player.active_quests
            if quest in npc['quests'] and  # NPC must be the quest giver
            self.is_quest_completable(quest)
        ]

        if completable_quests:
            print(f"\n{npc['name']}: Ah, you've returned! Let me see your progress...")
            for quest in completable_quests:
                print(f"\nYou can complete: {quest}")
                choice = input("Turn in this quest? (y/n): ").lower()
                if choice == 'y':
                    self.complete_quest(quest)
                    if quest in self.player.active_quests:
                        self.player.active_quests.remove(quest)
                    print(f"Quest '{quest}' completed!")
                    break  # Exit the loop after completing a quest
        
        # Then show available quests
        available_quests = [
            quest for quest in npc['quests']
            if quest not in self.player.quests_completed 
            and quest not in self.player.active_quests
            and self.can_take_quest(quest)
        ]

        if available_quests and not completable_quests:
            print(f"\n{npc['name']}: I have some tasks that need attention...")
            for quest in available_quests:
                print(f"\n- {quest}")
                if self.can_take_quest(quest):
                    choice = input("Accept this quest? (y/n): ").lower()
                    if choice == 'y':
                        self.handle_quest(quest)
                        break  # Exit the loop after accepting a quest
                else:
                    required_quests = self.quest_data[quest]["requires"]
                    if required_quests:
                        print(f"  (Requires completion of: {', '.join(required_quests)})")

        if not available_quests and not completable_quests:
            print(f"\n{npc['name']}: I have nothing for you at the moment.")

    def is_quest_completable(self, quest: str) -> bool:
        """Check if a quest is ready to be turned in"""
        quest_data = self.quest_data[quest]
        current_progress = self.player.quest_progress.get(quest, 0)
        
        if current_progress >= quest_data["progress_max"]:
            return all(item in self.player.inventory 
                    for item in quest_data["items_needed"])
        return False

    def complete_quest(self, quest: str):
        """Complete a quest and give rewards"""
        quest_data = self.quest_data[quest]
        
        # Remove required items
        for item in quest_data["items_needed"]:
            self.player.inventory.remove(item)
        
        # Give reward
        if quest_data["reward"]:
            self.player.inventory.append(quest_data["reward"])
            print(f"\nQuest completed: {quest}")
            print(f"Received reward: {quest_data['reward'].replace('_', ' ')}")
        else:
            print(f"\nQuest completed: {quest}")
        
        # Update quest lists
        self.player.active_quests.remove(quest)
        self.player.quests_completed.append(quest)
        
        # Notify about newly available quests
        for potential_quest, potential_data in self.quest_data.items():
            if (potential_quest not in self.player.active_quests and 
                potential_quest not in self.player.quests_completed and
                all(req in self.player.quests_completed for req in potential_data["requires"])):
                print(f"\nNew quest available: {potential_quest}")
                print("Talk to the appropriate NPC to accept this quest.")

    def can_take_quest(self, quest: str) -> bool:
        """Check if all prerequisites are met for taking a quest"""
        required_quests = self.quest_data[quest]["requires"]
        return all(req in self.player.quests_completed for req in required_quests)

    def handle_quest(self, quest: str):
        """Add a new quest to the player's active quests"""
        if quest not in self.player.active_quests and quest not in self.player.quests_completed:
            self.player.active_quests.append(quest)
            self.player.quest_progress[quest] = 0
            print(f"\nQuest accepted: {quest}")
            
            # Display quest details
            quest_data = self.quest_data[quest]
            
            print("\nQuest Requirements:")
            if quest_data["enemy_kills"]:
                print("Enemies to defeat:")
                for enemy, count in quest_data["enemy_kills"].items():
                    print(f"- {enemy}: {count}")
            
            if quest_data["items_needed"]:
                print("Items needed:")
                for item in quest_data["items_needed"]:
                    print(f"- {item.replace('_', ' ')}")
            
            if quest_data["reward"]:
                print(f"\nReward: {quest_data['reward'].replace('_', ' ')}")
        else:
            print("\nYou already have this quest or have completed it.")

    def check_all_quests(self):
        """Check if any active quests have been completed but not yet turned in"""
        for quest in self.player.active_quests:
            quest_data = self.quest_data[quest]
            current_progress = self.player.quest_progress.get(quest, 0)
            
            # Check if quest requirements are met
            if current_progress >= quest_data["progress_max"]:
                # Verify required items are in inventory
                has_required_items = all(item in self.player.inventory 
                                    for item in quest_data["items_needed"])
                
                if has_required_items:
                    print(f"\nQuest requirements met for: {quest}")
                    print("Return to the quest giver to complete the quest!")
                    self.player.quest_progress[quest] = quest_data["progress_max"]  # Cap the progress

    def fight_skekso(self):
        self.fighting_skekso = True
        self.combat("Emperor Skekso")
        self.fighting_skekso = False

    def check_game_over(self) -> bool:
        """Check if the game should end"""
        if self.player.health <= 0:
            print("\nYou have fallen in battle... Game Over!")
            return True
            
        all_quests_completed = len(self.player.quests_completed) == len(self.quest_data)
        
        if all_quests_completed:
            self.trigger_ending()
            return True
        return False

    def trigger_ending(self):
        print('\nwoohoo you did it')

    def quit_game(self):
        """Handle game quit"""
        if input("\nAre you sure you want to quit? (y/n): ").lower() == 'y':
            print("\nThanks for playing The Crystal Kingdoms!")
            self.game_running = False

# Start the game if this file is run directly
if __name__ == "__main__":
    game = CrystalKingdoms()
    game.start_game()