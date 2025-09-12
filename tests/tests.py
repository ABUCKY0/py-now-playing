import unittest
# import asynctest
from unittest.mock import MagicMock, patch
from py_now_playing import MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode, PlaybackInfo, MediaTimeline, PyNowPlaying, MediaInfo
import logging
import time 
# import flet as ft
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    PlaybackInfoChangedEventArgs,
    TimelinePropertiesChangedEventArgs,
    MediaPropertiesChangedEventArgs,
    GlobalSystemMediaTransportControlsSession
)

from datetime import datetime, timedelta
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
import asyncio


GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
GRAY = "\033[90m"

async def main_test():
  print("Ensure Media App is open and playing media for this test to work.")
  input("Press Enter to continue...")
  # np = PyNowPlaying(aumid="music.amazon.com-6BE721EE_pwn81ww419gp8!App") # Amazon Music Edge App
  # np = PyNowPlaying(aumid=(await PyNowPlaying.get_all_aumids_by_name("Media Player"))[0]) # Windows Media Player
  # np = PyNowPlaying(aumid="AmazonMobileLLC.AmazonMusic_kc6t79cpj4tp0!AmazonMobileLLC.AmazonMusic") # Amazon Music UWP App
  # np = PyNowPlaying(aumid="SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify") # Spotify UWP App

  # await np.initalize_mediamanager()
  np = await PyNowPlaying.create(aumid="music.amazon.com-6BE721EE_pwn81ww419gp8!App") # Amazon Music Edge App
  media_info: MediaInfo = await np.get_media_info()
  media_timeline: MediaTimeline = await np.get_timeline_properties()
  media_playback: PlaybackInfo = await np.get_playback_info()

  print("----------------------------------Media Info----------------------------------")
  print(f"Title: {media_info.title}")
  print(f"Artist: {media_info.artist}")
  print(f"Album: {media_info.album_title}")
  print(f"Album Artist: {media_info.album_artist}")
  print(f"Album Track Count: {media_info.album_track_count}")
  print(f"Track Number: {media_info.track_number}")
  print(f"Genres: {media_info.genres}")
  print(f"Playback Type: {media_info.playback_type}")
  print(f"Thumbnail: {media_info.thumbnail}")
  print("---------------------------------------------------------------------------")
  print("----------------------------------Media Timeline----------------------------------")
  print(f"Start Time: {media_timeline.start_time}")
  print(f"End Time: {media_timeline.end_time}")
  print(f"Max Seek Time: {media_timeline.max_seek_time}")
  print(f"Position: {media_timeline.position}")
  print(f"Min Seek Time: {media_timeline.min_seek_time}")
  print(f"Last Updated Time: {media_timeline.last_updated_time}")
  print("---------------------------------------------------------------------------")
  print("----------------------------------Media Playback----------------------------------")
  print(f"Playback Type: {media_playback.playback_type}")
  print(f"Playback Status: {media_playback.playback_status}")
  print(f"Playback Rate: {media_playback.playback_rate}")
  print(f"Auto Repeat Mode: {media_playback.auto_repeat_mode}")
  print(f"Is Shuffle Active: {media_playback.is_shuffle_active}")
  print("---------------------------------------------------------------------------")
  print("----------------------------------Enabled Controls----------------------------------")
  print(f"Channel Down: {media_playback.controls.channel_down}")
  print(f"Channel Up: {media_playback.controls.channel_up}")
  print(f"Fast Forward: {media_playback.controls.fast_forward}")
  print(f"Next Track: {media_playback.controls.next_track}")
  print(f"Pause: {media_playback.controls.pause} {GRAY}(This depends on the current playback status, i.e. if it's paused you can't pause it){RESET}")
  print(f"Playback Position (Seek): {media_playback.controls.playback_position}")
  print(f"Playback Rate: {media_playback.controls.playback_rate}")
  print(f"Play: {media_playback.controls.play} {GRAY}(This depends on the current playback status, i.e. if it's playing you can't play it){RESET}")
  print(f"Toggle Play/Pause: {media_playback.controls.toggle_play_pause}")
  print(f"Previous Track: {media_playback.controls.previous_track}")
  print(f"Record: {media_playback.controls.record}")
  print(f"Repeat: {media_playback.controls.repeat}")
  print(f"Rewind: {media_playback.controls.rewind}")
  print(f"Shuffle: {media_playback.controls.shuffle}")
  print(f"Stop: {media_playback.controls.stop}")
  print("---------------------------------------------------------------------------")

  total_tests = 9
  success_count = 0
  skipped_count = 0
  failure_count = 0
  try:
    # Test all of the different functions
    print("Pausing media...", end=" ", flush=True)
    await np.play()  # Ensure playback is started before pausing
    time.sleep(1)  # Wait for the play to take effect
    media_playback = await np.get_playback_info()
    if media_playback.controls.pause is True:
      await np.pause()
      time.sleep(1)  # Wait for the pause to take effect
      playback_info = await np.get_playback_info()
      assert playback_info.playback_status == MediaPlaybackStatus.PAUSED, f"{RED}FAIL. Media playback status should be PAUSED{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping pause test because media is already paused or pause control is not available{RESET}")
      skipped_count += 1


    print("Resuming media...", end=" ", flush=True)
    media_playback = await np.get_playback_info()
    if media_playback.controls.play is True:
      await np.play()
      time.sleep(1)  # Wait for the play to take effect
      assert (await np.get_playback_info()).playback_status == MediaPlaybackStatus.PLAYING, f"{RED}FAIL. Media playback status should be PLAYING{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping play test because media is already playing or play control is not available{RESET}")
      skipped_count += 1


    print("Toggling playback...", end=" ", flush=True)
    media_playback = await np.get_playback_info()
    if media_playback.controls.toggle_play_pause is True:
      current_status = (await np.get_playback_info()).playback_status
      await np.toggle_play_pause()
      time.sleep(1)  # Wait for the toggle to take effect
      playback_info = await np.get_playback_info()
      if current_status == MediaPlaybackStatus.PLAYING:
          assert playback_info.playback_status == MediaPlaybackStatus.PAUSED, f"{RED}FAIL. Media playback status should be PAUSED after toggle{RESET}"
      else:
          assert playback_info.playback_status == MediaPlaybackStatus.PLAYING, f"{RED}FAIL. Media playback status should be PLAYING after toggle{RESET}"
      print(f"{GREEN}Success{RESET}")
      await np.play()  # Ensure playback is resumed after toggle
      time.sleep(1)  # Wait for the play to take effect
      success_count += 1
    else:
      print(f"{GRAY}Skipping toggle play/pause test because toggle control is not available{RESET}")
      skipped_count += 1
    

    current_pos = 0
    print("Seeking media to 10 seconds...", end=" ", flush=True)
    if (await np.get_playback_info()).controls.playback_position is True:
      current_pos = (await np.get_timeline_properties()).position.seconds
      res = await np.seek(10)
      assert res is True, f"{RED}FAIL. Seek operation should return True{RESET}"
      time.sleep(1)  # Wait for the seek to take effect
      timeline = await np.get_timeline_properties()
      assert timeline.position.seconds >= 10, f"{RED}FAIL. Media position should be 10 seconds after seeking{RESET}"
      print(f"{GREEN}Success{RESET}")
      await np.seek(100)
      success_count += 1
    else:
      print(f"{GRAY}Skipping seek test because playback position control is not available{RESET}")
      skipped_count += 1




    print("Skipping to next track...", end=" ", flush=True)
    if (await np.get_playback_info()).controls.next_track is True:
      current_song_name = (await np.get_media_info()).title
      await np.next_track()
      time.sleep(2)  # Wait for the next track to take effect
      playback_info = await np.get_playback_info()
      new_song_name = (await np.get_media_info()).title
      assert current_song_name != new_song_name, f"{RED}FAIL. Media should have changed to the next track{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping next track test because next track control is not available{RESET}")
      skipped_count += 1




    if (await np.get_playback_info()).controls.previous_track is True:
      print("Giving 5 seconds to allow the next track to play...", end=" ", flush=True)
      time.sleep(5)
      print(f"{GRAY}Done{RESET}")

      print("Skipping to previous track...", end=" ", flush=True)
      current_song_name = (await np.get_media_info()).title
      await np.previous_track()
      await np.previous_track()  # Call twice to ensure it goes back to the original track because Amazon Music skips back to the beginning of the current track if called once
      # Loop until the previous track is actually played (check name)
      loop_escape_count = 10 # 10 seconds
      while loop_escape_count > 0 and (await np.get_media_info()).title == current_song_name:
        time.sleep(1)
        loop_escape_count -= 1
      if loop_escape_count <= 0:
        print(f"{RED}FAIL. Previous track did not change after 10 seconds{RESET}")
        failure_count += 1
        raise Exception("Previous track did not change after 10 seconds")
      playback_info = await np.get_playback_info()
      new_song_name = (await np.get_media_info()).title
      assert current_song_name != new_song_name, f"{RED}FAIL. Media should have changed back to the previous track{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping previous track test because previous track control is not available{RESET}")
      skipped_count += 1





    print("Setting Repeat mode...", end=" ", flush=True)
    if (await np.get_playback_info()).controls.repeat is True:
      await np.change_auto_repeat_mode(MediaPlaybackAutoRepeatMode.TRACK)
      time.sleep(1)  # Wait for the repeat mode to take effect
      playback_info = await np.get_playback_info()
      assert playback_info.auto_repeat_mode == MediaPlaybackAutoRepeatMode.TRACK, f"{RED}FAIL. Media auto repeat mode should be TRACK{RESET}"
      print(f"{GREEN}Success{RESET}")
      await np.change_auto_repeat_mode(MediaPlaybackAutoRepeatMode.NONE)  # Reset to NONE for next tests
      success_count += 1
    else:
      print(f"{GRAY}Skipping repeat mode test because repeat control is not available{RESET}")
      skipped_count += 1





    print("Rewinding media...", end=" ", flush=True)
    if (await np.get_playback_info()).controls.rewind is True:
      await np.seek(100)
      time.sleep(1)  # Wait for the seek to take effect
      current_time = (await np.get_timeline_properties()).position.seconds
      await np.rewind()
      time.sleep(1)  # Wait for the rewind to take effect
      new_time = (await np.get_timeline_properties()).position.seconds
      timeline = await np.get_timeline_properties()
      assert new_time < current_time, f"{RED}FAIL. Media position should be less than {current_time} seconds after rewinding{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping rewind test because rewind control is not available{RESET}")
      skipped_count += 1

      

    print("Fast forwarding media...", end=" ", flush=True)
    if (await np.get_playback_info()).controls.fast_forward is True: 
      await np.seek(10)
      time.sleep(1)  # Wait for the seek to take effect
      current_time = (await np.get_timeline_properties()).position.seconds
      await np.fast_forward()
      time.sleep(1)  # Wait for the fast forward to take effect
      new_time = (await np.get_timeline_properties()).position.seconds
      timeline = await np.get_timeline_properties()
      assert new_time > current_time, f"{RED}FAIL. Media position should be greater than {current_time} seconds after fast forwarding{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
    else:
      print(f"{GRAY}Skipping fast forward test because fast forward control is not available{RESET}")
      skipped_count += 1
    
    try:
      # Making sure the class throws an error if we try to instantiate it directly
      print("Testing direct instantiation...", end=" ", flush=True)
      PyNowPlaying(aumid="music.amazon.com-6BE721EE_pwn81ww419gp8!App")
      print(f"{RED}FAIL. Direct instantiation should raise an error{RESET}")
      failure_count += 1
    except RuntimeError as e:
      assert str(
          e) == "Direct instantiation of PyNowPlaying is prohibited because async initialization is required. Use PyNowPlaying.create() to instantiate this class.", f"{RED}FAIL. Expected RuntimeError with specific message{RESET}"
      print(f"{GREEN}Success{RESET}")
      success_count += 1
  except Exception as e:
    print(f"{RED}An error occurred during the tests: {e}{RESET}")
    failure_count = 1
  finally:
    print("\n----------------------------------Test Summary----------------------------------")
    print(f"Total Tests: {total_tests}")
    print(f"Successes: {success_count}")
    print(f"Skipped due to unavailability: {skipped_count}")
    print(f"Failures: {failure_count}")
    print("---------------------------------------------------------------------------")
 
 
if __name__ == '__main__':
  asyncio.run(main_test())

