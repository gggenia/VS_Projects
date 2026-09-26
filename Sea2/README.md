# Sea2

A small Python desktop GUI with three buttons that display and speak `Hello`.
Choose a childlike, woman, or man voice.

## Run

Install the speech dependency once from this folder:

```powershell
python -m pip install -r requirements.txt
```

Then start the app:

```powershell
python main.py
```

The app uses Tkinter for its window, and online neural speech for the three voices. An internet connection is required to generate audio; the text `Hello` is sent to Microsoft's speech service.
