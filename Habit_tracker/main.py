from tracker_ui import launch_app
from database import init_db

if __name__ == "__main__":
    init_db()
    launch_app()
