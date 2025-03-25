# Advanced Audio Enhancement System (AAES) 🎵

## Overview
**AAES** is a **digital signal processing (DSP)-based** solution designed to enhance audio quality by reducing noise, improving stereo separation, and optimizing frequency balance. Built with a **React frontend** and a **Python backend**, AAES offers a seamless and efficient user experience. The system leverages advanced algorithms for **real-time audio enhancement**, making it suitable for various applications like **music streaming, VoIP communication, gaming, and assistive technologies**.

## Features
✅ **Noise Reduction** – Removes background noise for clearer audio  
✅ **Stereo Enhancement** – Expands left-right channel separation  
✅ **Dynamic Equalization** – Optimizes frequency response for balanced sound  
✅ **Real-Time Processing** – Fast and efficient DSP algorithms for instant results  
✅ **User-Friendly Interface** – Simple and intuitive UI for ease of use  
✅ **Multi-Format Support** – Works with MP3, WAV, and FLAC formats  
✅ **Cross-Platform Compatibility** – Can be used on desktop and mobile devices  

## Tech Stack
### Frontend (React)
- **React.js** – UI Development
- **Tailwind CSS** – Styling for responsive design
- **Axios** – API communication
- **Web Audio API** – Audio processing in the browser
- **React Router** – Navigation and routing
- **Redux/Context API** – State management

### Backend (Python)
- **Flask/FastAPI** – API development and request handling
- **NumPy & SciPy** – Signal processing and mathematical operations
- **PyDub** – Audio manipulation and format conversion
- **FFmpeg** – Processing and encoding audio files

## Project Structure
```
AAES/
│── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/    # UI Components
│   │   ├── pages/         # Application Pages
│   │   ├── utils/         # Utility Functions
│   │   ├── App.js         # Main Component
│   │   └── index.js       # Entry Point
│   └── public/            # Static Files (HTML, Icons, etc.)
│
│── backend/               # Python Backend
│   ├── app/
│   │   ├── routes/        # API Endpoints
│   │   ├── services/      # DSP Processing Functions
│   │   ├── main.py        # Entry Point
│   └── requirements.txt   # Dependencies
│
│── docs/                  # Documentation Files
│── README.md              # Project Documentation
│── package.json           # Frontend Dependencies
│── requirements.txt       # Backend Dependencies
│── .gitignore             # Git Ignore File
```

## Installation & Setup
### Prerequisites
- **Node.js & npm/yarn** (For React Frontend)
- **Python 3.x & pip** (For Backend)
- **FFmpeg** (For audio processing, install via `sudo apt install ffmpeg` on Linux/macOS or use Windows binaries)

### Backend Setup (Python)
```bash
cd backend
pip install -r requirements.txt
python index.py  # Start the API Server
```

### Frontend Setup (React)
```bash
cd frontend
npm ci  # Install Dependencies
npm run dev    # Run the Development Server
```

## Usage
1. Run the **backend server** (`python index.py`)
2. Start the **React frontend** (`npm run dev`)
3. Upload an audio file, apply enhancement features, and download the optimized version

## API Endpoints (Backend)
| Method | Endpoint       | Description                      |
|--------|--------------|----------------------------------|
| POST   | `/upload`    | Upload an audio file             |
| GET    | `/process`   | Process and enhance the audio    |
| GET    | `/download`  | Download the enhanced audio file |
| GET    | `/status`    | Check the processing status      |

## Contribution
🚀 Contributions are welcome! Follow these steps to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
📜 **MIT License** – Free to use and modify under open-source terms.

---

## Collaborators
👥 This project is maintained by:
- [Surath Chowdhury](https://github.com/Surath83)
- [Sristi Priya](https://github.com/SristiPriya01)
- [Sneha Mal](https://github.com/Snehamal)
- [Sameer Kumar Choudhury](https://github.com/contributor4)

📧 **Contact:** surath172003@gmail.com


