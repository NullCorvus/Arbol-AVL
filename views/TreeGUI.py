import customtkinter as ctk
from BinaryTree import BinaryTree
import time
import math
import random

class TreeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🌳 Bosque Binario Interactivo 🌳")
        self.geometry("1200x800")
        self.configure(fg_color="#E8F5E8")
        
        # Set nature theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # --- Binary tree object ---
        self.tree = BinaryTree()
        self.node_positions = {}
        self.animation_in_progress = False
        
        # --- Layout ---
        self.create_widgets()
        self.setup_scrollable_canvas()

    def setup_scrollable_canvas(self):
        """Setup the scrollable canvas with proper dimensions"""
        # Configure canvas scrolling region - más ancho para evitar superposición
        self.canvas.configure(scrollregion=(0, 0, 1500, 1500))
        
        # Draw the background
        self.draw_background()

    def draw_background(self):
        """Draw the background with extended ground"""
        self.canvas.delete("background")
        
        # Canvas dimensions for scrolling
        canvas_width = 1500
        canvas_height = 1500
        
        # Sky (top 25% of canvas)
        sky_height = int(canvas_height * 0.25)
        self.canvas.create_rectangle(0, 0, canvas_width, sky_height, 
                                   fill="#87CEEB", outline="", tags="background")
        
        # Ground (remaining 75% of canvas)
        ground_y = sky_height
        self.canvas.create_rectangle(0, ground_y, canvas_width, canvas_height, 
                                   fill="#8B4513", outline="", tags="background")
        
        # Grass line at the top of ground
        self.canvas.create_rectangle(0, ground_y, canvas_width, ground_y + 30, 
                                   fill="#228B22", outline="", tags="background")
        
        # Clouds in sky
        cloud_positions = [(100, 80), (400, 120), (700, 90), (1000, 110), (1300, 80)]
        for x, y in cloud_positions:
            self.canvas.create_oval(x, y, x+80, y+40, fill="white", outline="", tags="background")
            self.canvas.create_oval(x+20, y-10, x+100, y+30, fill="white", outline="", tags="background")
        
        # Sun
        self.canvas.create_oval(1350, 50, 1400, 100, fill="#FFD700", outline="", tags="background")

    def create_widgets(self):
        # Header with nature theme
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=15)
        
        header = ctk.CTkLabel(header_frame, 
                             text="🌿 Bosque Binario Interactivo 🍃", 
                             font=("Arial", 28, "bold"),
                             text_color="#2E7D32")
        header.pack()
        
        subheader = ctk.CTkLabel(header_frame,
                                text="Planta valores y observa cómo crece tu árbol",
                                font=("Arial", 14),
                                text_color="#388E3C")
        subheader.pack(pady=5)

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="#5D4037", corner_radius=15)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Input section
        input_frame = ctk.CTkFrame(main_container, fg_color="#8D6E63", corner_radius=12)
        input_frame.pack(pady=15, padx=15, fill="x")

        self.entry = ctk.CTkEntry(input_frame, 
                                 placeholder_text="🌱 Ingresa valores separados por comas (ej: 8,3,10,1,6)", 
                                 width=600,
                                 height=40,
                                 font=("Arial", 14),
                                 corner_radius=10,
                                 border_color="#4CAF50",
                                 fg_color="#FFF8E1",
                                 text_color="#5D4037")
        self.entry.pack(side="left", padx=15, pady=12)
        
        add_btn = ctk.CTkButton(input_frame, 
                               text="🌿 Plantar", 
                               command=self.add_values,
                               height=40,
                               width=120,
                               font=("Arial", 14, "bold"),
                               corner_radius=10,
                               fg_color="#4CAF50",
                               hover_color="#388E3C",
                               border_color="#2E7D32",
                               border_width=2,
                               text_color="white")
        add_btn.pack(side="left", padx=5)

        # Buttons frame
        btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_container.pack(pady=10)

        btn_frame = ctk.CTkFrame(btn_container, 
                                fg_color="#388E3C", 
                                corner_radius=12,
                                border_color="#2E7D32",
                                border_width=2)
        btn_frame.pack()

        buttons = [
            ("🍃 Preorden", self.show_preorder, "#4CAF50"),
            ("🌺 Inorden", self.show_inorder, "#FF9800"),
            ("🍂 Postorden", self.show_postorder, "#8D6E63"),
            ("🗑️ Limpiar", self.clear_tree, "#F44336")
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(btn_frame, 
                               text=text,
                               command=command,
                               width=140,
                               height=35,
                               font=("Arial", 12, "bold"),
                               corner_radius=8,
                               fg_color=color,
                               hover_color=self.darken_color(color, 20),
                               text_color="white")
            btn.grid(row=0, column=i, padx=6, pady=8)

        # Canvas container with scroll
        canvas_container = ctk.CTkFrame(main_container, 
                                       fg_color="#5D4037", 
                                       corner_radius=12,
                                       border_color="#3E2723",
                                       border_width=2)
        canvas_container.pack(fill="both", expand=True, padx=15, pady=10)

        canvas_label = ctk.CTkLabel(canvas_container, 
                                   text="🌳 Visualización del Árbol (usa scroll para navegar)",
                                   font=("Arial", 14, "bold"),
                                   text_color="#FFF8E1")
        canvas_label.pack(pady=8)

        # Create scrollable canvas frame
        canvas_scroll_frame = ctk.CTkFrame(canvas_container, fg_color="transparent")
        canvas_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create scrollbars and canvas
        self.v_scrollbar = ctk.CTkScrollbar(canvas_scroll_frame, orientation="vertical")
        self.h_scrollbar = ctk.CTkScrollbar(canvas_scroll_frame, orientation="horizontal")
        
        # Canvas más ancho para evitar superposición
        self.canvas = ctk.CTkCanvas(canvas_scroll_frame,
                                   width=1100, 
                                   height=500,
                                   bg="#87CEEB",
                                   highlightthickness=0,
                                   yscrollcommand=self.v_scrollbar.set,
                                   xscrollcommand=self.h_scrollbar.set)
        
        self.v_scrollbar.configure(command=self.canvas.yview)
        self.h_scrollbar.configure(command=self.canvas.xview)

        # Layout with grid for proper scrollbar placement
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        canvas_scroll_frame.grid_rowconfigure(0, weight=1)
        canvas_scroll_frame.grid_columnconfigure(0, weight=1)

        # Bind mouse wheel for scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Output label
        self.output_label = ctk.CTkLabel(main_container, 
                                        text="🌱 Bienvenido! Ingresa valores para comenzar...",
                                        font=("Arial", 13, "bold"),
                                        text_color="#2E7D32",
                                        height=40,
                                        fg_color="#C8E6C9",
                                        corner_radius=10)
        self.output_label.pack(pady=10, padx=15, fill="x")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def darken_color(self, color, amount):
        """Darken a color by given amount"""
        if color.startswith("#"):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def clear_tree(self):
        """Clear the tree and reset"""
        if self.animation_in_progress:
            return
            
        self.tree = BinaryTree()
        self.canvas.delete("tree")
        self.canvas.delete("highlight")
        self.node_positions.clear()
        self.show_message("🗑️ Árbol limpiado! Listo para nuevos valores.", "#FF9800")

    def add_values(self):
        if self.animation_in_progress:
            return
            
        text = self.entry.get().strip()
        if not text:
            self.show_message("🌱 Por favor ingresa algunos valores.", "#FF9800")
            return

        try:
            values = [int(x.strip()) for x in text.split(",") if x.strip()]
            for val in values:
                self.tree.add(val)
            
            self.animate_tree_growth(values)
            self.entry.delete(0, 'end')
            
        except ValueError:
            self.show_message("❌ Solo números separados por comas.", "#FF5252")

    def animate_tree_growth(self, values):
        self.animation_in_progress = True
        self.show_message("🌱 Plantando valores...", "#4CAF50")
        
        # Redraw background and tree
        self.draw_background()
        self.draw_tree()
        
        # Auto-scroll to show the tree properly
        self.auto_scroll_to_tree()
        
        self.show_message(f"🌳 ¡Árbol crecido con {len(values)} valores!", "#4CAF50")
        self.animation_in_progress = False

    def auto_scroll_to_tree(self):
        """Auto-scroll to show the tree properly"""
        self.canvas.yview_moveto(0.3)  # Scroll down to center the tree

    def draw_tree(self):
        """Draw the tree with optimized layout to avoid overlaps"""
        # Clear previous tree
        self.canvas.delete("tree")
        self.canvas.delete("highlight")
        self.node_positions.clear()
        
        if self.tree.root:
            # Calculate tree depth for better spacing
            depth = self.get_tree_depth(self.tree.root)
            
            # Position the tree lower and centered
            ground_level = 400  # Moved down from 450
            root_x = 750  # Centered in wider canvas
            root_y = ground_level
            
            # Draw main trunk
            trunk_height = 80
            trunk_width = 25
            self.canvas.create_rectangle(root_x - trunk_width//2, root_y - trunk_height,
                                       root_x + trunk_width//2, root_y,
                                       fill="#8B4513", outline="#5D4037", width=2, tags="tree")
            
            # Calculate initial offset based on tree depth
            initial_offset = 200 + (depth * 30)  # More space for deeper trees
            
            # Draw the binary tree with optimized layout
            self._draw_tree_node(self.tree.root, root_x, root_y, initial_offset, 0, depth)

    def get_tree_depth(self, node):
        """Calculate the depth of the tree"""
        if node is None:
            return 0
        left_depth = self.get_tree_depth(node.left)
        right_depth = self.get_tree_depth(node.right)
        return max(left_depth, right_depth) + 1

    def _draw_tree_node(self, node, x, y, offset, level, max_depth):
        """Draw tree node with collision avoidance"""
        if node is None:
            return

        # Store node position
        self.node_positions[node.value] = (x, y)

        # Choose colors based on level
        node_color = self.get_node_color(level)
        branch_color = "#5D4037"

        # Calculate dynamic spacing based on tree depth
        vertical_spacing = 80 + (max_depth * 5)  # More vertical space for deep trees
        
        # Adjust horizontal spacing to prevent overlap
        # Use a more gradual reduction for deeper levels
        next_offset = offset * (0.7 if level < 3 else 0.8)
        
        # Draw left child with adjusted positioning
        if node.left:
            left_x = x - offset
            left_y = y + vertical_spacing
            
            # Check if this position would cause overlap
            if not self.would_overlap(left_x, left_y, level + 1):
                self.draw_root_branch(x, y, left_x, left_y, branch_color, level)
                self._draw_tree_node(node.left, left_x, left_y, next_offset, level + 1, max_depth)
            else:
                # Adjust position to avoid overlap
                adjusted_x = x - offset * 1.2
                self.draw_root_branch(x, y, adjusted_x, left_y, branch_color, level)
                self._draw_tree_node(node.left, adjusted_x, left_y, next_offset, level + 1, max_depth)

        # Draw right child with adjusted positioning
        if node.right:
            right_x = x + offset
            right_y = y + vertical_spacing
            
            # Check if this position would cause overlap
            if not self.would_overlap(right_x, right_y, level + 1):
                self.draw_root_branch(x, y, right_x, right_y, branch_color, level)
                self._draw_tree_node(node.right, right_x, right_y, next_offset, level + 1, max_depth)
            else:
                # Adjust position to avoid overlap
                adjusted_x = x + offset * 1.2
                self.draw_root_branch(x, y, adjusted_x, right_y, branch_color, level)
                self._draw_tree_node(node.right, adjusted_x, right_y, next_offset, level + 1, max_depth)

        # Draw the node
        self.draw_root_node(x, y, node.value, node_color, level)

    def would_overlap(self, x, y, level):
        """Check if a new node would overlap with existing nodes"""
        node_radius = 20 + level
        for pos_x, pos_y in self.node_positions.values():
            distance = math.sqrt((x - pos_x)**2 + (y - pos_y)**2)
            if distance < node_radius * 2.5:  # 2.5 times radius for safe spacing
                return True
        return False

    def draw_root_branch(self, x1, y1, x2, y2, color, level):
        """Draw a root branch with natural curve"""
        branch_width = max(2, 8 - level)
        
        # Create a natural curve for roots
        control_x = (x1 + x2) // 2
        control_y = (y1 + y2) // 2 + 20
        
        self.canvas.create_line(x1, y1, control_x, control_y, x2, y2,
                              fill=color, width=branch_width, smooth=True, tags="tree")

    def draw_root_node(self, x, y, value, color, level):
        """Draw a root node with value"""
        radius = 18 + (3 - level)  # Larger nodes at higher levels
        
        # Root nodule circle
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                              fill=color, outline="#FFFFFF", width=2, tags="tree")
        
        # Node value
        font_size = max(8, 12 - level // 2)
        self.canvas.create_text(x, y, text=str(value), 
                              font=("Arial", font_size, "bold"), 
                              fill="#FFFFFF", tags="tree")
        
        # Add subtle texture for root-like appearance
        if level > 0:
            self.canvas.create_oval(x - radius + 3, y - radius + 3, 
                                  x + radius - 3, y + radius - 3,
                                  outline=self.darken_color(color, 30), width=1, tags="tree")

    def get_node_color(self, level):
        """Get node color based on tree level"""
        colors = ["#8B4513", "#A0522D", "#CD853F", "#D2691E", "#8B7355", "#BC8F8F"]
        return colors[level % len(colors)]

    def show_preorder(self):
        if not self.tree.root or self.animation_in_progress:
            return
        self.animate_traversal("PREORDEN", self.tree.pre_order(), "🍃", "#4CAF50")

    def show_inorder(self):
        if not self.tree.root or self.animation_in_progress:
            return
        self.animate_traversal("INORDEN", self.tree.in_order(), "🌺", "#FF9800")

    def show_postorder(self):
        if not self.tree.root or self.animation_in_progress:
            return
        self.animate_traversal("POSTORDEN", self.tree.post_order(), "🍂", "#8D6E63")

    def animate_traversal(self, traversal_type, traversal_list, emoji, color):
        self.animation_in_progress = True
        result_text = f"{emoji} {traversal_type}: {traversal_list}"
        self.show_message(f"🔍 Realizando {traversal_type}...", color)
        
        def highlight_next(index=0):
            if index < len(traversal_list):
                value = traversal_list[index]
                if value in self.node_positions:
                    x, y = self.node_positions[value]
                    self.highlight_node(x, y, color)
                    self.scroll_to_node(x, y)
                
                current_values = traversal_list[:index+1]
                progress = f"{index+1}/{len(traversal_list)}"
                animated_text = f"{emoji} {traversal_type} [{progress}]: {' → '.join(map(str, current_values))}"
                self.output_label.configure(text=animated_text, text_color=color)
                
                self.after(700, lambda: highlight_next(index + 1))
            else:
                self.output_label.configure(text=result_text)
                self.show_message(f"✅ {traversal_type} completado!", color)
                self.animation_in_progress = False

        highlight_next()

    def scroll_to_node(self, x, y):
        """Scroll canvas to make node visible"""
        # Get visible area
        x0 = self.canvas.canvasx(0)
        y0 = self.canvas.canvasy(0)
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        
        # If node not visible, scroll to it
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            # Calculate normalized scroll position
            scroll_y = (y - self.canvas.winfo_height() / 3) / 1500
            scroll_x = (x - self.canvas.winfo_width() / 2) / 1500
            self.canvas.yview_moveto(max(0, min(1, scroll_y)))
            self.canvas.xview_moveto(max(0, min(1, scroll_x)))

    def highlight_node(self, x, y, color):
        """Highlight a node during traversal"""
        radius = 25
        # Create pulsing highlight effect
        for size in [radius, radius + 5, radius + 10]:
            highlight = self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                              outline=color, width=2, tags="highlight")
            self.after(100, lambda h=highlight: self.canvas.delete(h))

    def show_message(self, message, color):
        """Show message"""
        self.output_label.configure(text=message, text_color=color)
