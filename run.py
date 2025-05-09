from quiz_app import create_app
from quiz_app.config import Config

app = create_app()
Config.validate_config()

if __name__ == '__main__':
    app.run(debug=True)