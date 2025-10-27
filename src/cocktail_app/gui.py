import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from tkinter import font as tkfont
import threading
from pathlib import Path

KB_PATH = Path(__file__).parent / 'knowledge' / 'cocktail_knowledge_base.pl'

class ModernCocktailExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🍸 MixMaster Pro - Cocktail Expert System")
        self.root.geometry("930x800")
        self.root.configure(bg='#0F172A')
        
        # Modern color scheme
        self.colors = {
            'primary': '#3B82F6',
            'secondary': '#1E293B',
            'accent': '#8B5CF6',
            'background': '#0F172A',
            'surface': '#1E293B',
            'text_primary': '#F1F5F9',
            'text_secondary': '#94A3B8',
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'selected': '#3B82F6'
        }
        
        # Store selected buttons for visual feedback
        self.selected_buttons = {}
        
        # Configure styles
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('Modern.TNotebook', 
                       background=self.colors['background'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab', 
                       background=self.colors['secondary'],
                       foreground='black',
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('Modern.TNotebook.Tab', 
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'black')])

    # --- rest of the original GUI implementation ---
    # For brevity this file preserves the original implementation exactly
    # except for references to the knowledge base file which now use KB_PATH

    def setup_ui(self):
        # Header
        self.create_header()
        
        # Create main notebook with modern style
        self.notebook = ttk.Notebook(self.root, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Preferences Tab
        self.preferences_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(self.preferences_frame, text='🎯 SET PREFERENCES')
        
        # Results Tab
        self.results_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(self.results_frame, text='🍹 RECOMMENDATIONS')
        
        # Loading Screen
        self.loading_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(self.loading_frame, text='⏳ LOADING')
        
        self.setup_preferences_tab()
        self.setup_results_tab()
        self.setup_loading_tab()

    # NOTE: The following methods are identical to your original file, but
    # any filesystem references to the knowledge base have been changed
    # to use KB_PATH (a Path object pointing to the packaged KB file).

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=80)
        header_frame.pack(fill='x', padx=20, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Title
        title_font = tkfont.Font(family='Segoe UI', size=24, weight='bold')
        title_label = tk.Label(header_frame, 
                              text="🍸 MixMaster Pro", 
                              font=title_font,
                              bg=self.colors['secondary'],
                              fg=self.colors['text_primary'])
        title_label.pack(side='left', padx=20, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                text="AI-Powered Cocktail Recommendations",
                                font=('Segoe UI', 12),
                                bg=self.colors['secondary'],
                                fg=self.colors['text_secondary'])
        subtitle_label.pack(side='left', padx=10, pady=20)
        
        # Status indicator
        self.status_label = tk.Label(header_frame,
                                   text="● Ready",
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=self.colors['secondary'],
                                   fg=self.colors['success'])
        self.status_label.pack(side='right', padx=20, pady=20)

    def setup_preferences_tab(self):
        # Main container with modern scrollbar
        main_container = tk.Frame(self.preferences_frame, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Header with icon
        header_container = tk.Frame(self.scrollable_frame, bg=self.colors['background'])
        header_container.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_container, text="🎯", 
                font=('Segoe UI', 48),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(pady=(10, 0))
        
        tk.Label(header_container, text="Customize Your Cocktail Experience", 
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['text_primary']).pack(pady=(5, 5))
        
        tk.Label(header_container, text="Tell us your preferences and we'll find your perfect match", 
                font=('Segoe UI', 12),
                bg=self.colors['background'],
                fg=self.colors['text_secondary']).pack(pady=(0, 20))
        
        # ===== SPIRIT PREFERENCE =====
        spirit_frame = self.create_modern_section("🍾 Spirit Preference", self.scrollable_frame)
        self.spirit_var = tk.StringVar(value="no_preference")
        
        spirits = [
            ("Rum", "rum", "#FF6B6B"),
            ("Gin", "gin", "#4ECDC4"), 
            ("Vodka", "vodka", "#45B7D1"),
            ("Whiskey", "whiskey", "#FFA07A"),
            ("Tequila", "tequila", "#98D8C8"),
            ("No Preference", "no_preference", "#BB86FC")
        ]
        
        spirit_container = tk.Frame(spirit_frame, bg=self.colors['surface'])
        spirit_container.pack(fill='x', padx=10, pady=10)
        
        for i, (text, value, color) in enumerate(spirits):
            btn = self.create_choice_button(spirit_container, text, value, self.spirit_var, color, "spirit")
            btn.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # ===== FLAVOR PROFILE =====
        flavor_frame = self.create_modern_section("👅 Flavor Profile", self.scrollable_frame)
        
        # Flavor notes
        tk.Label(flavor_frame, text="Preferred Flavor Notes:", 
                bg=self.colors['surface'], fg=self.colors['text_primary'], 
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.flavor_var = tk.StringVar(value="citrus")
        flavors = [
            ("🍋 Citrus", "citrus", "#FDE68A"),
            ("🍬 Sweet", "sweet", "#FCA5A5"), 
            ("🌿 Herbal", "herbal", "#86EFAC"),
            ("🥛 Creamy", "creamy", "#F3F4F6"),
            ("💪 Strong", "strong", "#FDBA74")
        ]
        
        flavor_container = tk.Frame(flavor_frame, bg=self.colors['surface'])
        flavor_container.pack(fill='x', padx=10, pady=5)
        
        for i, (text, value, color) in enumerate(flavors):
            btn = self.create_choice_button(flavor_container, text, value, self.flavor_var, color, "flavor")
            btn.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # Strength preference
        strength_container = tk.Frame(flavor_frame, bg=self.colors['surface'])
        strength_container.pack(fill='x', padx=10, pady=15)
        
        tk.Label(strength_container, text="Alcohol Strength Preference:", 
                bg=self.colors['surface'], fg=self.colors['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        self.strength_var = tk.IntVar(value=7)
        strength_scale = tk.Scale(strength_container, from_=1, to=10, variable=self.strength_var, 
                                 orient='horizontal', length=400,
                                 bg=self.colors['surface'], fg=self.colors['text_primary'], 
                                 troughcolor=self.colors['secondary'],
                                 highlightbackground=self.colors['surface'],
                                 sliderrelief='flat',
                                 sliderlength=20,
                                 showvalue=True,
                                 font=('Segoe UI', 9))
        strength_scale.pack(fill='x', pady=10)
        
        # Labels for scale
        scale_labels = tk.Frame(strength_container, bg=self.colors['surface'])
        scale_labels.pack(fill='x')
        tk.Label(scale_labels, text="Light", bg=self.colors['surface'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(side='left')
        tk.Label(scale_labels, text="Moderate", bg=self.colors['surface'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(side='left', expand=True)
        tk.Label(scale_labels, text="Strong", bg=self.colors['surface'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(side='right')
        
        # ===== SKILL LEVEL =====
        skill_frame = self.create_modern_section("🛠️ Skill Level", self.scrollable_frame)
        self.skill_var = tk.StringVar(value="beginner")
        
        skills = [
            ("👶 Beginner\n(basic shaking/stirring)", "beginner", "#6EE7B7"),
            ("👨‍🍳 Intermediate\n(muddling, layering)", "intermediate", "#3B82F6"), 
            ("👨‍🔬 Expert\n(complex techniques)", "expert", "#8B5CF6")
        ]
        
        skill_container = tk.Frame(skill_frame, bg=self.colors['surface'])
        skill_container.pack(fill='x', padx=10, pady=10)
        
        for i, (text, value, color) in enumerate(skills):
            btn = self.create_choice_button(skill_container, text, value, self.skill_var, color, "skill")
            btn.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # ===== OCCASION CONTEXT =====
        occasion_frame = self.create_modern_section("🎉 Occasion Context", self.scrollable_frame)
        self.occasion_var = tk.StringVar(value="casual_relaxing")
        
        occasions = [
            ("🎊 Party / Social", "party", "#F87171"),
            ("💝 Romantic Dinner", "romantic_dinner", "#FB7185"),
            ("😌 Casual Relaxing", "casual_relaxing", "#60A5FA"),
            ("🎇 Celebration", "celebration", "#FBBF24"),
            ("🍽️ After Dinner", "after_dinner", "#34D399"),
            ("🍸 Aperitif", "aperitif", "#A78BFA")
        ]
        
        occasion_container1 = tk.Frame(occasion_frame, bg=self.colors['surface'])
        occasion_container1.pack(fill='x', padx=10, pady=5)
        occasion_container2 = tk.Frame(occasion_frame, bg=self.colors['surface'])
        occasion_container2.pack(fill='x', padx=10, pady=5)
        
        for i, (text, value, color) in enumerate(occasions):
            container = occasion_container1 if i < 3 else occasion_container2
            btn = self.create_choice_button(container, text, value, self.occasion_var, color, "occasion")
            btn.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # ===== SEASONAL PREFERENCES =====
        season_frame = self.create_modern_section("🌸 Seasonal Preferences", self.scrollable_frame)
        self.season_var = tk.StringVar(value="all_seasons")
        
        seasons = [
            ("🌷 Spring", "spring", "#86EFAC"),
            ("☀️ Summer", "summer", "#FDE68A"),
            ("🍂 Autumn", "autumn", "#FDBA74"),
            ("❄️ Winter", "winter", "#BFDBFE"),
            ("🌎 All Seasons", "all_seasons", "#C7D2FE")
        ]
        
        season_container = tk.Frame(season_frame, bg=self.colors['surface'])
        season_container.pack(fill='x', padx=10, pady=10)
        
        for i, (text, value, color) in enumerate(seasons):
            btn = self.create_choice_button(season_container, text, value, self.season_var, color, "season")
            btn.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # ===== ACTION BUTTONS =====
        button_frame = tk.Frame(self.scrollable_frame, bg=self.colors['background'])
        button_frame.pack(fill='x', pady=30)
        
        # Main action buttons
        actions = [
            ("🎯 Get AI Recommendations", self.get_recommendations, self.colors['primary']),
            ("🔄 Reset Preferences", self.reset_preferences, self.colors['secondary']),
            ("📚 Browse All Cocktails", self.browse_all, self.colors['accent'])
        ]
        
        for text, command, color in actions:
            btn = self.create_modern_button(button_frame, text, command, color)
            btn.pack(side='left', padx=10, pady=10, fill='x', expand=True)

    def create_modern_section(self, title, parent):
        """Create a modern section frame with gradient-like appearance"""
        section_frame = tk.Frame(parent, bg=self.colors['background'])
        section_frame.pack(fill='x', padx=10, pady=15)
        
        # Title with accent
        title_frame = tk.Frame(section_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(title_frame, text=title, 
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['text_primary']).pack(side='left')
        
        # Content container with surface color
        content_frame = tk.Frame(section_frame, bg=self.colors['surface'], 
                                relief='flat', bd=1)
        content_frame.pack(fill='x', padx=0, pady=0)
        
        return content_frame

    def create_choice_button(self, parent, text, value, variable, color, group):
        """Create modern choice buttons with better selection handling"""
        btn = tk.Radiobutton(parent, text=text, value=value, variable=variable,
                            command=lambda: self.on_button_select(btn, group, color),
                            bg=self.colors['surface'],
                            fg=self.colors['text_primary'],
                            selectcolor=color,
                            activebackground=self.colors['secondary'],
                            activeforeground='white',
                            font=('Segoe UI', 10),
                            indicatoron=0,
                            relief='raised',
                            bd=2,
                            padx=15,
                            pady=10,
                            width=12,
                            wraplength=120)
        
        # Store initial state
        if group not in self.selected_buttons:
            self.selected_buttons[group] = None
        
        # Set initial selection
        if variable.get() == value:
            self.on_button_select(btn, group, color, initial=True)
            
        return btn

    def on_button_select(self, button, group, color, initial=False):
        """Handle button selection with visual feedback"""
        # Reset previous selection in this group
        if group in self.selected_buttons and self.selected_buttons[group]:
            prev_btn = self.selected_buttons[group]
            prev_btn.config(bg=self.colors['surface'], fg=self.colors['text_primary'])
        
        # Set new selection
        button.config(bg=color, fg='black' if self.get_brightness(color) > 128 else 'white')
        self.selected_buttons[group] = button

    def get_brightness(self, hex_color):
        """Calculate brightness of a color to determine text color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 299 + g * 587 + b * 114) // 1000

    def create_modern_button(self, parent, text, command, color):
        """Create modern gradient-like buttons"""
        btn = tk.Button(parent, text=text, command=command,
                      font=('Segoe UI', 11, 'bold'),
                      bg=color,
                      fg='white',
                      activebackground=color,
                      activeforeground='white',
                      relief='flat',
                      bd=0,
                      padx=20,
                      pady=15,
                      cursor='hand2')
        
        # Add hover effect
        def on_enter(e):
            btn['bg'] = self.adjust_color(color, -20)
        def on_leave(e):
            btn['bg'] = color
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def adjust_color(self, color, amount):
        """Adjust color brightness"""
        # Simple color adjustment for hover effect
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def setup_results_tab(self):
        # Results container
        results_container = tk.Frame(self.results_frame, bg=self.colors['background'])
        results_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(results_container, bg=self.colors['background'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="🍹 Your Personalized Recommendations", 
                font=('Segoe UI', 20, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['text_primary']).pack(side='left')
        
        # Results count
        self.results_count = tk.Label(header_frame, text="0 cocktails found",
                                    font=('Segoe UI', 12),
                                    bg=self.colors['background'],
                                    fg=self.colors['text_secondary'])
        self.results_count.pack(side='right')
        
        # Results text area with modern styling
        text_container = tk.Frame(results_container, bg=self.colors['surface'], relief='flat', bd=1)
        text_container.pack(fill='both', expand=True)
        
        self.results_text = tk.Text(text_container, 
                                   height=25, 
                                   width=80, 
                                   bg=self.colors['surface'], 
                                   fg=self.colors['text_primary'],
                                   font=('Consolas', 11), 
                                   wrap='word',
                                   padx=20,
                                   pady=20,
                                   relief='flat',
                                   bd=0)
        
        scrollbar = ttk.Scrollbar(text_container, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial message
        self.show_welcome_message()

    def setup_loading_tab(self):
        loading_container = tk.Frame(self.loading_frame, bg=self.colors['background'])
        loading_container.pack(expand=True, fill='both')
        
        # Animated loading content
        tk.Label(loading_container, text="🍸", 
                font=('Segoe UI', 48),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(pady=(100, 20))
        
        tk.Label(loading_container, text="MixMaster AI is working...", 
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['text_primary']).pack(pady=10)
        
        tk.Label(loading_container, text="Analyzing your preferences and finding perfect matches", 
                font=('Segoe UI', 12),
                bg=self.colors['background'],
                fg=self.colors['text_secondary']).pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(loading_container, mode='indeterminate', length=400)
        self.progress.pack(pady=30)

    def show_welcome_message(self):
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', 'end')
        
        welcome_text = """
╔══════════════════════════════════════════════════╗
               🍸 WELCOME TO MIXMASTER PRO         
            AI-Powered Cocktail Expert System       
╚══════════════════════════════════════════════════╝

🎯 HOW TO GET STARTED:

1. Go to the 'SET PREFERENCES' tab
2. Customize your cocktail preferences
3. Click 'Get AI Recommendations'
4. Discover your perfect cocktails!

💡 FEATURES:
• Personalized cocktail recommendations
• Advanced preference matching
• Complete cocktail database
• Modern, intuitive interface

📚 You can also browse all cocktails using the 'Browse All Cocktails' button.

Ready to find your perfect drink? Let's get started! 🎉
"""
        self.results_text.insert('1.0', welcome_text)
        self.results_text.config(state='disabled')
        self.results_count.config(text="👆 Set preferences to begin")

    def get_recommendations(self):
        # Show loading screen
        self.notebook.select(2)  # Loading tab
        self.progress.start(10)
        self.status_label.config(text="● Processing...", fg=self.colors['warning'])
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.process_recommendations)
        thread.daemon = True
        thread.start()

    def process_recommendations(self):
        try:
            if not KB_PATH.exists():
                self.root.after(0, lambda: messagebox.showerror("Error", f"{KB_PATH} file not found!"))
                return
            
            # Build Prolog query
            query = f"""
            assertz(known(spirit_preference, {self.spirit_var.get()}, _)),
            assertz(known(flavor_notes, {self.flavor_var.get()}, _)),
            assertz(known(skill_level, {self.skill_var.get()}, _)),
            assertz(known(strength, {self.strength_var.get()}, _)),
            assertz(known(occasion_type, {self.occasion_var.get()}, _)),
            assertz(known(current_season, {self.season_var.get()}, _)),
            find_and_display_recommendations.
            """
            
            process = subprocess.Popen(['swipl', '-q', '-s', str(KB_PATH)], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            stdout, stderr = process.communicate(input=query, timeout=30)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.display_results(stdout, stderr))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to get recommendations: {str(e)}"))

    def display_results(self, stdout, stderr):
        self.progress.stop()
        self.notebook.select(1)  # Results tab
        
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', 'end')
        
        if stdout:
            formatted_output = self.format_output(stdout)
            self.results_text.insert('1.0', formatted_output)
            
            # Count cocktails found
            cocktail_count = formatted_output.count('🍸 🍸 🍸')
            self.results_count.config(text=f"🎯 {cocktail_count} cocktails matched your preferences")
        else:
            self.results_text.insert('1.0', "❌ No results returned from the expert system.")
            self.results_count.config(text="❌ No matches found")
            
        if stderr and "Warning" not in stderr:
            self.results_text.insert('end', f"\n\n--- System Messages ---\n{stderr}")
            
        self.results_text.config(state='disabled')
        self.status_label.config(text="● Ready", fg=self.colors['success'])

    def format_output(self, output):
        """Fixed output formatting that preserves all data"""
        lines = output.split('\n')
        formatted_lines = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'Match Score:' in line:
                score = line.split(':')[1].strip()
                formatted_lines.append(f"🎯 **MATCH SCORE: {score}**")
                formatted_lines.append("─" * 50)
            elif '**' in line and 'Match Score' not in line:
                # Cocktail name
                cocktail_name = line.replace('**', '').strip()
                formatted_lines.append(f"\n🍸 🍸 🍸  {cocktail_name.upper()}  🍸 🍸 🍸\n")
            elif 'Base Spirit:' in line:
                formatted_lines.append(f"   🍾 {line}")
            elif 'Strength:' in line and 'Complexity:' in line:
                formatted_lines.append(f"   ⚡ {line}")
            elif 'Ingredients:' in line:
                # Don't add extra section headers, just show the content
                ingredients = line.replace('Ingredients:', '').strip()
                formatted_lines.append(f"   🧪 Ingredients: {ingredients}")
            elif 'Techniques:' in line:
                techniques = line.replace('Techniques:', '').strip()
                formatted_lines.append(f"   ⚙️  Techniques: {techniques}")
            elif 'Flavors:' in line:
                flavors = line.replace('Flavors:', '').strip()
                formatted_lines.append(f"   👅 Flavors: {flavors}")
            elif 'Best for:' in line:
                best_for = line.replace('Best for:', '').strip()
                formatted_lines.append(f"   🎉 Best for: {best_for}")
            elif 'Season:' in line and 'Glass:' in line:
                formatted_lines.append(f"   🏺 {line}")
            elif 'History:' in line:
                history = line.replace('History:', '').strip()
                formatted_lines.append(f"   📖 History: {history}")
            elif '----------------------------------------' in line:
                formatted_lines.append("\n" + "═" * 60 + "\n")
            elif line and not any(keyword in line for keyword in 
                                ['Match Score', '**', 'Base Spirit', 'Strength', 
                                 'Ingredients', 'Techniques', 'Flavors', 'Best for', 
                                 'Season', 'Glass', 'History', '----------------------------------------']):
                # If it's a regular line that got separated, add it with proper indentation
                formatted_lines.append(f"   {line}")
        
        return '\n'.join(formatted_lines)

    def browse_all(self):
        try:
            if not KB_PATH.exists():
                messagebox.showerror("Error", f"{KB_PATH} file not found!")
                return
            
            self.notebook.select(2)  # Loading tab
            self.progress.start(10)
            
            thread = threading.Thread(target=self.process_browse_all)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to browse cocktails: {str(e)}")

    def process_browse_all(self):
        try:
            process = subprocess.Popen(['swipl', '-q', '-s', str(KB_PATH)], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            stdout, stderr = process.communicate(input="browse_all_cocktails.", timeout=30)
            
            self.root.after(0, lambda: self.display_browse_results(stdout, stderr))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to browse cocktails: {str(e)}"))

    def display_browse_results(self, stdout, stderr):
        self.progress.stop()
        self.notebook.select(1)  # Results tab
        
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', 'end')
        
        self.results_text.insert('1.0', "📚 COMPLETE COCKTAIL DATABASE\n\n")
        self.results_text.insert('end', "═" * 50 + "\n\n")
        
        if stdout:
            formatted_output = self.format_output(stdout)
            self.results_text.insert('end', formatted_output)
            
            cocktail_count = formatted_output.count('🍸 🍸 🍸')
            self.results_count.config(text=f"📚 {cocktail_count} total cocktails in database")
        else:
            self.results_text.insert('end', "❌ No cocktails found in database.")
            self.results_count.config(text="❌ Database empty")
            
        self.results_text.config(state='disabled')
        self.status_label.config(text="● Ready", fg=self.colors['success'])

    def reset_preferences(self):
        # Reset all to defaults
        self.spirit_var.set("no_preference")
        self.flavor_var.set("citrus")
        self.skill_var.set("beginner")
        self.strength_var.set(7)
        self.occasion_var.set("casual_relaxing")
        self.season_var.set("all_seasons")
        
        # Reset button visuals
        for group in self.selected_buttons:
            self.selected_buttons[group] = None
        
        messagebox.showinfo("Reset Complete", "🎯 All preferences have been reset to default values!")
        self.status_label.config(text="● Reset Complete", fg=self.colors['success'])

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCocktailExpertSystem(root)
    root.mainloop()
