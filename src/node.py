class Node:
    def __init__(self):
        self.next_node = None
    
    def set_next_node(self, node):
        self.next_node = node

    def process(self, data):
        pass

    def run(self, data, debug = False):
        processed_data = self.process(data)

        if (debug):
            print(f"End of node, entered data: \n{data}\nprocessed data:\n{processed_data}")

        if (self.next_node):
            return self.next_node.run(processed_data, debug)
        
        return processed_data