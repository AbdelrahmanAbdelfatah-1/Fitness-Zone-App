def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def binary_search(sorted_data, target):
    low, high = 0, len(sorted_data) - 1
    target = target.lower()
    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_data[mid].lower()
        if mid_val == target:
            return mid, sorted_data
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, sorted_data



class Stack :
    def __init__(self) :
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, frame):
        if self.items:
            self.items[-1].pack_forget()
        self.items.append(frame)
        frame.pack(fill="both", expand=True)

    def pop(self):
        if len(self.items) <= 1:
            return None

        current_frame = self.items.pop()
        current_frame.pack_forget()

        previous_frame = self.items[-1]
        previous_frame.pack(fill="both", expand=True)
        return previous_frame
