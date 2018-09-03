from todpole import events


print("Running on http://127.0.0.1:8282/ (Press CTRL+C to quit)")
events.WSGIServer(("127.0.0.1", 8282), app,
            handler_class=WebSocketHandler).serve_forever()