from flask import Flask

class Wishlister():
    def __init__(self, *args, **kwargs):
        pass

    def add_game(self, game_id):
        pass

    def remove_game(self, game_id):
        pass

    def insert_game(self, *args, **kwargs):
        pass

    def swap_games(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass
    
    def shuffle(self, *args, **kwargs):
        pass

    def display_games(self, *args, **kwargs):
        pass

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
