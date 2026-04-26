import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    return hash_password(password) == hashed


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")