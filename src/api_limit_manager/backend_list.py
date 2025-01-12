from datetime import timedelta

class BackendList:
    def __init__(self):
        self.list = []

    def start(self, uid, start_time):
        end_time = start_time + timedelta(minutes=5)
        self.list.append((uid, start_time, end_time))

    def done(self, uid, end_time):
        found = None
        for i, item in enumerate(self.list):
            if item[0] == uid:
                found = self.list.pop(i)
                break
        if found is None:
            raise Exception(f"Not found: {uid}")
        start_time = found[1]

        index = 0
        for i in range(len(self.list) - 1, -1, -1):
            item = self.list[i]
            if item[2] <= end_time:
                index = i + 1
                break
        self.list.insert(index, (uid, start_time, end_time))

    def get_time(self, index):
        if index is None or index > len(self.list):
            return None
        return self.list[-index][2]
