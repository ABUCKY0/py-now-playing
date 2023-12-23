import sys
sys.path.append('.')
sys.path.append('..')
import py_now_playing
import asyncio
from pypresence import Presence
import pypresence.exceptions
from pypresence.exceptions import InvalidID
import time
import multiprocessing
import logging
import os
import sys
import traceback

# Set up logging
#logging.basicConfig(level=logging.NOTSET)
logging.basicConfig(level=logging.INFO)
# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO)

# Disable logging to consile with sys
#sys.stdout = open(os.devnull, 'w')
#sys.stderr = open(os.devnull, 'w')
logger = logging.getLogger(__name__)

def start_rpc(client_id, now_playing_queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    rpc = Presence(client_id)

    def connect_rpc():
        while True:
            try:
                logger.info("try to connect")
                rpc.connect()
                logger.info("Connected to Discord RPC")
                break
            except Exception as e:
                logger.error(f"Failed to connect to Discord RPC: {e}")
                traceback.print_exc()
                time.sleep(15)

    # Call connect_rpc directly
    connect_rpc()

    while True:
        try:
            now_playing_list = now_playing_queue.get()
            logger.info(now_playing_list)
            if now_playing_list:
                rpc.update(
                    details=now_playing_list['title'] or "Unknown Song", 
                    state='by ' + now_playing_list['artist'] if now_playing_list['artist'] is not None else 'by Unknown Artist',
                    large_image='https://pro2-bar-s3-cdn-cf4.myportfolio.com/42020405547ae2dc93d34e8df7965fc4/5d5b55e2-c1b4-46cb-a027-6a21bee9de3f_rw_1920.gif?h=85babbd0e5d4aa7c618295a359c1811f',  # Replace with your image key
                    large_text='Amazon Music',
                )
            else:
                logger.info("No Music Playing")
                rpc.clear()
        except (pypresence.exceptions.DiscordNotFound, pypresence.exceptions.InvalidPipe, pypresence.PipeClosed) as e:
            connect_rpc()
        except BrokenPipeError or EOFError as f:
            logger.error(f"BrokenPipeError: {f}")
            traceback.print_exc()
        except EOFError or UnboundLocalError as g:
            logger.error(f"EOFError: {g}")
            traceback.print_exc()

        time.sleep(5)


async def main():
    np = py_now_playing.NowPlaying()
    await np.initalize_mediamanger()

    client_id = '1187213553673965619'  # Replace with your client ID
    manager = multiprocessing.Manager()
    now_playing_queue = manager.Queue()

    # Start the Discord RPC in a separate process
    rpc_process = multiprocessing.Process(target=start_rpc, args=(client_id, now_playing_queue))
    rpc_process.start()

    try:
        while True:
            now_playing = await np.get_active_app_user_model_ids()
            now_playing = list(filter(lambda app: app['Name'] == 'Amazon Music', now_playing))

            if not now_playing:
                now_playing_queue.put(None)
                await asyncio.sleep(5)
                continue

            now_playing_appid = now_playing[0]['AppID']
            try:
                data = await np.get_now_playing(now_playing_appid)
            except PermissionError as permerr:
                logger.error("PermissionError: ")
                traceback.print_exc()
                data = None
                pass
            now_playing_queue.put(data)
            logger.info("A Song is Playing, Here is the Json for that: " + str(data))
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        logger.info("Interrupted by user, stopping processes...")
        rpc_process.terminate()  # Terminate the rpc_process
        # Kill the event loop
        asyncio.get_event_loop().stop()
    except OSError as e:
        logger.error(f"OSError {e}")
        
        traceback.print_exc()
        now_playing_queue.put(None)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        traceback.print_exc()
        pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user, caught in if, exiting...")
        sys.exit(0)