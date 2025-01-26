from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 3000))
    debug = os.environ.get("FLASK_DEBUG", True)
    app.run(host=host, port=port, debug=debug)
