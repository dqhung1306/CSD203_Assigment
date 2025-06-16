from Node import Node
class AVLTree:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        if not node:
            return -1
        return 1 + max(self.getHeight(node.left), self.getHeight(node.right))

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def countNodes(self, node):
        if not node:
            return 0
        return 1 + self.countNodes(node.left) + self.countNodes(node.right)

    def rotateLeft(self, node):
        nodeRight = node.right
        nodeRightLeft = nodeRight.left
        node.right = nodeRightLeft
        nodeRight.left = node
        if nodeRightLeft:
            nodeRightLeft.parent = node
        nodeRight.parent = node.parent
        node.parent = nodeRight
        if nodeRight.parent is None:
            self.root = nodeRight
        elif nodeRight.parent.left == node:
            nodeRight.parent.left = nodeRight
        else:
            nodeRight.parent.right = nodeRight
        node.height = self.getHeight(node)
        nodeRight.height = self.getHeight(nodeRight)
        return nodeRight

    def rotateRight(self, node):
        nodeLeft = node.left
        nodeLeftRight = nodeLeft.right
        node.left = nodeLeftRight
        nodeLeft.right = node
        if nodeLeftRight:
            nodeLeftRight.parent = node
        nodeLeft.parent = node.parent
        node.parent = nodeLeft
        if nodeLeft.parent is None:
            self.root = nodeLeft
        elif nodeLeft.parent.left == node:
            nodeLeft.parent.left = nodeLeft
        else:
            nodeLeft.parent.right = nodeLeft
        node.height = self.getHeight(node)
        nodeLeft.height = self.getHeight(nodeLeft)
        return nodeLeft

    def search(self, id):
        return self._search(self.root, id)

    def _search(self, node, id):
        if not node or node.data.Id == id:
            return node
        if id < node.data.Id:
            return self._search(node.left, id)
        return self._search(node.right, id)

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if not node:
            new_node = Node(data)
            return new_node
        if data.Id < node.data.Id:
            node.left = self._insert(node.left, data)
            if node.left:
                node.left.parent = node
        elif data.Id > node.data.Id:
            node.right = self._insert(node.right, data)
            if node.right:
                node.right.parent = node
        else:
            return node
        node.height = self.getHeight(node)
        balance = self.getBalance(node)
        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rotateRight(node)
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.rotateLeft(node)
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)
        return node

    def findMin(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node

    def delete(self, id):
        self.root = self._delete(self.root, id)

    def _delete(self, node, id):
        if not node:
            return node
        if id < node.data.Id:
            node.left = self._delete(node.left, id)
        elif id > node.data.Id:
            node.right = self._delete(node.right, id)
        else:
            if not node.left and not node.right:
                if node.parent:
                    if node.parent.left == node:
                        node.parent.left = None
                    else:
                        node.parent.right = None
                if node == self.root:
                    self.root = None
                return None
            if not node.left:
                temp = node.right
                if temp:
                    temp.parent = node.parent
                if node.parent:
                    if node.parent.left == node:
                        node.parent.left = temp
                    else:
                        node.parent.right = temp
                if node == self.root:
                    self.root = temp
                return temp
            elif not node.right:
                temp = node.left
                if temp:
                    temp.parent = node.parent
                if node.parent:
                    if node.parent.left == node:
                        node.parent.left = temp
                    else:
                        node.parent.right = temp
                if node == self.root:
                    self.root = temp
                return temp
            else:
                minNode = self.findMin(node.right)
                node.data = minNode.data
                node.right = self._delete(node.right, minNode.data.Id)
        node.height = self.getHeight(node)
        balance = self.getBalance(node)
        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rotateRight(node)
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.rotateLeft(node)
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)
        return node

    def inorderTraversal(self, node, result):
        if node:
            self.inorderTraversal(node.left, result)
            result.append(node.data)
            self.inorderTraversal(node.right, result)
    