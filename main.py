from todpole.events import *


print("Running on http://127.0.0.1:8282/ (Press CTRL+C to quit)")
WSGIServer(("127.0.0.1", 8282), app,
            handler_class=WebSocketHandler).serve_forever()