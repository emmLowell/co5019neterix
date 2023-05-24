from config import ConfigManager, RedisConfig
from functools import wraps
import threading
import redis
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main


class RedisManager:
    config_manager: 'ConfigManager' = ConfigManager()
    redis_config = config_manager.read_config(RedisConfig)
    redis_connection = redis.Redis.from_url(redis_config.url)
    listening_thread: threading.Thread = None
    
    CHANNEL_PREFIX = b"scanner_tunnel:"
    CORE_CHANNEL = CHANNEL_PREFIX + b"core"
    
    @staticmethod
    def is_connected():
        try:
            RedisManager.redis_connection.ping()
            return True
        except redis.exceptions.ConnectionError:
            return False
    
    @staticmethod
    def require_connection(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if(RedisManager.is_connected()):
                func(*args, **kwargs)
            else:
                print("Redis is not connected")
        return wrapper
    
    @staticmethod
    def receive_message(message):
        print(message)
        
    @staticmethod
    def callback_handler(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            try:
                if(isinstance(data, dict) and "data" in data):
                    print(data)
                    raw_data = data["data"]
                    string_data = raw_data.decode("utf-8")
                    data = string_data.split(" ")
                    return func(*data, *args, **kwargs)
                print(f"{data} {type(data)} is dict: ", data is dict)
                return func(data, *args, **kwargs)
            except Exception as e:
                print(data, e)
        return wrapper
    
    @staticmethod
    @require_connection
    def listen(main: 'Main'):
        pubsub = RedisManager.redis_connection.pubsub()
        subs = {
            RedisManager.CHANNEL_PREFIX + b"core": RedisManager.receive_message,
            RedisManager.CHANNEL_PREFIX + b"schedule": RedisManager.callback_handler(main.polling.start_polling_id),
            RedisManager.CHANNEL_PREFIX + b"stop_scheduler": RedisManager.callback_handler(main.polling.stop_polling),
            RedisManager.CHANNEL_PREFIX + b"scan": RedisManager.callback_handler(main.polling.start_polling_id_once)
            }
        pubsub.subscribe(subs.keys())
        pubsub.channels.update(subs)
        pubsub.execute_command(f"SUBSCRIBE" ,*subs.keys())

        pubsub.run_in_thread(sleep_time=0.001, daemon=True)
    
    
    @staticmethod
    @require_connection
    def send(channel: str = None, message: str = None):
        if(channel is None):
            channel = RedisManager.CORE_CHANNEL
        if(message is None): return print("No message to send")
        RedisManager.redis_connection.publish(channel, message)
        
    @staticmethod
    @require_connection
    def schedule(schedule_id: int):
        RedisManager.send(channel=RedisManager.CHANNEL_PREFIX + b"schedule", message=f"{schedule_id}")
        
    @staticmethod
    @require_connection
    def stop_scheduler(scheduler_id: int):
        RedisManager.send(channel=RedisManager.CHANNEL_PREFIX + b"stop_scheduler", message=f"{scheduler_id}")
        
    @staticmethod
    @require_connection
    def scan(ip: str, scan_type: str, port_type: str):
        RedisManager.send(channel=RedisManager.CHANNEL_PREFIX + b"scan", message=f"{ip} {scan_type} {port_type}")
        
        