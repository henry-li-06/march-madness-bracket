from game2d import GPath, GameApp, GLabel
from bracket import Node


class Bracket(GameApp):

    def __init__(self, width, height, year):
        super().__init__(width=width, height=height)
        Node.init_data(year)

    def start(self):
        self.root = Node('N/A', 0, 600, 300)
        self.root.build_tree()
        self.root.make_predictions()
        self.text = []
        self.lines = []
        self.create_tree()

    def create_tree(self):
        self.add_node(self.root)
        self.add_line(self.root)

    def add_node(self, node):
        self.text.append(
            GLabel(text=node.data, x=node.x, y=node.y, font_size=10))
        if(not node.left is None):
            self.add_node(node.left)
            self.add_node(node.right)

    def add_line(self, node):
        self.lines.append(GPath(points=(node.x, node.y, node.x,
                                        node.left.y), linewidth=1, linecolor='blue'))
        self.lines.append(GPath(points=(
            node.x, node.left.y, node.left.x, node.left.y), linewidth=1, linecolor='blue'))
        self.lines.append(GPath(points=(node.x, node.y, node.x,
                                        node.right.y), linewidth=1, linecolor='blue'))
        self.lines.append(GPath(points=(
            node.x, node.right.y, node.right.x, node.right.y), linewidth=1, linecolor='blue'))
        if(not node.left.left is None):
            self.add_line(node.left)
            self.add_line(node.right)

    def update(self, dt):
        self.draw()

    def draw(self):
        for text in self.text:
            text.draw(self.view)
        for line in self.lines:
            line.draw(self.view)
