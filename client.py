import asyncio
import websockets
import json
import base64
import logging
import pygame
import io
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisplayManager:
    def __init__(self, loop):  # Recebe o loop como parâmetro
        pygame.init()
        
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        
        self.screen = pygame.display.set_mode((self.width, self.height), 
                                            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        logger.info(f"🖥️ Display configurado: {self.width}x{self.height}")
        self.current_image = None
        self.loop = loop  # Guarda referência do loop
        
        # Inicia loop de display
        self.loop.create_task(self.display_loop())

    # ... resto dos métodos igual ...

async def main():
    loop = asyncio.get_event_loop()
    display = DisplayManager(loop)  # Passa o loop para o DisplayManager
    
    ip = "0.0.0.0"
    port = 8081
    
    logger.info(f"🚀 Iniciando servidor WebSocket em ws://{ip}:{port}")
    async with websockets.serve(
        handle_connection, 
        ip, 
        port,
        max_size=None,
        max_queue=None
    ):
        logger.info("🎯 Servidor WebSocket rodando")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pygame.quit()
        logger.info("👋 Servidor finalizado")