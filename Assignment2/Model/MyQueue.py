class NodeQ:
    def __init__(self,data):
        self.data = data
        self.next = None
class My_Queue:
    def __init__(self):
        self.head = None
        self.tail = None
    def isEmpty(self):
        return self.head ==None
    def EnQueue(self, data):
        node = NodeQ(data)
        if self.isEmpty():
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
    #end def
    def DeQueue(self):
        if self.isEmpty():
            return None
        data = self.head.data
        self.head = self.head.next
        return data
#end class    
