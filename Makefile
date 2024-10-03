.PHONY: chat-gourmet
chat-gourmet:
	docker compose up --build

.PHONY: chat-gourmet-server
chat-gourmet-server:
	docker compose up --build core qdrant

.PHONY: qdrant
qdrant:
	docker run -p 6333:6333 -v $(PWD)/qdrant_storage:/qdrant/storage --ulimit nofile=10000:10000 qdrant/qdrant:v1.11.3