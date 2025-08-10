"""
Control Panel Test
"""
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import io
import base64
import flet as ft
from py_now_playing import MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode, PlaybackInfo, MediaTimeline, PyNowPlaying, MediaInfo


async def main(page: ft.Page):
    page.title = "Media Control UI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    pbc = PyNowPlaying(aumid="music.amazon.com-6BE721EE_pwn81ww419gp8!App")
    await pbc.initalize_mediamanager()

    async def play(e):
        await pbc.play()

    async def pause(e):
        await pbc.pause()

    async def stop(e):
        await pbc.stop()

    async def rewind(e):
        await pbc.rewind()

    async def fast_forward(e):
        await pbc.fast_forward()

    async def next_track(e):
        await pbc.next_track()

    async def previous_track(e):
        await pbc.previous_track()

    async def toggle_play_pause(e):
        await pbc.toggle_play_pause()

    async def update_media_info():
        media_info = await pbc.get_media_info()
        playback_status_pbc = await pbc.get_playback_info()
        timeline_pbc = await pbc.get_timeline_properties()
        status = None

        # Check playback_status_pbc for None
        if playback_status_pbc is not None:
            if playback_status_pbc.playback_status == MediaPlaybackStatus.PLAYING:
                status = 'Playing'
            elif playback_status_pbc.playback_status == MediaPlaybackStatus.PAUSED:
                status = 'Paused'
            elif playback_status_pbc.playback_status == MediaPlaybackStatus.STOPPED:
                status = 'Stopped'
            else:
                status = 'Unknown'
        else:
            status = 'Unknown'

        # Check media_info for None and its attributes
        if media_info is not None:
            artist.value = f"{getattr(media_info, 'artist', 'Unknown')}"
            title.value = f"{getattr(media_info, 'title', 'Unknown')}"
        else:
            artist.value = "Artist: Unknown"
            title.value = "Title: Unknown"

        playback_status.value = f"Status: {status}"

        # Check thumbnail for None
        if media_info is not None and getattr(media_info, 'thumbnail', None) is not None:
            buffered = io.BytesIO()
            media_info.thumbnail.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            thumbnail.src_base64 = f"{img_str}"
        else:
            thumbnail.src_base64 = ""

        # Check timeline_pbc and interpolated timeline for None
        interpolated_timeline = await pbc.get_interpolated_timeline_properties()
        if (
            interpolated_timeline is not None
            and timeline_pbc is not None
            and getattr(interpolated_timeline, "position", None) is not None
            and getattr(timeline_pbc, "end_time", None) is not None
            and timeline_pbc.end_time.total_seconds() > 0
        ):
            progress_bar.value = interpolated_timeline.position.total_seconds() / \
                timeline_pbc.end_time.total_seconds()
        else:
            progress_bar.value = 0

        page.update()

    async def periodic_update():
        while True:
            await update_media_info()
            await asyncio.sleep(0.5)  # Update every 0.05 seconds

    play_button = ft.Button(
        text="Play", on_click=lambda e: asyncio.run(play(e)), width=150, height=50)
    pause_button = ft.Button(
        text="Pause", on_click=lambda e: asyncio.run(pause(e)), width=150, height=50)
    stop_button = ft.Button(
        text="Stop", on_click=lambda e: asyncio.run(stop(e)), width=150, height=50)
    rewind_button = ft.Button(
        text="Rewind", on_click=lambda e: asyncio.run(rewind(e)), width=150, height=50)
    fast_forward_button = ft.Button(
        text="Fast Forward", on_click=lambda e: asyncio.run(fast_forward(e)), width=150, height=50)
    next_track_button = ft.Button(
        text="Next Track", on_click=lambda e: asyncio.run(next_track(e)), width=150, height=50)
    previous_track_button = ft.Button(
        text="Previous Track", on_click=lambda e: asyncio.run(previous_track(e)), width=150, height=50)
    toggle_play_pause_button = ft.Button(
        text="Toggle Play/Pause", on_click=lambda e: asyncio.run(toggle_play_pause(e)), width=150, height=50)

    artist = ft.Text(value="Artist: ", size=20)
    title = ft.Text(value="Title: ", size=20)
    playback_status = ft.Text(value="Status: ", size=20)
    thumbnail = ft.Image(src="", width=100, height=100)
    progress_bar = ft.ProgressBar(value=0, width=60000, height=50)

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            thumbnail,
                            title,
                            artist,
                            playback_status,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    alignment=ft.alignment.top_left,
                    padding=30,
                ),
                ft.Container(
                    content=progress_bar,
                    alignment=ft.alignment.top_center,
                    padding=30,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            # play_button,
                            # pause_button,
                            # stop_button,
                            # rewind_button,
                            # fast_forward_button,
                            previous_track_button,
                            next_track_button,
                            toggle_play_pause_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    alignment=ft.alignment.bottom_center,
                    padding=30,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    asyncio.create_task(periodic_update())

ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
