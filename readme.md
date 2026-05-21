# Lumina Style Bot

Customer service chatbot for a fictional fashion store, built with Python and Flet and integrated with Groq AI. The project answers questions about products, payments, shipping, exchanges, support, and also uses a local JSON catalog to retrieve store information.

## Features

- Simple graphical interface built with Flet
- Chat responses in Portuguese and English
- Groq API integration
- Product lookup from `bd.json`
- Search by category, product name, and quantity
- Basic shipping calculation using ZIP/postal codes with ViaCEP
- Ready-made answers for payments, promotions, size chart, exchanges, support, and tracking
- API key configuration directly through the interface

## Technologies

- Python
- Flet
- Groq API
- Requests
- Langdetect
- ViaCEP
- JSON

## Project Structure

```text
Lumina_Style/
├── main.py             # Project entry point
├── src/
│   ├── __init__.py
│   ├── app.py          # Chatbot graphical interface
│   └── chatbot.py      # Message, product, language, shipping, and AI logic
├── data/
│   └── bd.json         # Store database in Portuguese and English
├── .env.example        # API key configuration example
├── .gitignore
├── requirements.txt    # Project dependencies
└── readme.md           # Project documentation
```

## How to Run

### 1. Clone or download the project

```bash
git clone <repository-url>
cd Lumina_Style
```

If you already have the project folder, just open a terminal inside it.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

When the application opens, click the settings button and enter your Groq API key.

When a key is saved, the app creates a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

If the key field is cleared and saved empty, the app removes the `.env` file.

> Important: do not publish your API key in public repositories.

### 5. Run the project

```bash
python main.py
```

You can also run it as a module:

```bash
python -m src.app
```

## Example Questions

```text
Quais produtos voces vendem?
Tem camiseta?
Quero 2 mochilas
Qual o frete para 01001-000?
Quais formas de pagamento?
Tem promocao?
Como funciona a troca?
Show me the products
Do you have sneakers?
```

## Database

The `data/bd.json` file stores the shop data in two languages:

- `pt`: Portuguese responses and products
- `en`: English responses and products

Each product includes fields such as:

- `nome`
- `preco`
- `emoji`
- `cores`
- `categorias`
- `descricao`

## How It Works

The main flow is handled by `processar_mensagem_total` inside `src/chatbot.py`.

The chatbot first tries to answer using local rules:

- detects the message language;
- checks whether the user requested predefined information, such as payment or shipping;
- identifies ZIP/postal codes;
- searches products by name or category;
- calculates quantity when the user provides numbers.

If no local rule can answer the message, the project sends the question to Groq, including the store data as context.

## Future Improvements

- Add automated tests
- Improve the interface design
- Add conversation history
- Move tests into a dedicated `tests/` folder
- Automatically validate the `bd.json` format
- Create and deploy a web version

## Author

Project developed by Joaquim Koster as a study project for AI chatbots, graphical interfaces, and automated e-commerce customer service.
