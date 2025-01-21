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
    def __init__(self, loop):
        pygame.init()
        
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        
        self.screen = pygame.display.set_mode((self.width, self.height), 
                                            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        logger.info(f"🖥️ Display configurado: {self.width}x{self.height}")
        self.current_image = None
        self.loop = loop
        
        # Inicia loop de display
        self.loop.create_task(self.display_loop())
    
    def update_image(self, image_data):
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Mantém proporção
            display_ratio = self.width / self.height
            image_ratio = image.width / image.height
            
            if image_ratio > display_ratio:
                new_width = self.width
                new_height = int(self.width / image_ratio)
            else:
                new_height = self.height
                new_width = int(self.height * image_ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            pos_x = (self.width - new_width) // 2
            pos_y = (self.height - new_height) // 2
            
            image_data = image.tobytes()
            self.current_image = {
                'surface': pygame.image.fromstring(image_data, (new_width, new_height), 'RGB'),
                'position': (pos_x, pos_y)
            }
            
            logger.info(f"✨ Nova imagem carregada: {new_width}x{new_height}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar imagem: {e}")

    async def display_loop(self):  # Método que faltava
        clock = pygame.time.Clock()
        
        while True:
            if self.current_image:
                self.screen.fill((0, 0, 0))
                self.screen.blit(
                    self.current_image['surface'], 
                    self.current_image['position']
                )
                pygame.display.flip()
            
            clock.tick(60)
            await asyncio.sleep(0.016)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and 
                    event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    return

async def handle_connection(websocket):
    logger.info("🔗 Nova conexão recebida")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if "image" in data:
                    display.update_image(data["image"])
            except Exception as e:
                logger.error(f"❌ Erro ao processar mensagem: {e}")
    except Exception as e:
        logger.error(f"❌ Erro na conexão: {e}")

async def main():
    loop = asyncio.get_event_loop()
    global display
    display = DisplayManager(loop)
    
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