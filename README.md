# LearnEase Chatbot

An intelligent chatbot system for enhancing learning experience using LangChain and LLMs.

## Features

- Natural language processing using LangChain
- PostgreSQL database integration
- Singleton pattern implementation
- Logging system
- Environment configuration

## Prerequisites

- Python 3.8+
- PostgreSQL
- Together API key
- Poetry (Python dependency management)

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd learnEase-chatbot
```

2. Install Poetry (if not installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

For Windows PowerShell:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

3. Install dependencies

```bash
poetry install
```

4. Configure environment variables
   Create a `.env` file with:

```
DATABASE_CLIENT=postgres
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=learnEase
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
TOGETHER_API_KEY=your_api_key
```

## Project Structure

```
learnEase-chatbot/
├── config/
│   ├── engine.py
│   └── logger.py
├── langChain/
│   └── langChain.py
├── logs/
├── .env
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Usage

Activate the Poetry shell:

```bash
poetry shell
```

Then use the chatbot:

```python
from langChain.langChain import LangChain

# Initialize the chatbot
chatbot = LangChain()

# Use the chatbot
response = chatbot.execute_query_tool.run("Your query here")
```

## Development

To run in debug mode with logging:

```bash
poetry run python app.py
```

## Managing Dependencies

Add a new dependency:

```bash
poetry add package_name
```

Add a development dependency:

```bash
poetry add --group dev package_name
```

Update dependencies:

```bash
poetry update
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]
