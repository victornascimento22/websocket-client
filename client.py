import asyncio
import websockets
import json
import base64
import os
import logging
from websockets.server import serve

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageDisplay:
    def __init__(self):
        self.image_dir = "images"
        self.transition_time = 15
        
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        
        self.start_feh()
        
    def start_feh(self):
        os.system("pkill feh")
        cmd = f"feh -F -Z -D {self.transition_time} -R {self.transition_time} --sort filename {self.image_dir}/* &"
        os.system(cmd)
        logger.info("🖼️ Feh iniciado em modo slideshow")
    
    def add_image(self, image_data, index):
        filename = os.path.join(self.image_dir, f"image_{index:03d}.png")
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))
        logger.info(f"✨ Imagem salva: {filename}")
        os.system("pkill -USR1 feh")

display = ImageDisplay()

async def handle_websocket(websocket):
    logger.info("🔗 Nova conexão WebSocket estabelecida")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                image = data.get("image")
                index = data.get("index", 0)
                
                if image:
                    display.add_image(image, index)
                    logger.info(f"📥 Recebida imagem {index}")
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ Erro ao decodificar mensagem: {e}")
            except Exception as e:
                logger.error(f"❌ Erro ao processar mensagem: {e}")
    except websockets.exceptions.ConnectionClosed:
        logger.info("🔌 Conexão fechada")
    except Exception as e:
        logger.error(f"❌ Erro na conexão: {e}")

async def main():
    ip = os.popen("hostname -I | awk '{print $1}'").read().strip()
    port = 8081

    logger.info(f"🚀 Iniciando servidor WebSocket em ws://{ip}:{port}")
    
    async with serve(handle_websocket, ip, port):
        logger.info(f"🎯 Servidor WebSocket rodando em ws://{ip}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Servidor finalizado pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")