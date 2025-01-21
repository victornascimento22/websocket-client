import websocket
import json
import base64
import os
import time

class ImageDisplay:
    def __init__(self):
        self.image_dir = "images"
        self.transition_time = 15
        
        # Cria diretório de imagens se não existir
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        
        # Inicia o feh em modo slideshow
        self.start_feh()
        
    def start_feh(self):
        # Mata qualquer instância existente do feh
        os.system("pkill feh")
        # Inicia o feh em modo slideshow com ordem numérica
        cmd = f"feh -F -Z -D {self.transition_time} -R {self.transition_time} --sort filename {self.image_dir}/* &"
        os.system(cmd)
        print("🖼️ Feh iniciado em modo slideshow")
    
    def add_image(self, image_data, index):
        # Salva a imagem no diretório com padding de zeros para ordenação correta
        filename = os.path.join(self.image_dir, f"image_{index:03d}.png")
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))
        print(f"✨ Imagem salva: {filename}")
        
        # Força o feh a recarregar as imagens
        os.system("pkill -USR1 feh")

def on_message(ws, message):
    try:
        data = json.loads(message)
        image = data.get("image")
        index = data.get("index", 0)
        transition_time = data.get("transition_time", 15)
        
        if image:
            display.add_image(image, index)
            print(f"📥 Recebida imagem {index}")
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

def on_error(ws, error):
    print(f"❌ Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexão fechada, tentando reconectar...")
    time.sleep(5)  # Espera 5 segundos antes de reconectar
    connect_websocket()  # Tenta reconectar

def on_open(ws):
    print("🔗 Conexão WebSocket estabelecida")
    # Envia mensagem identificando este Raspberry Pi
    ip = os.popen("hostname -I | awk '{print $1}'").read().strip()
    ws.send(json.dumps({"type": "identify", "ip": ip}))

def connect_websocket():
    # Substitua pelo IP da sua API
    API_URL = "ws://sua-api:8080/ws/connect"
    
    ws = websocket.WebSocketApp(
        API_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    ws.run_forever()

if __name__ == "__main__":
    print("🚀 Iniciando cliente de display...")
    
    # Verifica e instala dependências
    os.system("which feh || sudo apt-get install -y feh")
    
    # Inicia o display manager
    display = ImageDisplay()
    
    # Conecta ao WebSocket e mantém conexão
    while True:
        try:
            connect_websocket()
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente