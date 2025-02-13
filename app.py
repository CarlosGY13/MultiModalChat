import os
import base64
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from openai import OpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

async def analyze_image(update: Update, context: CallbackContext, image_path: str):
    base64_image = encode_image(image_path)
    language = context.user_data.get('language', 'es')
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Analiza los resultados médicos en la imagen y "
                                f"brinda una respuesta clara y sencilla en {language}:\n"
                                "- Si los resultados son normales, confirma que están bien.\n"
                                "- Si hay valores anómalos, da una recomendación básica.\n"
                                "Ejemplo de recomendación: 'Tu nivel de glucosa está alto, es recomendable reducir el consumo de azúcar y hacer ejercicio.'"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )
        clean_response = response.choices[0].message.content.replace("*", "").replace("#", "")
        await update.message.reply_text(clean_response)
    except FileNotFoundError:
        await update.message.reply_text("Error: La imagen no se encontró en la ruta especificada.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "¡Hola! Soy un bot de Telegram diseñado para brindarte recomendaciones sobre embarazo, "
        "prevención de enfermedades, cuidado prenatal, alimentación, higiene y vacunación. "
        "También puedo analizar imágenes médicas y ofrecer respuestas breves y concisas. "
        "Por favor, selecciona el idioma en el que deseas recibir las respuestas:\n"
        "1. Español\n"
        "2. Shipibo-Konibo\n"
        "3. Quechua"
    )

async def select_language(update: Update, context: CallbackContext):
    text = update.message.text.replace("*", "").replace("#", "")
    if text == "1":
        context.user_data['language'] = 'es'
        await update.message.reply_text("Has seleccionado Español.")
    elif text == "2":
        context.user_data['language'] = 'shipibo-konibo'
        await update.message.reply_text("Has seleccionado Shipibo-Konibo.")
    elif text == "3":
        context.user_data['language'] = 'quechua'
        await update.message.reply_text("Has seleccionado Quechua.")
    else:
        await update.message.reply_text("Selección no válida. Por favor, selecciona 1, 2 o 3.")

async def handle_query(update: Update, context: CallbackContext):
    if 'language' not in context.user_data:
        await select_language(update, context)
        return

    language = context.user_data.get('language', 'es')
    user_query = update.message.text.replace("*", "").replace("#", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Actúa como un chatbot en {language}, brindando recomendaciones sobre embarazo, "
                        "prevención de enfermedades, cuidado prenatal, alimentación, higiene y vacunación. "
                        "También puedes analizar imágenes médicas y brindar respuestas breves. Procura que tus respuestas "
                        "a imágenes sean lo más concisas posibles. "
                        "Limítate a responder únicamente los temas mencionados en este prompt. "
                        "No des recetas médicas, no hables de medicamentos específicos.\n"
                        f"{user_query}"
                    ),
                }
            ],
        )
        clean_response = response.choices[0].message.content.replace("*", "").replace("#", "")
        await update.message.reply_text(clean_response)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def handle_image(update: Update, context: CallbackContext):
    if 'language' not in context.user_data:
        await select_language(update, context)
        return

    language = context.user_data.get('language', 'es')
    photo_file = await update.message.photo[-1].get_file()
    image_path = f"temp/{photo_file.file_id}.jpg"

    # Create the temp directory if it doesn't exist
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    await photo_file.download_to_drive(image_path)
    await analyze_image(update, context, image_path)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
