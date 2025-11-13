#!/usr/bin/env python
"""Script para executar a aplicação FastAPI."""
import uvicorn
import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
