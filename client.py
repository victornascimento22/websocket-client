# ... imports anteriores ...

class DisplayManager:
    # ... código anterior ...

async def handle_connection(websocket):
    logger.info("🔗 Nova conexão recebida")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if "image" in data:
                    display.update_image(data["image"])
                # Envia pong para manter conexão viva
                await websocket.pong()
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
    
    while True:  # Loop de reconexão
        try:
            logger.info(f"🚀 Iniciando servidor WebSocket em ws://{ip}:{port}")
            async with websockets.serve(
                handle_connection, 
                ip, 
                port,
                max_size=None,
                max_queue=None,
                ping_interval=20,    # Envia ping a cada 20 segundos
                ping_timeout=60,     # Timeout de 60 segundos para pong
                close_timeout=10     # Timeout de 10 segundos para fechar conexão
            ) as server:
                logger.info("🎯 Servidor WebSocket rodando")
                await asyncio.Future()
        except Exception as e:
            logger.error(f"❌ Erro no servidor: {e}")
            await asyncio.sleep(5)  # Espera 5 segundos antes de tentar reconectar
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pygame.quit()
        logger.info("👋 Servidor finalizado")