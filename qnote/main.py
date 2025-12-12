from qnote.app import QnoteApp
from qnote.utils import init_db


def main():
    init_db()
    app = QnoteApp()
    app.run()
