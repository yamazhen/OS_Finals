class TLB:
    def __init__(self, size=4):
        self.size = size
        self.entries = {}
        self.access_order = []
        self.hits = 0
        self.misses = 0

    def invalidate(self, page_number):
        if page_number in self.entries:
            del self.entries[page_number]
            if page_number in self.access_order:
                self.access_order.remove(page_number)
    
    def lookup(self, page_number):
        if page_number in self.entries:
            self.hits += 1
            if page_number in self.access_order:
                self.access_order.remove(page_number)
            self.access_order.append(page_number)
            return self.entries[page_number]
        else:
            self.misses += 1
            return None
    
    def update(self, page_number, frame_number):
        if page_number in self.entries:
            if page_number in self.access_order:
                self.access_order.remove(page_number)
        elif len(self.entries) >= self.size:
            if self.access_order:
                lru_page = self.access_order.pop(0)
                if lru_page in self.entries:
                    del self.entries[lru_page]
        
        self.entries[page_number] = frame_number
        self.access_order.append(page_number)
    
    def get_hit_ratio(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0
