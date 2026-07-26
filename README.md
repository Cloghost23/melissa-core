


For androids:
pkg update && pkg install libandroid-spawn
pkg install wget

# 1. Update packages and pull down the development toolchain
pkg update && pkg install git cmake clang ninja -y

# 2. Clone the codebase
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# 3. Configure and compile using Ninja
cmake -B build -G Ninja
cmake --build build --config Release -j $(nproc)

# First option for global access of llama.cpp 
cd ~/llama.cpp 
cp build/bin/llama-* $PREFIX/bin/

# Second option 
cd ~/llama.cpp
cmake --install build --prefix $PREFIX



For native Linux devices:
# Update and install system prerequisites (Ubuntu/Debian example)
sudo apt update && sudo apt install -y git build-essential cmake ninja-build

# Clone the repository and enter the directory
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Configure the build tree using Ninja as the generator
sudo apt install ninja
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# Run the build
cmake --build build --config Release
sudo cmake --install build


cd /
llama-server --version



# Melissa: Local Autonomous AI Assistant

Melissa is a custom, web-based autonomous AI software agent and user interface engineered to run completely locally on mobile hardware configurations. Designed to bypass the privacy concerns and subscription costs of cloud-reliant platforms, Melissa brings robust, context-aware analysis directly onto the device.

---

## 🛠️ Core Architecture & Features

*   **Localized Architecture:** Powered by a lightweight Python Flask web server integrated directly with a local inference server.
*   **Self-Contained Mobile Environment:** Optimized to execute entirely within an Android Termux environment, operating fully independent of external cloud networks.
*   **Sliding Window Memory:** Implements a custom orchestration layer that manages a rolling history of the most recent conversation turns to prevent token overflow and eliminate context amnesia.
*   **Direct Math Evaluation Bypass:** Features an intelligent regex-driven interceptor that handles straightforward arithmetic operations natively within the Python backend to preserve CPU cycles.
*   **Hardware Spike Patience:** Configured with an extended 120-second connection timeout threshold to gracefully handle processing spikes inherent to local mobile processors.
*   **100% Offline KaTeX Rendering:** Integrated with local math rendering scripts, allowing complex physics concepts and mathematical equations to render beautifully as clean formulas without requiring an active internet connection.
*   **Premium UX Utilities:** Includes a slide-out Session History Sidebar with real-time text filtering, inline message copying, and one-tap backend response regeneration.

---

## 📐 Project Structure

```text
melissa-project/
├── app.py                 # Flask Backend Orchestration Layer
├── static/                # Local Asset Storage (100% Offline)
│   ├── auto-render.min.js # Local KaTeX Auto-Renderer
│   ├── katex.min.css      # Local KaTeX Stylesheet
│   └── katex.min.js       # Local KaTeX Core Engine
└── templates/
    └── index.html         # Responsive Dark-Mode UI Shell


After the endeavour of this setup, the final nail in the coffin is to run the llama.cpp server on port 8080 with this command:
llama-server -m ["with your LLM"] -c 2048 
--port 8080

Then go to your app.py and run it
Note: it's always a good practice to launch a virtual environment like .venv with this type of projects 
