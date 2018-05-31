import enum

class NodeType(enum.Enum):
    Cond = 0
    Loop = 1
    Normal = 2
    Start = 3
    Exit = 4
    DoLoop = 5
    MergeNode = 6


class Parser:
    graph = None
    nodes = {}

    def __init__(self):
        f = open('parser.py')
        self.createGraph(f.read())
        pass

    def createGraph(self, code):
        codeLines = code.split('\n')

        counter = 1
        parentNode = None
        mergeParentNode = None

        for line in codeLines:
            line = line.strip()
            if self.graph is None:
                nod = Node(counter, None, line)
                self.graph = nod

            else:
                if line.startswith('if'):
                    mNod = Node(counter, parent, None, NodeType.MergeNode)
                    mergeParentNode = mNod
                    counter += 1

                    nod = Node(counter, parent, line, NodeType.Cond)
                    mNod.addChild(nod)
                    parentNode = nod

                elif line.startswith('else if') or line.startswith('else'):
                    mNod = Node(counter, parent, None, NodeType.MergeNode)
                    mergeParentNode = mNod
                    counter += 1

                    nod = Node(counter, parent, line, NodeType.Cond)
                    mNod.addChild(nod)
                    parentNode = nod

                elif line.startswith('for') or line.startswith('while'):
                    mNod = Node(counter, parent, None, NodeType.MergeNode)
                    counter += 1

                    nod = Node(counter, parent, line, NodeType.Loop)
                    mNod.addChild(nod)

                    self.graph.addChild(Node(counter, parent, line, NodeType.Loop))

                elif line.startswith('do'):
                    mNod = Node(counter, parent,None, NodeType.MergeNode)
                    self.graph.setNextNode(mNod)
                    counter += 1

                    nod = Node(counter, parent, line, NodeType.DoLoop)
                    mNod.addChild(nod)

                    self.graph.addChild(Node(counter, parent, line, NodeType.DoLoop))

                elif line.startswith('continue'):
                    self.graph.addChild(Node(counter, parent, line, NodeType.Normal))

                elif line.startswith('break'):
                    self.graph.addChild(Node(counter, parent, line, NodeType.Normal))

                else:
                    self.graph.addChild(Node(counter, parent, line, NodeType.Normal))

            parent = nod

            self.nodes[counter] = nod
            self.graph.addChild(nod)

            counter += 1

Parser()

class Node:
    id = None
    content = None
    explored = False
    children = {}
    parent = None
    nextNode = None
    previousNode = None
    nodeType = NodeType.Normal
    mergeNode = False

    def __init__(self, id, parent, previousNode, content, nodeType, mergeNode=False):
        self.explored = False
        self.id = id
        self.parent = parent
        self.nodeType = nodeType
        self.content = content
        self.mergeNode = mergeNode
        self.previousNode = previousNode

    def addChild(self, child):
        self.children[child.id] = child

    def isExplored(self):
        return self.explored

    def setExplored(self, explored):
        self.explored = explored

    def setNextNode(self, nextNode):
        self.nextNode = nextNode
#
# class MergeNode:
#     children = {}
#     parent = None
#     nextNode = None
#
#     def __init__(self, id, parent):
#         self.parent = parent
#         self.id = id
#
#     def addChild(self, node):
#         self.children[node.id] = node
#
#     def setNextNode(self, node):
#         self.nextNode = node