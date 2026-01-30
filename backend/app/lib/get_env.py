# from dotenv import load_dotenv
import os

# load_dotenv()


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        raise EnvironmentError(f"Gagal memuat variabel lingkungan wajib: {name}")
