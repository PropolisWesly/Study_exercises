class Tree:
    def __init__(self, Node=None):
        self.root = Node

    @staticmethod
    def _pre_oder(node):
        if node is None:
            return
        print(node.value)
        Tree._pre_oder(node.left)
        Tree._pre_oder(node.right)

    def pre_oder(self):
        if self.root is None:
            return
        node = self.root
        print(node.value)
        Tree._pre_oder(node.left)
        Tree._pre_oder(node.right)

    @staticmethod
    def _post_oder(node):
        if node is None:
            return
        Tree._post_oder(node.left)
        Tree._post_oder(node.right)
        print(node.value)

    def post_oder(self):
        if self.root is None:
            return
        node = self.root
        Tree._post_oder(node.left)
        Tree._post_oder(node.right)
        print(node.value)

    @staticmethod
    def _height(node):
        if node is None:
            return 0
        node_left_lenght = Tree._height(node.left)
        node_right_lenght = Tree._height(node.right)
        return max(node_left_lenght, node_right_lenght) + 1

    def height(self):
        if self.root is None:
            return 0
        node = self.root
        node_left_lenght = Tree._height(node.left)
        node_right_lenght = Tree._height(node.right)
        return max(node_left_lenght, node_right_lenght) + 1

    @staticmethod
    def _print_level(node, level):
        if node is None:
            return
        if level == 0:
            return print(node.value)
        elif level > 0:
            Tree._print_level(node.left, level - 1)
            Tree._print_level(node.right, level - 1)

    def width_oder(self):
        h = self.height()
        for i in range(h):
            self._print_level(self.root, i)

    @staticmethod
    def _max_value(node):
        if node is None:
            return - float('inf')
        max_left_value = Tree._max_value(node.left)
        max_right_value = Tree._max_value(node.right)
        return max(max_left_value, max_right_value, node.value)

    def max_value(self):
        if self.root is None:
            return
        node = self.root
        max_left_value = Tree._max_value(node.left)
        max_right_value = Tree._max_value(node.right)
        return max(max_left_value, max_right_value, node.value)


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

a = Node(1)
a.left = Node(2)
a.right = Node(3)
a.right.right = Node(6)
a.left.left = Node(4)
a.left.right = Node(5)
tree = Tree(a)
tree.pre_oder()
print('\n\n\n\n')
tree.post_oder()
print('\n\n\n\n')
print(tree.height())
print('\n\n')
tree.width_oder()
print(tree.max_value())
print('\n\n')
print(29 % 3)
line = 'sosaty'
print(line[-1])


print(bin(44))
line = str(bin(3))
line = line.replace('0b', '')
print(line)
