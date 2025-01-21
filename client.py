import asyncio
import websockets
import json
import base64
import os
import logging
from websockets.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_connection(websocket: WebSocketServerProtocol):
    logger.info("🔗 Nova conexão recebida")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"📥 Mensagem recebida: {data}")
                # Processa a mensagem aqui
            except Exception as e:
                logger.error(f"❌ Erro ao processar mensagem: {e}")
    except Exception as e:
        logger.error(f"❌ Erro na conexão: {e}")

async def main():
    ip = "0.0.0.0"  # Aceita conexões de qualquer IP
    port = 8081
    
    logger.info(f"🚀 Iniciando servidor WebSocket em ws://{ip}:{port}")
    async with websockets.serve(handle_connection, ip, port):
        logger.info("🎯 Servidor WebSocket rodando")
        await asyncio.Future()  # Roda indefinidamente

if __name__ == "__main__":
    asyncio.run(main())