from Treenode import Treenode

class BinaryTree():
    def __init__(self):
        self.root = None

    

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
