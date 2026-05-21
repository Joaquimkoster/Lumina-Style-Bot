import os
import time
from pathlib import Path
import flet as ft

try:
    from src.chatbot import ChatSession, processar_mensagem_total
except ImportError:
    class ChatSession:
        pass

    def processar_mensagem_total(texto, key, session=None):
        time.sleep(1.5)  
        return f"Resposta simulada para: {texto}"

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_ENV = RAIZ_PROJETO / ".env"
ARQUIVO_KEY_ANTIGO = RAIZ_PROJETO / "chave_groq.txt"
NOME_VARIAVEL_KEY = "GROQ_API_KEY"

def carregar_chave_local():
    chave_ambiente = os.getenv(NOME_VARIAVEL_KEY)
    if chave_ambiente:
        return chave_ambiente.strip()

    if ARQUIVO_ENV.exists():
        with open(ARQUIVO_ENV, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha.startswith(f"{NOME_VARIAVEL_KEY}="):
                    return linha.split("=", 1)[1].strip().strip('"').strip("'")

    if ARQUIVO_KEY_ANTIGO.exists():
        with open(ARQUIVO_KEY_ANTIGO, "r", encoding="utf-8") as f:
            return f.read().strip()

    return "SUA_CHAVE_AQUI"

def salvar_chave_local(chave):
    chave = chave.strip()
    if not chave:
        if ARQUIVO_ENV.exists(): ARQUIVO_ENV.unlink()
        if ARQUIVO_KEY_ANTIGO.exists(): ARQUIVO_KEY_ANTIGO.unlink()
        os.environ.pop(NOME_VARIAVEL_KEY, None)
        return

    with open(ARQUIVO_ENV, "w", encoding="utf-8") as f:
        f.write(f"{NOME_VARIAVEL_KEY}={chave}\n")
    
    if ARQUIVO_KEY_ANTIGO.exists(): ARQUIVO_KEY_ANTIGO.unlink()
    os.environ[NOME_VARIAVEL_KEY] = chave

def main(page: ft.Page):
    page.title = "Lumina Style Bot"
    page.theme_mode = "light"
    page.padding = ft.Padding(left=20, top=20, right=8, bottom=20)
    page.window_width = 500
    page.window_height = 700

    chave_inicial = carregar_chave_local()
    api_key_container = {"key": chave_inicial}
    chat_session = ChatSession()

    chat = ft.Column(expand=True, scroll="adaptive", spacing=10)
    
    indicador_digitando = ft.Row(
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.ProgressRing(width=14, height=14, stroke_width=2),
                        ft.Text("Lumina está pensando...", italic=True, size=12, color="gray"),
                    ],
                    spacing=8,
                ),
                bgcolor="#eeeeee",
                padding=10,
                border_radius=15,
            )
        ],
        alignment="start",
        visible=False
    )

    def processar_resposta(texto, api_key):
        try:
            resposta = processar_mensagem_total(texto, api_key, chat_session)
        except Exception as err:
            resposta = f"Erro técnico: {err}"

        indicador_digitando.visible = False
        nova_msg.disabled = False
        botao_enviar.disabled = False
        if indicador_digitando in chat.controls:
            chat.controls.remove(indicador_digitando)
        chat.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(resposta, color="black"),
                    bgcolor="#eeeeee",
                    padding=10,
                    border_radius=15,
                    width=350
                )
            ], alignment="start")
        )
        page.update()

    def enviar_mensagem(e):
        texto = nova_msg.value.strip()
        if not texto:
            return
        
        if api_key_container["key"] in ["SUA_CHAVE_AQUI", ""]:
            chat.controls.append(ft.Text("⚠️ Configure a API Key no botão acima!", color="red"))
            page.update()
            return

        chat.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(texto, color="white"),
                    bgcolor="blue",
                    padding=10,
                    border_radius=15,
                ),
                ft.Container(width=22),
            ], alignment="end")
        )
        
        nova_msg.value = ""
        nova_msg.disabled = True
        botao_enviar.disabled = True
        indicador_digitando.visible = True
        if indicador_digitando not in chat.controls:
            chat.controls.append(indicador_digitando)
        page.update()

        page.run_thread(processar_resposta, texto, api_key_container["key"])

    nova_msg = ft.TextField(
        label="Digite sua mensagem...", 
        expand=True,
        on_submit=enviar_mensagem,
        border_radius=25
    )

    api_input = ft.TextField(
        label="API Key da Groq", 
        password=True, 
        can_reveal_password=True,
        value=api_key_container["key"] if api_key_container["key"] != "SUA_CHAVE_AQUI" else ""
    )

    botao_enviar = ft.FloatingActionButton(icon=ft.Icons.SEND, on_click=enviar_mensagem, bgcolor="blue")

    def salvar_chave(e):
        chave = api_input.value.strip()
        salvar_chave_local(chave)
        api_key_container["key"] = chave or "SUA_CHAVE_AQUI"
        dialogo_config.open = False
        page.update()

    dialogo_config = ft.AlertDialog(
        title=ft.Text("Configurações"),
        content=ft.Container(content=api_input, width=300, height=70),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: setattr(dialogo_config, "open", False) or page.update()),
            ft.ElevatedButton("Salvar", on_click=salvar_chave),
        ],
    )

    page.overlay.append(dialogo_config)

    page.add(
        ft.Row([
            ft.Text("Lumina Style", size=28, weight="bold", color="blue"),
            ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda _: setattr(dialogo_config, "open", True) or page.update())
        ], alignment="spaceBetween"),
        
        ft.Divider(),
        
        ft.Container(
            content=chat,
            expand=True,
            border_radius=10,
            padding=ft.Padding(left=15, top=15, right=4, bottom=15),
        ),
        
        ft.Row([
            nova_msg,
            botao_enviar
        ])
    )

if __name__ == "__main__":
    ft.run(main)
