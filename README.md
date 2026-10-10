<div align="center">

# Financial Filing AI Assistant (Chatbot) 🚀

<img src="https://github.com/user-attachments/assets/b6b4568e-f80f-4dd6-9556-dce2333bffc7" alt="Demo GIF" />

</div>

---

**genai-sec10k-insights** is a full-stack Retrieval-Augmented Generation (RAG) web application that enables users to interactively query and analyze SEC 10-K filings from major companies. The system extracts key insights from long-form financial reports using a semantic search pipeline powered by OpenAI embeddings and a FAISS vector store, all deployed behind a FastAPI backend and custom frontend.

---

## 📌 Features

- 🔍 **Query Interface**: Users can ask questions in natural language and get context-aware answers from 10-K filings.
- 📄 **Document Source**: Uses real SEC 10-K filings from companies like AAPL, TSLA, JPM, etc.
- ⚙️ **Backend**: FastAPI-based API server with secure authentication and RAG pipeline.
- 🧠 **Vector Search**: OpenAI embeddings + FAISS index for fast and accurate semantic retrieval.
- 💻 **Frontend**: Custom HTML, CSS, and JavaScript interface with clean UI and dynamic response rendering.
- 🔐 **Authentication**: Random 6-digit terminal-generated access code required before accessing the app.

---

## 🗂️ Project Structure

```

genai-sec10k-insights/
├── backend/
│   └── app/
│       ├── main.py               # FastAPI entry point
│       ├── api\_routes.py         # API route handlers
│       ├── config.example.py     # Config template
│       └── rag\_pipeline.py       # RAG logic: load FAISS, embed, search
│
├── data/
│   ├── raw/                      # Raw 10-K filings (e.g., AAPL\_10k.txt)
│   ├── parsed/                   # Chunked JSON from raw filings
│   └── faiss\_index/             # Prebuilt FAISS index and mapping
│
├── sec\_downloader/              # Utility scripts
│   ├── download\_sec\_filings.py  # Scrapes and saves raw 10-Ks
│   ├── chunk\_text.py            # Splits long 10-K text into chunks
│   └── embed\_and\_store.py       # Embeds chunks and builds FAISS index
│
├── frontend/
│   ├── index.html               # Main chat UI
│   ├── auth.html                # Auth page with blur effect
│   ├── styles.css               # Styling for layout and animation
│   ├── app.js                   # Query + response logic (AJAX)
│   └── assets/                  # Fonts, icons, etc.
│
├── notebooks/
│   └── mock\_10k\_40\_questions.json  # Mock questions for testing
│
├── Dockerfile                   # Production-ready Docker image
├── requirements.txt             # Python dependencies
├── LICENSE
└── README.md                    # You're here!

````
## 🚦 Step-by-Step Walkthrough

Follow this guided walkthrough to experience the full pipeline from server startup to querying a 10-K report:

---

### 🔁 1. Start the FastAPI Server

From the project root, run the backend using:

```bash
cd backend
uvicorn app.main:app --reload
````

Once started, you'll see a **well-formatted terminal output** styled using `rich`, including:

* Project banner
* Usage instructions
* Export variable tips
* A **random 6-digit authentication code**

Example:

