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

    def searchByInvoiceID(self, id):
        return self._searchByInvoiceID(self.root, id)
    #####################
    def _searchByInvoiceID(self, node, id):
        if not node:
            return None
        if node.data.InvoiceId == id:
            return node.data
        elif id < node.data.InvoiceId:
            return self._searchByInvoiceID(node.left, id)
        else:
            return self._searchByInvoiceID(node.right, id)
    

    #####################
    def searchByCustomerID(self, customer_id):
        result = []
        self._searchByCustomerID(self.root, customer_id, result)
        return result

    def _searchByCustomerID(self, node, customer_id, result):
        if not node:
            return
        if node.data.CustomerId == customer_id:
            result.append(node.data)
        self._searchByCustomerID(node.left, customer_id, result)
        self._searchByCustomerID(node.right, customer_id, result)
    #####################
    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if not node:
            new_node = Node(data)
            return new_node
        if data.InvoiceId < node.data.InvoiceId:
            node.left = self._insert(node.left, data)
            if node.left:
                node.left.parent = node
        elif data.InvoiceId > node.data.InvoiceId:
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

    def findMinTotal(self, node):
        if not node:
            return float('inf')
        left_min = self.findMinTotal(node.left)
        right_min = self.findMinTotal(node.right)
        return min(left_min, right_min, node.data.Total)
    
    def inorderTraversal(self, node, result):
        if node:
            self.inorderTraversal(node.left, result)
            result += node.data.Total
            self.inorderTraversal(node.right, result)
    def getTotal(self, node):
        if not node:
            return 0
        total = node.data.Total
        total += self.getTotal(node.left)
        total += self.getTotal(node.right)
        return total