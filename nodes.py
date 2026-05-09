# nodes.py
# Combined: SimpleNumberCounter, SimpleConstantNumber, SimpleLogicBoolean, StringFromList, LoadTextFile

import math

# ── Counter state ────────────────────────────────────────────────────────────
_counter_state = {"value": 0}


def wrapIndex(index, length):
    if length == 0:
        print("ezXY: Divide by zero error, returning 0.")
        return 0, 0
    index_mod = int(math.fmod(index, length))
    wraps = index // length
    return index_mod, wraps


class SimpleNumberCounter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode":  (["increment", "decrement", "increment_to_stop", "decrement_to_stop"],),
                "stop":  ("FLOAT", {"default": 100.0, "min": 0.0, "max": 99999.0, "step": 1.0}),
                "start": ("INT",   {"default": 0, "min": 0, "max": 99999}),
                "step":  ("INT",   {"default": 1, "min": 0, "max": 99999}),
            },
            "optional": {
                "reset_bool": ("NUMBER",),
            }
        }

    FUNCTION = "count"
    CATEGORY = "Simple Utils"
    RETURN_TYPES = ("NUMBER", "FLOAT", "INT")
    RETURN_NAMES = ("number", "float", "int")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def count(self, mode, stop, start, step, reset_bool=None):
        global _counter_state
        if reset_bool is not None and float(reset_bool) > 0:
            _counter_state["value"] = start
        v = _counter_state["value"]
        if mode in ("increment", "increment_to_stop"):
            next_v = v + step
            if next_v >= stop:
                next_v = start
            _counter_state["value"] = next_v
        else:
            next_v = v - step
            if next_v < 0:
                next_v = int(stop)
            _counter_state["value"] = next_v
        return (float(v), float(v), int(v))


class SimpleConstantNumber:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 1.0, "min": -99999.0, "max": 99999.0, "step": 1.0}),
            }
        }

    FUNCTION = "output"
    CATEGORY = "Simple Utils"
    RETURN_TYPES = ("NUMBER", "FLOAT", "INT")
    RETURN_NAMES = ("NUMBER", "FLOAT", "INT")

    def output(self, value):
        return (float(value), float(value), int(value))


class SimpleLogicBoolean:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True}),
            }
        }

    FUNCTION = "output"
    CATEGORY = "Simple Utils"
    RETURN_TYPES = ("BOOLEAN", "NUMBER", "INT", "FLOAT")
    RETURN_NAMES = ("BOOLEAN", "NUMBER", "INT", "FLOAT")

    def output(self, boolean):
        v = 1 if boolean else 0
        return (boolean, float(v), int(v), float(v))


class StringFromList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "list_input": ("STRING", {"forceInput": True},),
                "index": ("INT", {"default": 0, "min": -999, "max": 999, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "INT",)
    RETURN_NAMES = ("list item", "size", "wraps",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, False, True)
    FUNCTION = "pick"
    CATEGORY = "ezXY/utility"

    def pick(self, list_input, index):
        length = len(list_input)
        wraps_list, item_list = [], []
        for i in index:
            index_mod, wraps = wrapIndex(i, length)
            wraps_list.append(wraps)
            item_list.append(list_input[index_mod])
        return (item_list, length, wraps_list,)


class LoadTextFile:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "/input/yourfile.txt", "multiline": False}),
            }
        }

    FUNCTION = "load"
    CATEGORY = "Simple Utils"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def load(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return (f.read(),)
        except Exception as e:
            print(f"[LoadTextFile] Error reading '{file_path}': {e}")
            return ("",)


NODE_CLASS_MAPPINGS = {
    "Number Counter":  SimpleNumberCounter,
    "Constant Number": SimpleConstantNumber,
    "Logic Boolean":   SimpleLogicBoolean,
    "StringFromList":  StringFromList,
    "LoadTextFile":    LoadTextFile,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Number Counter":  "Number Counter (Simple)",
    "Constant Number": "Constant Number (Simple)",
    "Logic Boolean":   "Logic Boolean (Simple)",
    "StringFromList":  "String From List",
    "LoadTextFile":    "Load Text File (Simple)",
}
