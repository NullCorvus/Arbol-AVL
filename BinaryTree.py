from Treenode import Treenode

class BinaryTree():
    def __init__(self):
        self.root = None

    def add(self, value):
        self.root = self._add_recursive(self.root, value)
        print("Inorder:", self.in_order())
        print("Preorder:", self.pre_order())



    def _add_recursive(self, node, value):

        # Inserción BST normal
        if not node:
            return Treenode(value)

        if value < node.value:
            node.left = self._add_recursive(node.left, value)
        else:
            node.right = self._add_recursive(node.right, value)

        # Actualizar altura
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        # Factor de balance
        balance = self.get_balance(node)

        # --- CASOS DE DESBALANCE ---

        # 1. Left Left
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        # 2. Right Right
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        # 3. Left Right
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # 4. Right Left
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node



    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self,node):
        x = node.left
        t2 = x.right

        x.right = node
        node.left = t2

        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))
        x.height = 1 + max(self.get_height(x.left),self.get_height(x.right))
         
        
        return x 
    
    def left_rotate(self, node):
        y = node.right
        t2 = y.left

        y.left = node
        node.right = t2

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y


        
    def pre_order(self):
        return self.recursive_pre(self.root)

    def recursive_pre(self, node):
        if node is None:
            return []
        return ([node.value] + self.recursive_pre(node.left) + self.recursive_pre(node.right))        

    def in_order(self):
        return self.recursive_in(self.root)

    def recursive_in(self, node):
        if node is None:
            return []
        return ( self.recursive_in(node.left) + [node.value] + self.recursive_in(node.right))        

    def post_order(self):
        return self.recursive_post(self.root)

    def recursive_post(self, node):
        if node is None:
            return []
        return (self.recursive_post(node.left) + self.recursive_post(node.right) + [node.value])        
