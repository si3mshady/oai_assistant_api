Here’s a clean, professional **README.md** you can include with that code. It explains what the script does, how to set it up, and how to use it.

---

# 🧠 OpenAIAssistant

This project provides a lightweight Python wrapper class around the **OpenAI Assistants API (beta)** to automate message threads, runs, and assistant creation.

It demonstrates how to:

* Create and manage an OpenAI Assistant programmatically
* Manage conversation threads and persistent storage using `shelve`
* Send and retrieve messages
* Run instructions through the new **Threads and Runs** API

---

## 🚀 Features

* ✅ Create an assistant with custom instructions and model
* ✅ Automatically create or reuse conversation threads
* ✅ Send user messages and retrieve assistant responses
* ✅ Persist thread data locally using Python’s built-in `shelve`
* ✅ Demonstrates real-time interaction with the **OpenAI Python SDK (beta)**

---

## 🧩 Requirements

**Python Version:** 3.9 or later

**Dependencies:**

* `openai` (latest SDK with `beta.assistants` support)
* `python-dotenv`
* `shelve` (standard library)
* `os` (standard library)

Install dependencies:

```bash
pip install openai python-dotenv
```

---

## ⚙️ Setup

1. **Clone the repository or copy the script:**

   ```bash
   git clone https://github.com/yourusername/OpenAIAssistant.git
   cd OpenAIAssistant
   ```

2. **Create a `.env` file** in the project directory and add your API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the script:**

   ```bash
   python assistant.py
   ```

---

## 🧠 How It Works

### 1. Initialization

When you instantiate the class:

```python
roboto = OpenAIAssistant()
```

The assistant loads your environment variables and prepares the OpenAI client.

### 2. Create an Assistant

```python
roboto.create_assistant()
```

This creates an OpenAI Assistant instance with custom instructions and model (default: `gpt-3.5-turbo`).

### 3. Create or Retrieve a Thread

Threads store message context. The script either:

* Creates a new thread (and saves it using `shelve`)
* Or reuses an existing one from local storage

```python
roboto.create_thread()
```

### 4. Send a Message

```python
roboto.create_message("When is Veterans Day each year in America?")
```

This sends a user message into the assistant’s thread.

### 5. Run Instructions

```python
roboto.run_errand(roboto.thread_id, roboto.assistant.id, roboto.instructions)
```

This executes the assistant run, waits for completion, and prints the response.

---

## 🧾 Example Output

```
Assistant created: MrRobot
Thread created and saved to db
Running assistant...
Veterans Day is observed annually on November 11 in the United States.
```

---

## ⚠️ Notes

* The `check_thread_exists`, `save_to_db`, and `get_thread_id` methods are partially commented out.
  You can uncomment or extend them to make thread persistence functional.
* Replace `gpt-3.5-turbo` with `gpt-4.1-mini` or higher for better results.
* This script uses **blocking** polling (`time.sleep(5)`), so consider using async calls for production environments.

---

## 🧑‍💻 Example Customization

To change the assistant’s personality:

```python
roboto = OpenAIAssistant(
    name="HelperBot",
    instructions="Respond in a friendly tone and provide concise answers.",
    model="gpt-4.1"
)
```

To change the default question:

```python
roboto.create_prompt_message = "Explain quantum computing in simple terms."
```

---

## 📜 License

MIT License © 2025 [Your Name]

---

Would you like me to format it with Markdown badges and emojis (like “built with Python 🐍” or “powered by OpenAI ⚡”) to make it more GitHub-ready?
