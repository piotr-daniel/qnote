from .app import QnoteApp
from .utils import init_db


def main():
    init_db()
    app = QnoteApp()
    app.run()
