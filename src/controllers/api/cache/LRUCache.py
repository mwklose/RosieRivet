from collections import defaultdict
class Node():
    def __init__(self,sess_key,rr_inst,file):
        self.sess_key = sess_key
        self.rr_inst = rr_inst
        self.file = file
        self.prev = None
        self.next = None
        
class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.size = 0
        self.SentinelNode = Node(None,None,None)
        self.SentinelNode.next = self.SentinelNode
        self.SentinelNode.prev = self.SentinelNode
        self.lookup = defaultdict(lambda : Node())
    
    def moveup(self,key):
        node = self.lookup[key]
        next = self.SentinelNode.next
        self.SentinelNode.next = node
        node.prev = self.SentinelNode
        node.next = next
        next.prev = node
        
    def evict(self):
        last_node = self.SentinelNode.prev
        del self.lookup[last_node.key]
        self.size -= 1
        self.SentinelNode.prev = self.SentinelNode.prev.prev
        self.SentinelNode.prev.next = self.SentinelNode

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        
        if key not in self.lookup:
            return -1

        node = self.lookup[key]
        node.prev.next = node.next
        node.next.prev = node.prev
        self.moveup(key)
        return node.rr_inst,node.file

    def put(self, key, rr_inst, file):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.lookup:
            node = self.lookup[key]
            node.rr_inst = rr_inst
            node.file = file
            node.prev.next = node.next
            node.next.prev = node.prev
        else:
            if(self.size + 1 > self.capacity):
                self.evict()
            self.lookup[key] = Node(key,rr_inst,file)
            self.size += 1
        self.moveup(key)