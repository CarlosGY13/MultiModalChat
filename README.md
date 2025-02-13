# MultiModalChat

MultiModalChat es un bot de Telegram diseñado para brindar recomendaciones sobre embarazo, prevención de enfermedades, cuidado prenatal, alimentación, higiene y vacunación. Además, puede analizar imágenes médicas y ofrecer respuestas breves y concisas en varios idiomas: Español, Shipibo-Konibo y Quechua.

## Características

- **Asesoramiento en salud**: Proporciona información sobre embarazo, prevención de enfermedades, cuidado prenatal, alimentación, higiene y vacunación.
- **Análisis de imágenes médicas**: Puede interpretar imágenes y ofrecer respuestas claras y concisas.
- **Soporte multilingüe**: Disponible en Español, Shipibo-Konibo y Quechua.

## Requisitos

Para ejecutar MultiModalChat, asegúrate de contar con:
- **Python 3.6 o superior**
- **Una cuenta de OpenAI** con una clave API válida
- **Un bot de Telegram** con un token válido

## Instalación

Sigue estos pasos para instalar y configurar MultiModalChat:

1. **Clona este repositorio**
   ```sh
   git clone https://github.com/tu-usuario/MultiModalChat.git
   cd MultiModalChat
   ```

2. **Crea y activa un entorno virtual**
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura las credenciales**
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```sh
   OPENAI_API_KEY="tu_clave_api_de_openai"
   TELEGRAM_BOT_TOKEN="tu_token_de_bot_de_telegram"
   ```

## Uso

1. **Ejecuta el bot**
   ```sh
   python app.py
   ```

2. **Interacción en Telegram**
   - Abre Telegram y busca tu bot mediante el nombre de usuario configurado.
   - Inicia una conversación con el bot.
   - Sigue las instrucciones para seleccionar un idioma y comenzar a recibir recomendaciones o analizar imágenes médicas.

## Estructura del Proyecto

La estructura principal del proyecto es la siguiente:

```
MultiModalChat/
├── app.py              # Archivo principal con la lógica del bot
├── requirements.txt    # Lista de dependencias
├── .env                # Archivo de configuración con claves API
├── LICENSE             # Licencia del proyecto
├── README.md           # Documentación del proyecto
```

## Licencia
Este proyecto está bajo la licencia [Apache 2.0](LICENSE).

