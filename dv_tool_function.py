import json
import os

import redis


# import load_command


def redis_client() -> redis.Redis:
    """Returns redis client"""
    return redis.Redis(
        host=os.environ["REDIS_DV_URL"],
        port=16704,
        username=os.environ["REDIS_USER"],
        password=os.environ["REDIS_DV_PASSWD"],
        decode_responses=True,
    )


def read_db_json(filename) -> dict:
    """Reads json value from redis (key: filename, value: data)"""
    client = redis_client()
    return client.json().get(filename)


def read_file_json(filename) -> dict:
    """Returns dictionary from a json file"""
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def write_db_json(filename: str, data: dict) -> None:
    """Writes dictionary to redis json (key: filename, value: data)"""
    redis_client().json().set(filename, ".", data)
    # return False if args is type(None)


def write_file_json(filename: str, data: dict) -> None:
    """Writes dictionary to json file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def check_dict_data(data: dict, arg) -> bool:
    """Check if arg is in data"""
    try:
        print(f"data in {arg} is {data[arg]}")
    except KeyError:
        return False
    else:
        return True


def check_db_file(filename) -> bool:
    """Check if filename exist in redis key"""
    return bool(redis_client().exists(filename))


def new_check_file(filename) -> bool:
    """Check if filename exist in file"""
    return os.path.isfile(filename)


"""
def lang_command(lang: str, command: str) -> str:
    try:
        command_out = load_command.read_description(lang, command)
    except FileNotFoundError:
        command_out = load_command.read_description("en", command)
    finally:
        return command_out
"""


def get_id(self) -> str:
    """Return the id of the user or guild (user id start with `user_`)"""
    try:
        server_id = str(self.guild.id)
    except Exception:
        server_id = f"user_{str(self.author.id)}"
    return server_id


def check_guild_or_dm(self) -> bool:
    """Return if this is a guild or a DM"""
    try:
        _ = str(self.guild.id)
    except Exception:
        _ = f"user_{str(self.author.id)}"
        return False
    else:
        return True


def check_platform(
    user_platform_set: bool,
    user_id: [str, int],
    guild_platform_set: bool,
    guild_id: [str, int],
    lang: str,
) -> str:
    """Return the platform of the user or guild (default: Google)"""
    if (
        lang in read_file_json("languages.json")["Support_Language"]
        and lang not in read_file_json("azure_languages.json")["Support_Language"]
    ):
        return "Google"
    if (
        lang in read_file_json("azure_languages.json")["Support_Language"]
        and lang not in read_file_json("languages.json")["Support_Language"]
    ):
        return "Azure"
    user_id = f"user_{str(user_id)}"
    if (
        user_platform_set
        and read_db_json("user_config")[user_id]["platform"] == "Google"
    ):
        print("Init Google TTS API 1")
        return "Google"

    elif (
        user_platform_set
        and read_db_json("user_config")[user_id]["platform"] == "Azure"
    ):
        print("Init Azure TTS API 1")
        return "Azure"
    elif guild_platform_set and read_db_json(f"{guild_id}")["platform"] == "Google":
        print("Init Google TTS API 2")
        return "Google"
    elif guild_platform_set and read_db_json(f"{guild_id}")["platform"] == "Azure":
        print("Init Azure TTS API 2")
        return "Azure"
    elif not user_platform_set and not guild_platform_set:
        print("Init Google TTS API 3")
        return "Google"
    else:
        print(
            f"You found a bug\n"
            f"User platform: {user_platform_set}\n"
            f"User id: {user_id}\n"
            f"Guild platform: {guild_platform_set}\n"
            f"Guild id: {guild_id}\n"
        )
        return "Something wrong"


def del_json(filename) -> None:
    """Delete json value from redis (key: filename)"""
    redis_client().delete(filename)
