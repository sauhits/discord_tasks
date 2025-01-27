import ctypes

def sort(raw_text: list):
    lib = ctypes.cdll.LoadLibrary("./src/sortWrapper.so")
    lib.sortList.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
    lib.sortList.restype = ctypes.POINTER(ctypes.c_char_p)
    lib.freeList.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
    lib.freeList.restype = None

    task_bytes = [f"{deadline}.{title}".encode("utf-8") for deadline, title in raw_text]

    task_array = (ctypes.c_char_p * len(task_bytes))(*task_bytes)

    sorted_task_array = lib.sortList(len(task_bytes), task_array)

    sorted_task = [sorted_task_array[i].decode("utf-8") for i in range(len(task_bytes))]
    lib.freeList(len(task_bytes), sorted_task_array)

    return sorted_task