```
🚀 genai-sec10k-insights is running on http://localhost:8000
🔒 Auth Code: 348215
🔗 Visit /chat to access the chatbot interface
```
###
![Screenshot from 2025-05-25 09-46-35 (1)](https://github.com/user-attachments/assets/c69cafca-3bbe-4720-bf36-bf7ca1597bbf)
###
---

### 🌐 2. Visit the Web App in Your Browser

Open:

```
http://localhost:8000
```

You’ll be taken to the **authentication screen** (`auth.html`) which has:

* A minimal design with blurred background
* An input field for the 6-digit code

Enter the code shown in your terminal and proceed.
###
![Screenshot from 2025-05-25 10-55-23](https://github.com/user-attachments/assets/afc7495c-c0e2-4104-a73b-74e77629b3db)
###
---

### 💬 3. Access the Chatbot Interface

Once authenticated, you'll land on the **main chat interface** (`index.html`) where you can:

* Ask any question related to the SEC 10-K reports of the 10 companies
* View dynamic responses with smooth UI animations
###
![ScreenShot Tool -20250525111020](https://github.com/user-attachments/assets/8b06117a-7287-480c-bfc4-cc844106de2d)
###
---


### 📥 4. Use an Example Prompt (or Ask Your Own)

To help you get started, we’ve provided a few **sample prompts** in:

```

notebooks/mock\_10k\_40\_questions.json

````

Here’s one you can try immediately:

```json
{
  "question": "What does Microsoft report about cybersecurity risks?"
}
````
###
![main](https://github.com/user-attachments/assets/7768f962-6e0f-4c98-82ac-15e98b5b8316)
###

📌 **Important Note:**
These are just **example prompts** — the chatbot is **not limited** to answering only those.
###
![Screenshot from 2025-05-25 09-49-41 (1)](https://github.com/user-attachments/assets/752b7a30-e6d0-4893-90a8-7479f05e6b16)
###
Since this app is built on top of the **actual SEC 10-K filings** from 10 companies (AAPL, MSFT, TSLA, AMZN, etc.), you can ask **any meaningful financial or business-related question** that could be answered from those filings.

✅ For example:

* "What does Apple say about supply chain risks?"
* "How does Amazon describe its revenue streams?"
* "What litigation risks does Meta report?"

Just make sure your question is **relevant to the content typically found in 10-K reports** (i.e., risk factors, business overview, financials, strategy, etc.).

Once submitted, your question will be semantically searched across the embedded document chunks, and an accurate answer will be generated based on the most relevant 10-K sources.
###
![Screencastfrom2025-05-2509-54-46-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/ba7e619b-463b-4fcf-b65f-5d3a8d975601)
###

---

## ⚙️ How It Works

### 1. Data Acquisition (`sec_downloader`)
- 10-K reports are downloaded using `download_sec_filings.py`.
- Files are stored in `data/raw/`.

### 2. Preprocessing
- `chunk_text.py` splits raw text into overlapping chunks with metadata.
- Output chunks saved as JSON in `data/parsed/`.

### 3. Embedding & Indexing
- `embed_and_store.py` uses OpenAI’s `text-embedding-3-small` model to embed parsed chunks.
- Embeddings stored in a FAISS index (`index.faiss` and `index.pkl`) under `data/faiss_index/`.

### 4. Backend (`backend/app`)
- `main.py` initializes FastAPI with secure cookie auth.
- `rag_pipeline.py` handles query embedding, similarity search via FAISS, and prompt construction.
- `api_routes.py` serves `/chat` route with POST support for queries.
- A random 6-digit access code is printed at app launch and must be entered to unlock the app.

### 5. Frontend (`frontend`)
- `auth.html`: Initial page prompts for access code with a blurred background.
- `index.html`: Interactive UI with user input box, loading animation, and styled answer display.
- `app.js`: Handles sending queries, receiving responses, and displaying them in real time.
- `styles.css`: Custom CSS for layout, transitions, and visual polish.

---

## 🚀 Running the App Locally

### 1. Clone the Repo

```bash
git clone https://github.com/r0han01/genai-sec10k-insights.git
cd genai-sec10k-insights
````

### 2. Set Up Environment

```bash
cd backend
cp app/config.example.py app/config.py
# Add your OpenAI API key and config in config.py
pip install -r requirements.txt
```

### 3. Run the App

```bash
cd backend
uvicorn app.main:app --reload
```

Access the app at: [http://localhost:8000/chat](http://localhost:8000/chat)

> ⚠️ Enter the access code displayed in the terminal on the `auth.html` page to unlock access.

### 4. (Optional) Docker Build

```bash
docker build -t genai-sec10k-app .
docker run -p 8000:8000 genai-sec10k-app
```

---

## 🔒 Authentication Mechanism

* When the FastAPI server starts, a secure 6-digit numeric access code is printed in the terminal.
* This must be entered on the frontend’s auth page before gaining access.
* Auth state is stored in cookies to protect `/chat` and `/docs`.

---

## 📊 Companies Covered

The app includes processed 10-K filings from the following companies:

* Apple (AAPL)
* Amazon (AMZN)
* JPMorgan Chase (JPM)
* Coca-Cola (KO)
* Meta (META)
* Microsoft (MSFT)
* NVIDIA (NVDA)
* Pfizer (PFE)
* Tesla (TSLA)
* Walmart (WMT)

## 🛠️ Troubleshooting & Swagger Testing

If the frontend chatbot interface (`/chat`) does not seem to be working correctly (e.g., blank responses, stuck loading, or CORS errors), you can **directly test the backend API** using the built-in Swagger UI at:
###
![Screencastfrom2025-05-2512-06-09-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/990ddaa1-9f8f-4a29-b42a-23eed6b31595)
###

```

http://localhost:8000/docs

````

### ✅ Why Use This?

- Confirms whether the backend and RAG pipeline are functioning correctly.
- Helps isolate whether issues originate from the **frontend** or **backend**.
- Allows developers to quickly debug request/response flow without modifying UI.

---

### 🧪 How to Test via Swagger

1. Make sure your FastAPI backend is running:
   ```bash
   uvicorn app.main:app --reload

2. Open your browser and go to:

   ```
   http://localhost:8000/docs
   ```

3. Scroll down to the `POST /ask` endpoint.

4. Click on **`Try it out`**.

5. In the request body, paste the following prompt:

   ```json
   {
     "question": "What does Microsoft report about cybersecurity risks?"
   }
   ```

6. Click **Execute**.

7. You should receive a structured JSON response:

   ```json
   {
     "answer": "Microsoft discusses cybersecurity risks related to...",
     "sources": [
       "MSFT_10k.txt"
     ]
   }
   ```

---

### 🧩 If It Works Here but Not in Frontend

If the Swagger `/ask` test returns valid responses but the frontend (`/chat`) does not:

* ✅ It means your **backend RAG pipeline is working fine**.
* ❌ The issue is likely in:

  * `frontend/app.js` (JavaScript fetch logic)
  * CORS configuration (make sure backend allows frontend origin)
  * Cookie or auth state mismatch

---

### 🔧 Recommended Fixes

* Check the console in browser dev tools (`F12`) for network or JS errors.
* Verify you're logged in with the correct 6-digit code.
* Ensure `fetch` requests from the frontend hit the same `/ask` endpoint with correct `Content-Type` headers.

---

By using the Swagger UI, you can verify your backend independently and streamline debugging efforts.

## 🧯 Stopping Docker Containers Safely

If you're running this app via Docker and need to stop it manually (especially if `docker stop` doesn't work or Docker is unresponsive), follow these steps:

---

### 🔍 1. List All Docker-Related Processes

Use `ps` and `grep` to identify Docker processes:

```bash
ps aux | grep docker
````

Sample output might include:

```
root     1234  ... /usr/bin/dockerd
root     2345  ... docker-containerd
user     3456  ... docker-proxy ...
```

Avoid killing core Docker daemons like `dockerd` or `containerd`.

---

### 🔪 2. Kill the Container Process by PID (Preferred)

Find the PID of the container process:

```bash
docker inspect --format '{{.State.Pid}}' genai-sec10k-container
```

Then stop it forcefully:

```bash
sudo kill -9 <PID>
```

Replace `<PID>` with the number returned above.

---

### 💥 3. Kill All Docker Container Processes (Advanced)

If you're confident and want to kill all Docker-related processes manually:

```bash
ps aux | grep docker | grep -v grep
```

Note the PIDs in column 2, then:

```bash
sudo kill -9 <pid1> <pid2> ...
```

⚠️ **Warning:** Only do this if you know what you're killing. Terminating Docker system processes may disrupt all containers or require restarting the Docker service.

---

### ✅ One-Liner (Recommended)

To quickly kill the container process cleanly:

```bash
sudo kill -9 $(docker inspect --format '{{.State.Pid}}' genai-sec10k-container)
```

This is the safest way to force-stop just the container, without impacting Docker itself.

## 🚀 Deployment on AWS EC2

You can deploy this full-stack RAG-based chatbot on an AWS EC2 instance using Docker. This section includes a full guide and real-world fixes for issues you might encounter.

---

### 🧱 Requirements

- AWS Account
- EC2 access with security group allowing:
  - Port **22** (SSH)
  - Port **8000** (FastAPI)
- SSH key pair (`.pem` file)
- `Docker` and `Git` installed on the EC2 instance
- OpenAI API Key

---

### 🔧 1. Launch EC2 Instance

- AMI: **Amazon Linux 2023**
- Type: `t2.micro` (Free Tier eligible)
- Enable auto-assign public IP
- Security group must include:
  - SSH (port 22) → `0.0.0.0/0`
  - HTTP (port 80) → `0.0.0.0/0` *(optional)*
  - Custom TCP (port 8000) → `0.0.0.0/0`

---

### 🔐 2. Connect via SSH

```bash
ssh -i /path/to/genai-key.pem ec2-user@<your-ec2-public-ip>
````

> If you get “Too many authentication failures”, use:

```bash
ssh -i /path/to/genai-key.pem -o IdentitiesOnly=yes ec2-user@<your-ec2-public-ip>
```

---

### 🐳 3. Install Docker and Git on EC2

```bash
sudo yum update -y
sudo yum install docker git -y
sudo service docker start
sudo usermod -aG docker ec2-user
exit
```

Re-login after the last step to activate Docker group changes.

---

### 📦 4. Clone the Repository

```bash
git clone https://github.com/r0han01/genai-sec10k-insights.git
cd genai-sec10k-insights
```

---

### 📁 5. Upload Your `data/` Folder (FAISS index + 10-K chunks)

On your **local machine**, run:

```bash
scp -i /path/to/genai-key.pem -o IdentitiesOnly=yes -r \
~/CoursePractice/aiProject/genai-sec10k-insights/data \
ec2-user@<your-ec2-public-ip>:~/genai-sec10k-insights/
```

> This avoids needing to rebuild the vector store on EC2.

---

### 🧪 6. Ensure Your Dockerfile Includes the `data/` Directory

Make sure this line in `Dockerfile` is uncommented:

```dockerfile
COPY data ./data
```

---

### 🧱 7. Build the Docker Image

```bash
docker build -t genai-sec10k-app .
```

---

### 🔑 8. Run the Container (Foreground with API Key)

```bash
docker run -p 8000:8000 \
  --name genai-sec10k-container \
  -e OPENAI_API_KEY=your-key-here \
  genai-sec10k-app
```

> This runs the app in the foreground so you can see logs and the auth code.

---

### 🌐 9. Access Your Web App

Open your browser:

```
http://<your-ec2-public-ip>:8000
```

* Enter the 6-digit code shown in your EC2 terminal
* You’ll be redirected to the chatbot interface
* Ask any question like:

```text
What does Microsoft report about cybersecurity risks?
```

---

### 🧩 Common Issues & Fixes

| Problem                            | Fix                                                                |
| ---------------------------------- | ------------------------------------------------------------------ |
| `Too many authentication failures` | Use `-o IdentitiesOnly=yes` with `ssh` or `scp`                    |
| `COPY data ./data` fails           | Make sure `data/` exists locally and isn’t ignored by `.gitignore` |
| App runs but doesn't answer        | You're missing the FAISS vector index — upload your `data/` folder |
| Input fields zoom on mobile        | Set `font-size: 16px` in `styles.css` for all input fields         |




