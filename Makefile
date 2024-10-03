.PHONY: chat-gourmet
chat-gourmet:
	docker compose up --build

.PHONY: chat-gourmet-server
chat-gourmet-server:
	docker compose up --build core qdrant