import websocket
import json
import base64
import os
import threading
import time
from collections import deque

class ImageDisplay:
    def __init__(self):
        self.image_dir = "images"  # Diretório para salvar as imagens
        self.images = deque()
        self.transition_time = 15
        self.running = True
        
        # Cria diretório de imagens se não existir
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        
        # Inicia o feh em modo slideshow
        self.start_feh()
        
    def start_feh(self):
        # Mata qualquer instância existente do feh
        os.system("pkill feh")
        # Inicia o feh em modo slideshow
        cmd = f"feh -F -Z -D {self.transition_time} -R {self.transition_time} {self.image_dir}/* &"
        os.system(cmd)
        print("🖼️ Feh iniciado em modo slideshow")
    
    def add_image(self, image_data, index):
        # Salva a imagem no diretório
        filename = os.path.join(self.image_dir, f"image_{index:03d}.png")
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))
        print(f"✨ Imagem salva: {filename}")
        
        # Força o feh a recarregar as imagens
        os.system("pkill -USR1 feh")

display = ImageDisplay()

def on_message(ws, message):
    try:
        data = json.loads(message)
        image = data.get("image")
        index = data.get("index", 0)
        transition_time = data.get("transition_time", 15)
        
        if image:
            display.transition_time = transition_time
            display.add_image(image, index)
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

def on_error(ws, error):
    print(f"❌ Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexão fechada")

def on_open(ws):
    print("🔗 Conexão estabelecida")

def connect_websocket():
    # Substitua pelo IP da sua API
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://sua-api:8080/ws/connect",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close,
                              on_open=on_open)
    
    ws.run_forever()

if __name__ == "__main__":
    print("🚀 Iniciando cliente de display...")
    
    # Instala dependências necessárias se não existirem
    os.system("which feh || sudo apt-get install -y feh")
    
    while True:
        try:
            connect_websocket()
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            time.sleep(5)