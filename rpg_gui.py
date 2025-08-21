import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread

class AnimatedRPG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🗡️ Epic Quest Adventure")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Game data
        self.enemies = ["goblin", "orc", "skeleton", "dragon"]
        self.items = ["potion", "sword", "shield", "gold"]
        self.quest_types = ["hunt", "collect"]
        
        # Color scheme
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'accent': '#0f3460',
            'gold': '#ffd700',
            'green': '#4ade80',
            'red': '#ef4444',
            'blue': '#3b82f6',
            'purple': '#8b5cf6',
            'text': '#e5e7eb'
        }
        
        self.player = None
        self.available_quests = []
        self.animation_queue = []
        
        self.setup_styles()
        self.create_widgets()
        self.start_game()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', background=self.colors['bg'], 
                       foreground=self.colors['gold'], font=('Arial', 20, 'bold'))
        style.configure('Card.TFrame', background=self.colors['card'], 
                       borderwidth=2, relief='raised')
        style.configure('Stat.TLabel', background=self.colors['card'], 
                       foreground=self.colors['text'], font=('Arial', 12))
        style.configure('Action.TButton', font=('Arial', 11, 'bold'))
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🗡️ EPIC QUEST ADVENTURE 🗡️", 
                              bg=self.colors['bg'], fg=self.colors['gold'],
                              font=('Arial', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Top section - Player stats and actions
        top_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        top_frame.pack(fill='x', pady=(0, 20))
        
        # Player stats card
        self.stats_frame = tk.Frame(top_frame, bg=self.colors['card'], 
                                   relief='raised', bd=3)
        self.stats_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_stats_section()
        
        # Action buttons
        action_frame = tk.Frame(top_frame, bg=self.colors['accent'], 
                               relief='raised', bd=3)
        action_frame.pack(side='right', fill='both', padx=(10, 0))
        
        self.create_action_buttons(action_frame)
        
        # Middle section - Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Quests
        left_panel = tk.Frame(content_frame, bg=self.colors['card'], 
                             relief='raised', bd=3, width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_quest_section(left_panel)
        
        # Right panel - Inventory and Log
        right_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_inventory_and_log(right_panel)
        
        # Animation canvas (overlay)
        self.animation_canvas = tk.Canvas(self.root, highlightthickness=0,
                                         bg=self.colors['bg'])
        self.animation_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.animation_canvas.configure(state='disabled')
        
    def create_stats_section(self):
        tk.Label(self.stats_frame, text="🏰 HERO STATUS", 
                bg=self.colors['card'], fg=self.colors['gold'],
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.name_label = tk.Label(self.stats_frame, bg=self.colors['card'], 
                                  fg=self.colors['text'], font=('Arial', 14, 'bold'))
        self.name_label.pack()
        
        # Level and XP
        level_frame = tk.Frame(self.stats_frame, bg=self.colors['card'])
        level_frame.pack(pady=5)
        
        self.level_label = tk.Label(level_frame, bg=self.colors['card'], 
                                   fg=self.colors['blue'], font=('Arial', 12, 'bold'))
        self.level_label.pack(side='left')
        
        # XP Progress bar
        self.xp_var = tk.IntVar()
        self.xp_progress = ttk.Progressbar(self.stats_frame, variable=self.xp_var, 
                                          maximum=100, length=200)
        self.xp_progress.pack(pady=5)
        
        self.xp_label = tk.Label(self.stats_frame, bg=self.colors['card'], 
                                fg=self.colors['text'], font=('Arial', 10))
        self.xp_label.pack()
        
        # Gold
        self.gold_label = tk.Label(self.stats_frame, bg=self.colors['card'], 
                                  fg=self.colors['gold'], font=('Arial', 12, 'bold'))
        self.gold_label.pack(pady=5)
        
    def create_action_buttons(self, parent):
        tk.Label(parent, text="⚔️ ACTIONS", bg=self.colors['accent'], 
                fg=self.colors['gold'], font=('Arial', 14, 'bold')).pack(pady=10)
        
        buttons = [
            ("🗡️ FIGHT", self.fight_action, self.colors['red']),
            ("🔍 EXPLORE", self.explore_action, self.colors['green']),
            ("📋 QUESTS", self.show_quests_action, self.colors['blue']),
            ("🎯 NEW QUEST", self.new_quest_action, self.colors['purple']),
            ("🎒 INVENTORY", self.show_inventory_action, self.colors['gold'])
        ]
        
        self.action_buttons = []
        for text, command, color in buttons:
            btn = tk.Button(parent, text=text, command=command,
                           bg=color, fg='white', font=('Arial', 11, 'bold'),
                           relief='raised', bd=2, padx=20, pady=8,
                           activebackground=color, activeforeground='white')
            btn.pack(pady=5, padx=10, fill='x')
            self.action_buttons.append(btn)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_leave(b, c))
    
    def on_button_hover(self, button, color):
        button.configure(bg=self.lighten_color(color))
        
    def on_button_leave(self, button, color):
        button.configure(bg=color)
        
    def lighten_color(self, color):
        # Simple color lightening
        colors_map = {
            self.colors['red']: '#f87171',
            self.colors['green']: '#86efac',
            self.colors['blue']: '#60a5fa',
            self.colors['purple']: '#a78bfa',
            self.colors['gold']: '#fde047'
        }
        return colors_map.get(color, color)
    
    def create_quest_section(self, parent):
        tk.Label(parent, text="📜 ACTIVE QUESTS", bg=self.colors['card'], 
                fg=self.colors['gold'], font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Scrollable quest list
        quest_canvas = tk.Canvas(parent, bg=self.colors['card'], highlightthickness=0)
        quest_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=quest_canvas.yview)
        self.quest_frame = tk.Frame(quest_canvas, bg=self.colors['card'])
        
        quest_canvas.configure(yscrollcommand=quest_scrollbar.set)
        quest_canvas.pack(side="left", fill="both", expand=True, padx=10)
        quest_scrollbar.pack(side="right", fill="y")
        
        quest_canvas.create_window((0, 0), window=self.quest_frame, anchor="nw")
        
        self.quest_canvas = quest_canvas
        
    def create_inventory_and_log(self, parent):
        # Inventory section
        inv_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=3)
        inv_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(inv_frame, text="🎒 INVENTORY", bg=self.colors['card'], 
                fg=self.colors['gold'], font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.inventory_frame = tk.Frame(inv_frame, bg=self.colors['card'])
        self.inventory_frame.pack(padx=10, pady=(0, 10))
        
        # Activity log
        log_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=3)
        log_frame.pack(fill='both', expand=True)
        
        tk.Label(log_frame, text="📰 ACTIVITY LOG", bg=self.colors['card'], 
                fg=self.colors['gold'], font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(log_frame, bg=self.colors['card'])
        text_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(text_frame, bg=self.colors['accent'], 
                               fg=self.colors['text'], font=('Courier', 10),
                               wrap='word', state='disabled')
        log_scroll = ttk.Scrollbar(text_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scroll.pack(side='right', fill='y')
        
    def start_game(self):
        # Get player name
        name = tk.simpledialog.askstring("Hero Name", "Enter your hero name:", 
                                        parent=self.root)
        if not name:
            name = "Brave Adventurer"
            
        self.player = self.make_player(name)
        self.available_quests = [self.make_quest(self.player["level"]) for _ in range(3)]
        
        self.update_display()
        self.log_message(f"🌟 Welcome {name}! Your epic adventure begins!")
        
        # Start animation loop
        self.animate_loop()
        
    def make_player(self, name):
        return {
            "name": name,
            "level": 1,
            "xp": 0,
            "next_xp": 100,
            "gold": 20,
            "inventory": {item: 0 for item in self.items},
            "quests": []
        }
        
    def make_quest(self, level):
        qtype = random.choice(self.quest_types)
        if qtype == "hunt":
            target = random.choice(self.enemies)
            need = random.randint(2, 4)
            return {"title": f"Hunt {need} {target}(s)", "type": "hunt",
                    "target": target, "need": need, "done": 0,
                    "xp": 30 + level * 10, "gold": 15 + level * 5, "status": "new"}
        else:
            target = random.choice(self.items)
            need = random.randint(2, 5)
            return {"title": f"Collect {need} {target}(s)", "type": "collect",
                    "target": target, "need": need, "done": 0,
                    "xp": 20 + level * 10, "gold": 10 + level * 5, "status": "new"}
    
    def update_display(self):
        if not self.player:
            return
            
        # Update stats
        self.name_label.configure(text=f"🏆 {self.player['name']}")
        self.level_label.configure(text=f"Level {self.player['level']}")
        
        # Update XP progress
        xp_percent = (self.player['xp'] / self.player['next_xp']) * 100
        self.xp_var.set(int(xp_percent))
        self.xp_label.configure(text=f"XP: {self.player['xp']}/{self.player['next_xp']}")
        
        self.gold_label.configure(text=f"💰 Gold: {self.player['gold']}")
        
        self.update_quests()
        self.update_inventory()
        
    def update_quests(self):
        # Clear existing quest widgets
        for widget in self.quest_frame.winfo_children():
            widget.destroy()
            
        if not self.player['quests']:
            tk.Label(self.quest_frame, text="No active quests", 
                    bg=self.colors['card'], fg=self.colors['text']).pack()
        else:
            for i, quest in enumerate(self.player['quests']):
                quest_widget = self.create_quest_widget(self.quest_frame, quest, i)
                quest_widget.pack(fill='x', pady=5)
                
        # Update scroll region
        self.quest_frame.update_idletasks()
        self.quest_canvas.configure(scrollregion=self.quest_canvas.bbox("all"))
        
    def create_quest_widget(self, parent, quest, index):
        frame = tk.Frame(parent, bg=self.colors['accent'], relief='raised', bd=2)
        
        # Quest title
        tk.Label(frame, text=quest['title'], bg=self.colors['accent'], 
                fg=self.colors['text'], font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=2)
        
        # Progress
        if quest['status'] == 'active':
            progress = f"Progress: {quest['done']}/{quest['need']}"
            color = self.colors['blue'] if quest['done'] < quest['need'] else self.colors['green']
        else:
            progress = "COMPLETED!"
            color = self.colors['green']
            
        tk.Label(frame, text=progress, bg=self.colors['accent'], 
                fg=color, font=('Arial', 9)).pack(anchor='w', padx=5)
        
        # Rewards
        rewards = f"Rewards: {quest['xp']} XP, {quest['gold']} Gold"
        tk.Label(frame, text=rewards, bg=self.colors['accent'], 
                fg=self.colors['gold'], font=('Arial', 8)).pack(anchor='w', padx=5, pady=(0, 5))
        
        return frame
        
    def update_inventory(self):
        # Clear existing inventory widgets
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()
            
        # Create inventory grid
        row = 0
        col = 0
        for item, count in self.player['inventory'].items():
            if count > 0:
                item_frame = tk.Frame(self.inventory_frame, bg=self.colors['accent'], 
                                     relief='raised', bd=1, padx=5, pady=3)
                item_frame.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
                
                emoji_map = {"potion": "🧪", "sword": "⚔️", "shield": "🛡️", "gold": "💰"}
                emoji = emoji_map.get(item, "📦")
                
                tk.Label(item_frame, text=f"{emoji} {count}", 
                        bg=self.colors['accent'], fg=self.colors['text'],
                        font=('Arial', 10)).pack()
                
                col += 1
                if col > 1:
                    col = 0
                    row += 1
    
    def log_message(self, message, color=None):
        if color is None:
            color = self.colors['text']
            
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"{message}\n", )
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        
        # Add floating text animation
        self.add_floating_text(message)
        
    def add_floating_text(self, text):
        # Create floating text animation
        x = random.randint(200, 800)
        y = 400
        
        text_id = self.animation_canvas.create_text(x, y, text=text, 
                                                   fill=self.colors['gold'], 
                                                   font=('Arial', 12, 'bold'))
        
        # Animate upward movement
        def animate_text(current_y, steps):
            if steps > 0:
                new_y = current_y - 2
                self.animation_canvas.coords(text_id, x, new_y)
                self.root.after(50, lambda: animate_text(new_y, steps - 1))
            else:
                self.animation_canvas.delete(text_id)
                
        animate_text(y, 30)
    
    def add_xp(self, amount):
        old_level = self.player["level"]
        self.player["xp"] += amount
        
        self.log_message(f"⭐ Gained {amount} XP!", self.colors['blue'])
        
        if self.player["xp"] >= self.player["next_xp"]:
            self.player["level"] += 1
            self.player["xp"] = 0
            self.player["next_xp"] = int(self.player["next_xp"] * 1.5)
            self.log_message(f"🎉 LEVEL UP! You are now level {self.player['level']}!", 
                           self.colors['gold'])
            self.show_level_up_animation()
            
        self.update_display()
    
    def show_level_up_animation(self):
        # Create level up effect
        for i in range(20):
            x = random.randint(100, 900)
            y = random.randint(100, 600)
            star = self.animation_canvas.create_text(x, y, text="⭐", 
                                                    fill=self.colors['gold'], 
                                                    font=('Arial', 16))
            
            # Animate stars
            def animate_star(star_id, delay):
                self.root.after(delay, lambda: self.animation_canvas.delete(star_id))
                
            animate_star(star, 2000 + i * 100)
    
    def fight_action(self):
        self.disable_buttons()
        enemy = random.choice(self.enemies)
        xp_gain = 20
        gold_gain = 10
        
        emoji_map = {"goblin": "👹", "orc": "👺", "skeleton": "💀", "dragon": "🐉"}
        emoji = emoji_map.get(enemy, "👾")
        
        self.log_message(f"⚔️ Fighting {emoji} {enemy}...")
        
        # Simulate battle delay
        self.root.after(1500, lambda: self.complete_fight(enemy, xp_gain, gold_gain))
        
    def complete_fight(self, enemy, xp_gain, gold_gain):
        self.log_message(f"🎯 Defeated {enemy}! +{xp_gain} XP, +{gold_gain} Gold")
        self.add_xp(xp_gain)
        self.player["gold"] += gold_gain
        
        # Update hunt quests
        for q in self.player["quests"]:
            if q["type"] == "hunt" and q["target"] == enemy and q["status"] == "active":
                q["done"] += 1
                if q["done"] >= q["need"]:
                    q["status"] = "done"
                    self.log_message(f"✅ Quest Completed: {q['title']}")
                    self.complete_quest(q)
                    
        self.update_display()
        self.enable_buttons()
        
    def explore_action(self):
        self.disable_buttons()
        item = random.choice(self.items)
        
        emoji_map = {"potion": "🧪", "sword": "⚔️", "shield": "🛡️", "gold": "💰"}
        emoji = emoji_map.get(item, "📦")
        
        self.log_message(f"🔍 Exploring...")
        
        # Simulate exploration delay
        self.root.after(1000, lambda: self.complete_explore(item, emoji))
        
    def complete_explore(self, item, emoji):
        self.log_message(f"🎁 Found {emoji} {item}!")
        self.player["inventory"][item] += 1
        
        # Update collect quests
        for q in self.player["quests"]:
            if q["type"] == "collect" and q["target"] == item and q["status"] == "active":
                q["done"] += 1
                if q["done"] >= q["need"]:
                    q["status"] = "done"
                    self.log_message(f"✅ Quest Completed: {q['title']}")
                    self.complete_quest(q)
                    
        self.update_display()
        self.enable_buttons()
        
    def complete_quest(self, quest):
        self.add_xp(quest["xp"])
        self.player["gold"] += quest["gold"]
        self.player["quests"].remove(quest)
        
    def show_quests_action(self):
        # Check for completed quests
        completed = [q for q in self.player["quests"] if q["status"] == "done"]
        for quest in completed:
            self.complete_quest(quest)
            
        if not self.player["quests"]:
            self.log_message("📋 No active quests.")
        else:
            self.log_message("📋 Check your quest panel for active quests!")
            
        self.update_display()
        
    def new_quest_action(self):
        # Create quest selection dialog
        quest_window = tk.Toplevel(self.root)
        quest_window.title("Available Quests")
        quest_window.geometry("400x300")
        quest_window.configure(bg=self.colors['bg'])
        quest_window.transient(self.root)
        quest_window.grab_set()
        
        tk.Label(quest_window, text="🎯 Available Quests", 
                bg=self.colors['bg'], fg=self.colors['gold'],
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        for i, quest in enumerate(self.available_quests):
            frame = tk.Frame(quest_window, bg=self.colors['card'], 
                           relief='raised', bd=2)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=quest['title'], bg=self.colors['card'], 
                    fg=self.colors['text'], font=('Arial', 11, 'bold')).pack(anchor='w', padx=5, pady=2)
            
            rewards = f"Rewards: {quest['xp']} XP, {quest['gold']} Gold"
            tk.Label(frame, text=rewards, bg=self.colors['card'], 
                    fg=self.colors['gold'], font=('Arial', 9)).pack(anchor='w', padx=5)
            
            tk.Button(frame, text="Accept Quest", 
                     command=lambda q=quest, w=quest_window: self.accept_quest(q, w),
                     bg=self.colors['green'], fg='white', font=('Arial', 10, 'bold')).pack(pady=5)
    
    def accept_quest(self, quest, window):
        quest["status"] = "active"
        self.player["quests"].append(quest)
        
        # Replace with new quest
        index = self.available_quests.index(quest)
        self.available_quests[index] = self.make_quest(self.player["level"])
        
        self.log_message(f"📝 Accepted quest: {quest['title']}")
        self.update_display()
        window.destroy()
        
    def show_inventory_action(self):
        self.log_message("🎒 Check your inventory panel!")
        
    def disable_buttons(self):
        for btn in self.action_buttons:
            btn.configure(state='disabled')
            
    def enable_buttons(self):
        for btn in self.action_buttons:
            btn.configure(state='normal')
            
    def animate_loop(self):
        # Continuous background animations
        if random.random() < 0.1:  # 10% chance each cycle
            self.add_sparkle_effect()
            
        self.root.after(2000, self.animate_loop)
        
    def add_sparkle_effect(self):
        # Add random sparkles
        x = random.randint(50, 950)
        y = random.randint(50, 650)
        sparkle = self.animation_canvas.create_text(x, y, text="✨", 
                                                  fill=self.colors['gold'], 
                                                  font=('Arial', 12))
        
        # Remove after 3 seconds
        self.root.after(3000, lambda: self.animation_canvas.delete(sparkle))
    
    def run(self):
        self.root.mainloop()

# Import required modules for dialog
import tkinter.simpledialog

if __name__ == "__main__":
    game = AnimatedRPG()
    game.run()