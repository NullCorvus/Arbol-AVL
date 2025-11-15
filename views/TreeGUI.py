import customtkinter as ctk
from BinaryTree import BinaryTree


class TreeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Binary Tree Visualizer 🌳")
        self.geometry("900x600")

        # --- Binary tree object ---
        self.tree = BinaryTree()

        # --- Layout ---
        self.create_widgets()

    def create_widgets(self):
        # Entry to add values
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter values separated by commas (e.g. 8,3,10,1,6)", width=400)
        self.entry.pack(pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)

        add_btn = ctk.CTkButton(btn_frame, text="Add Values", command=self.add_values)
        add_btn.grid(row=0, column=0, padx=10)

        pre_btn = ctk.CTkButton(btn_frame, text="Preorder", command=self.show_preorder)
        pre_btn.grid(row=0, column=1, padx=10)

        in_btn = ctk.CTkButton(btn_frame, text="Inorder", command=self.show_inorder)
        in_btn.grid(row=0, column=2, padx=10)

        post_btn = ctk.CTkButton(btn_frame, text="Postorder", command=self.show_postorder)
        post_btn.grid(row=0, column=3, padx=10)

        # Canvas for tree drawing
        self.canvas = ctk.CTkCanvas(self, width=850, height=400, bg="#F0F0F0")
        self.canvas.pack(pady=10)

        # Label to show traversal results
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.output_label.pack(pady=10)

    # --- Logic methods ---
    def add_values(self):
        text = self.entry.get().strip()
        if not text:
            self.output_label.configure(text="Please enter some values first.")
            return

        # Reset tree and insert new values
        self.tree = BinaryTree()
        try:
            values = [int(x.strip()) for x in text.split(",") if x.strip()]
            for val in values:
                self.tree.add(val)
            self.draw_tree()
            self.output_label.configure(text="Tree updated successfully!")
        except ValueError:
            self.output_label.configure(text="❌ Please enter only numbers separated by commas.")

    # --- Traversal display methods ---
    def show_preorder(self):
        self.output_label.configure(text=f"Preorder: {self.tree.pre_order()}")

    def show_inorder(self):
        self.output_label.configure(text=f"Inorder: {self.tree.in_order()}")

    def show_postorder(self):
        self.output_label.configure(text=f"Postorder: {self.tree.post_order()}")

    # --- Draw the tree recursively ---
    def draw_tree(self):
        self.canvas.delete("all")
        if self.tree.root:
            self._draw_node(self.tree.root, 425, 50, 200)

    def _draw_node(self, node, x, y, offset):
        if node is None:
            return

        # Draw the node circle
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#8BC34A", outline="black")
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

        # Draw left branch
        if node.left:
            self.canvas.create_line(x, y + radius, x - offset, y + 80 - radius, arrow=None)
            self._draw_node(node.left, x - offset, y + 80, offset // 2)

        # Draw right branch
        if node.right:
            self.canvas.create_line(x, y + radius, x + offset, y + 80 - radius, arrow=None)
            self._draw_node(node.right, x + offset, y + 80, offset // 2)
