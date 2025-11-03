# reAct Agent + RAG System with Model-Context-Protocol (MCP)

Retrieval-Augmented Generation (RAG) system built using a decoupled architecture. It leverages **LangChain**, is powered by **Gemini embeddings** and the **Gemini 2.5 Flash model**, and is exposed as a microservice using the **Model-Context-Protocol (MCP)** via the `FastMCP` framework.

The application is split into three main components: a server (backend RAG), an asynchronous command-line client for testing, and a Streamlit web client for interaction.

https://github.com/user-attachments/assets/895b83b3-ef0b-4cce-8f7f-ae9140f5eb3b

## Key Features

* **Gemini-Powered RAG:** Uses `GoogleGenerativeAIEmbeddings` (`text-embedding-004`) for vector creation and `gemini-2.5-flash` for question answering.
* **Decoupled Architecture (MCP):** The RAG logic runs as a separate service using **FastMCP** with `streamable-http` transport, promoting modularity and scalability.
* **Vector Store:** **Chroma** is used to store and retrieve document chunks.
* **Interactive Frontend:** A modern, form-based **Streamlit** application provides a smooth chat interface.

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.9+**

2.  **`pip`** and **`venv`**

3.  **Install dependencies:**
    ```bash
    pip install langchain-google-genai langchain-community langchain-classic fastmcp streamlit python-dotenv pypdf
    ```

4.  **Set up your API Key:**
    Create a file named `.env` in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

5.  **Add Sample Data:**
    Place the PDF file you wish to query into the project root and name it **`sample.pdf`**.

## 🏃 Running the Application

This is a **client-server application** and requires **two steps** to run simultaneously.

### Step 1: Start the MCP RAG Server

Open your **first terminal** and run the server file. This process loads the PDF, creates the vector database, initializes the RAG chain, and starts the MCP service on `http://127.0.0.1:8000`.

```bash
python rag_mcp_server.py
```
<img width="1328" height="453" alt="RAG (1)" src="https://github.com/user-attachments/assets/2aae0723-b41b-4e2c-a960-aa5d046fc4a3" />

### Step 2A: Run the Streamlit Web Client (Recommended)

Open a **second terminal** and run the Streamlit frontend. This client will use `fastmcp.Client` to communicate with the running server.

``` bash 
streamlit run rag_mcp_client.py
```

<img width="806" height="243" alt="RAG (2)" src="https://github.com/user-attachments/assets/8c7ee987-5fb0-41e8-aa91-45f1ec61c4b6" />

A browser window will automatically open with the chat interface.

### Step 2B: Run the Terminal Client (For Testing)

Alternatively, you can test the MCP connection directly using the terminal client:

``` bash 
python terminal_mcp_client.py
```

The backend RAG uses the following sequence:

* **Embeddings:** `GoogleGenerativeAIEmbeddings(model="text-embedding-004")`
* **Vector DB:** `Chroma`
* **LLM:** `ChatGoogleGenerativeAI(model="gemini-2.5-flash")`
* **Chain:** `RetrievalQA.from_chain_type` combines these components into the `retrieve_answer` function.
