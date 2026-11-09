class KeyTiming:
    """Pair key events from the focused lab widget using Tk timestamps."""

    def __init__(self):
        self._pressed = {}

    def press(self, keycode, keysym, timestamp):
        if keycode in self._pressed:
            return
        if len(keysym) == 1 and keysym.isalnum():
            category = "ALPHANUMERIC"
        elif keysym == "space":
            category = "SPACE"
        else:
            category = "SPECIAL"
        self._pressed[keycode] = (category, timestamp)

    def release(self, keycode, timestamp):
        press = self._pressed.pop(keycode, None)
        if press is None:
            return None
        category, start = press
        return {
            "action": "UP",
            "key_category": category,
            "dwell_ms": (timestamp - start) % (2**32),
        }

    def clear(self):
        self._pressed.clear()
