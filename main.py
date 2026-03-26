import flet as ft
import flet_audio as fta 
import os
import platform

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "NOVA x JayPlayer APK"
    page.padding = 20
    
    # --- 1. The Audio Engine ---
    audio_engine = fta.Audio(src="", autoplay=False)
    page.overlay.append(audio_engine)

    # --- 2. Android-Specific State ---
    state = {"songs": [], "index": -1}

    async def scan_music(e=None):
        # Detect if we are on Android or Windows
        if platform.system() == "Windows":
            music_path = os.path.expanduser("~/Music")
        else:
            # Standard Android Music folder path
            music_path = "/storage/emulated/0/Music"
            
        state["songs"] = []
        
        try:
            if os.path.exists(music_path):
                for root, _, files in os.walk(music_path):
                    for f in files:
                        if f.lower().endswith(".mp3"):
                            state["songs"].append(os.path.join(root, f))
            
            if not state["songs"]:
                status.value = "No MP3s found in Music folder."
            else:
                status.value = f"Loaded {len(state['songs'])} songs"
        except Exception as ex:
            status.value = f"Error: {str(ex)}"
            
        page.update()

    async def play_track(e=None):
        if not state["songs"]: 
            return
            
        if state["index"] == -1: 
            state["index"] = 0
        
        current_path = state["songs"][state["index"]]
        audio_engine.src = current_path
        
        # Await is required for flet-audio 0.82.2
        await audio_engine.play()
        
        song_info.value = os.path.basename(current_path)
        play_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED
        page.update()

    async def next_track(e=None):
        if state["songs"]:
            state["index"] = (state["index"] + 1) % len(state["songs"])
            await play_track()

    # --- 3. UI (Mobile Optimized) ---
    status = ft.Text("Ready", color="grey", size=12)
    song_info = ft.Text("Select Scan to begin", size=20, weight="bold", color="cyan", text_align="center")
    play_btn = ft.Button("PLAY", icon=ft.Icons.PLAY_ARROW, on_click=play_track)

    page.add(
        ft.Column([
            ft.Text("JAYPLAYER MOBILE", size=28, weight="bold", color="white"),
            status,
            ft.Divider(color="cyan", height=40),
            ft.Container(
                content=ft.Icon(ft.Icons.MUSIC_NOTE, size=120, color="cyan"),
                alignment=ft.alignment.center,
                padding=40,
                bgcolor="#101025",
                border_radius=30,
            ),
            ft.Container(height=20),
            song_info,
            ft.Row([
                ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_size=40, on_click=next_track),
                play_btn,
                ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_size=40, on_click=next_track),
            ], alignment="center"),
            ft.Container(height=30),
            ft.Button(
                "SCAN SYSTEM MUSIC", 
                icon=ft.Icons.SEARCH, 
                on_click=scan_music,
                width=250,
                color="white",
                bgcolor="#202040"
            )
        ], horizontal_alignment="center")
    )

    await scan_music()

ft.run(main)
