<h1 align="center">🎵 Advanced Audio Enhancement System (AAES)</h1>

<p align="center">
  A DSP-powered system for real-time audio enhancement, noise reduction, and intelligent stereo optimization.
</p>

<hr/>

<h2>📌 Overview</h2>

<p>
  <strong>AAES</strong> is a <strong>Digital Signal Processing (DSP)-based</strong> audio enhancement system built using a <strong>React frontend</strong> and a <strong>Python backend</strong>. 
  It improves audio clarity with noise reduction, frequency balancing, and stereo enhancement — ideal for:
</p>

<ul>
  <li>🎧 Music enhancement</li>
  <li>🗣️ VoIP & communication clarity</li>
  <li>♿ Assistive hearing technologies</li>
  <li>🎙️ Real-time DSP processing</li>
</ul>

<hr/>

<h2>✨ Key Features</h2>

<ul>
  <li>✅ <strong>Noise Reduction</strong> – Removes background noise</li>
  <li>✅ <strong>Stereo Enhancement</strong> – Improves left-right audio clarity</li>
  <li>✅ <strong>Dynamic Equalization</strong> – Balances audio frequencies</li>
  <li>✅ <strong>Real-Time DSP</strong> – FFT/STFT-based fast processing</li>
  <li>✅ <strong>User-Friendly React UI</strong></li>
  <li>✅ Supports <strong>WAV, MP3, FLAC</strong></li>
  <li>✅ <strong>Cross-Platform</strong> (Web + Local Processing)</li>
</ul>

<hr/>

<h2>🧰 Tech Stack</h2>

<h3>Frontend (React.js)</h3>
<ul>
  <li>React + Vite</li>
  <li>Tailwind CSS</li>
  <li>Axios</li>
  <li>React Router</li>
  <li>Web Audio API</li>
</ul>

<h3>Backend (Python)</h3>
<ul>
  <li>Flask</li>
  <li>NumPy, SciPy</li>
  <li>PyDub</li>
  <li>Librosa</li>
  <li>SoundFile</li>
  <li>FFmpeg</li>
  <li>Custom DSP modules <code>(services/)</code></li>
</ul>

<hr/>

<h2>📁 Updated Project Structure</h2>

<pre>
AAES/
│── frontend/                          
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.css
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       ├── assets/
│       ├── components/albumCover.jsx
│       └── components/utils.jsx
│
│── backend/                           
│   ├── app/
│   │   ├── main.py
│   │   ├── services/
│   │   │   └── lnr.py
│   │   └── routes/api.py
│   └── requirements.txt
│
│── docs/
│── README.md
│── .gitignore
</pre>

<hr/>

<h2>⚙️ Installation & Setup</h2>

<h3>🔧 Backend Setup (Python)</h3>

<p><strong>Prerequisites:</strong> Python 3.9+, FFmpeg installed</p>

<pre>
cd backend
pip install -r requirements.txt
python app/main.py
</pre>

<h3>💻 Frontend Setup (React + Vite)</h3>

<pre>
cd frontend
npm install
npm run dev
</pre>

<hr/>

<h2>🚀 Usage</h2>

<ol>
  <li>Start backend server: <code>python app/main.py</code></li>
  <li>Start React frontend: <code>npm run dev</code></li>
  <li>Open the UI and upload an audio file</li>
  <li>Choose enhancement features</li>
  <li>Preview / download the enhanced audio</li>
</ol>

<hr/>

<h2>🔌 API Endpoints</h2>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>POST</td>
    <td>/upload</td>
    <td>Upload audio file</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/process</td>
    <td>Process and enhance audio</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/download</td>
    <td>Download enhanced audio</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/status</td>
    <td>Check processing status</td>
  </tr>
</table>

<hr/>

<h2>🧑‍💻 Contributors</h2>

<ul>
  <li><strong>Surath Chowdhury</strong> – Creator</li>
  <li><strong>Sristi Priya</strong> – Frontend Developer</li>
  <li><strong>Sneha Mal</strong> – UI/UX</li>
  <li><strong>Sameer Kumar Choudhury</strong> – Contributor</li>
</ul>

<p>📧 <strong>Contact:</strong> <a href="mailto:surath172003@gmail.com">surath172003@gmail.com</a></p>

<hr/>

<h2>📝 License</h2>

<p><strong>MIT License</strong> — Free to use, modify, and distribute.</p>

<hr/>

<h2>🎉 Improvements Included</h2>

<ul>
  <li>✔ Accurate folder structure based on actual GitHub repo</li>
  <li>✔ Professional formatting</li>
  <li>✔ Improved readability</li>
  <li>✔ Polished UI/UX wording</li>
  <li>✔ Clean HTML formatting for GitHub</li>
</ul>
