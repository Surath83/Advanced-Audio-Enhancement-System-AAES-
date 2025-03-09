import { useState, useRef } from "react";
import axios from "axios";
import Style from "./App.module.css";

function AudioPlayer({ title, audioRef, src, isPlaying, setIsPlaying, onPlay }) {
  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        onPlay();
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className={Style.box}>
      <h2>{title}</h2>
      <audio ref={audioRef} src={src} controls></audio>
      <button className={Style.audioButton} onClick={togglePlay}>
        {isPlaying ? "Pause" : "Play"}
      </button>
    </div>
  );
}

function App() {
  const audioRef1 = useRef(null);
  const audioRef2 = useRef(null);
  const [isPlaying1, setIsPlaying1] = useState(false);
  const [isPlaying2, setIsPlaying2] = useState(false);
  const [audioSrc, setAudioSrc] = useState(null);
  const [enhancedAudio, setEnhancedAudio] = useState(null);
  const [isExportable, setIsExportable] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const stopAllAudio = () => {
    if (audioRef1.current) audioRef1.current.pause();
    if (audioRef2.current) audioRef2.current.pause();
    setIsPlaying1(false);
    setIsPlaying2(false);
  };

  const handleAudioUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setAudioSrc(URL.createObjectURL(file)); // Original audio
      setEnhancedAudio(response.data.processed_file); // Processed audio from backend
      setIsExportable(true);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async () => {
    if (!enhancedAudio) return;

    try {
      const response = await axios.get(enhancedAudio, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "enhancedAudio.mp3"); // File name
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Download failed:", error);
    }
  };

  return (
    <div className={Style.body}>
      <center>
        <h1 className={Style.head}>Advanced-Audio-Enhancement-System [AAES]</h1>

        <div className={Style.audioContainer}>
          <AudioPlayer
            title="Original Audio"
            audioRef={audioRef1}
            src={audioSrc}
            isPlaying={isPlaying1}
            setIsPlaying={setIsPlaying1}
            onPlay={() => {
              stopAllAudio();
              setIsPlaying1(true);
            }}
          />

          <AudioPlayer
            title="Enhanced Audio"
            audioRef={audioRef2}
            src={enhancedAudio}
            isPlaying={isPlaying2}
            setIsPlaying={setIsPlaying2}
            onPlay={() => {
              stopAllAudio();
              setIsPlaying2(true);
            }}
          />
        </div>

        <input
          type="file"
          accept="audio/*"
          ref={fileInputRef}
          onChange={handleAudioUpload}
          style={{ display: "none" }}
        />

        <button className={Style.import} onClick={() => fileInputRef.current.click()} disabled={uploading}>
          {uploading ? "Uploading..." : "Import"}
        </button>

        <button className={Style.export} onClick={handleDownload} disabled={!isExportable}>
          Export
        </button>
      </center>
    </div>
  );
}

export default App;
