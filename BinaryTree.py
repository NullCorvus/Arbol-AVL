from Treenode import Treenode

class BinaryTree():
    def __init__(self):
        self.root = None

    


          
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
