import asyncio
import tempfile
import threading
import tkinter as tk
from pathlib import Path

import edge_tts
from playsound3 import playsound


class Sea2App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.speech_lock = threading.Lock()
        self.voice_options = (
            ("Kid", "en-US-AnaNeural"),
            ("Woman", "en-US-AriaNeural"),
            ("Man", "en-US-GuyNeural"),
        )
        self.root.title("Sea2")
        self.root.geometry("480x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f6f2")

        content = tk.Frame(root, bg="#f3f6f2", padx=36, pady=32)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Sea2",
            font=("Segoe UI", 24, "bold"),
            fg="#183a35",
            bg="#f3f6f2",
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Choose a voice for Hello.",
            font=("Segoe UI", 11),
            fg="#52645f",
            bg="#f3f6f2",
        ).pack(anchor="w", pady=(4, 24))

        self.message = tk.Label(
            content,
            text="Ready when you are.",
            font=("Segoe UI", 14),
            fg="#183a35",
            bg="#f3f6f2",
            height=2,
        )
        self.message.pack(anchor="w", pady=(0, 14))

        buttons = tk.Frame(content, bg="#f3f6f2")
        buttons.pack(fill="x")
        for label, voice_id in self.voice_options:
            tk.Button(
                buttons,
                text=label,
                command=lambda voice_id=voice_id: self.say_hello(voice_id),
                font=("Segoe UI", 10, "bold"),
                fg="#ffffff",
                bg="#18715e",
                activebackground="#125b4c",
                activeforeground="#ffffff",
                relief="flat",
                padx=10,
                pady=10,
                cursor="hand2",
            ).pack(side="left", expand=True, fill="x", padx=4)

    def say_hello(self, voice_id: str) -> None:
        self.message.configure(text="Hello")
        threading.Thread(
            target=self.speak_hello,
            args=(voice_id,),
            daemon=True,
        ).start()

    def speak_hello(self, voice_id: str) -> None:
        try:
            with self.speech_lock, tempfile.TemporaryDirectory() as directory:
                audio_path = Path(directory) / "hello.mp3"
                speech = edge_tts.Communicate("Hello", voice_id)
                asyncio.run(speech.save(str(audio_path)))
                playsound(str(audio_path))
        except Exception:
            self.root.after(
                0,
                lambda: self.message.configure(
                    text="Speech unavailable. Check your internet connection."
                ),
            )


def main() -> None:
    root = tk.Tk()
    Sea2App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
