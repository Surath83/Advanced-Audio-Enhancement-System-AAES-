import { useState, useRef } from "react";
import axios from "axios";
import Style from "./Aaes.module.css";

function Slider({ label, value, onChange, min, max, step }) {
  return (
    <div className={Style.sliderBox}>
      <label className={Style.sliderLabel}>
        {label}: {value} dB
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        className={Style.slider}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

function Slider1({ label, value, onChange, min, max, step }) {
  return (
    <div className={Style.sliderBox}>
      <label className={Style.sliderLabel}>
        {label}: {value} %
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        className={Style.slider}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

function Aaes() {
  const audioRef1 = useRef(null);
  const audioRef2 = useRef(null);
  const fileInputRef = useRef(null);

  const [audioSrc, setAudioSrc] = useState(null);
  const [enhancedAudio, setEnhancedAudio] = useState(null);
  const [processedFileName, setProcessedFileName] = useState(null);

  const [isExportable, setIsExportable] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFormat, setSelectedFormat] = useState("wav");

  // Hearing Loss
  const defaultHL = {
    125: 0,
    250: 0,
    500: 0,
    1000: 0,
    2000: 0,
    4000: 0,
    8000: 0,
  };

  const [leftHL, setLeftHL] = useState(defaultHL);
  const [rightHL, setRightHL] = useState(defaultHL);

  const updateLeftHL = (freq, value) =>
    setLeftHL((prev) => ({ ...prev, [freq]: value }));

  const updateRightHL = (freq, value) =>
    setRightHL((prev) => ({ ...prev, [freq]: value }));

  // Tuning Gain
  const [tuningGain, setTuningGain] = useState(50);

  // -----------------------------
  // UPLOAD AUDIO → BACKEND PROCESS
  // -----------------------------
  const handleAudioUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setIsExportable(false);

    setAudioSrc(URL.createObjectURL(file));

    const formData = new FormData();
    formData.append("file", file);

    const hearingLossData = {
      left: leftHL,
      right: rightHL,
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "x-hearing-loss": JSON.stringify(hearingLossData),
            "x-tuning-gain": tuningGain,
          },
        }
      );

      const processedPath = response.data.processed_file;

      // Convert any slash format
      const fileName = processedPath
        .replace("processed/", "")
        .replace("\\processed\\", "")
        .split(/[/\\]/)
        .pop();

      setProcessedFileName(fileName);
      setEnhancedAudio(`http://127.0.0.1:5000/download/${fileName}`);
      setIsExportable(true);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setUploading(false);
    }
  };

  // -----------------------------
  // DOWNLOAD FINAL AUDIO
  // -----------------------------
  const handleDownload = async () => {
    if (!processedFileName) return;

    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/download/${processedFileName}`,
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], {
        type: `audio/${selectedFormat}`,
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", `enhancedAudio.${selectedFormat}`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error("Download failed:", err);
    }
  };

  return (
    <>
      <center>
        <h2 className={Style.intro}>
          Advanced Audio Enhancement System (AAES)
        </h2>
      </center>
      <div className={Style.mainWrapper}>
        {/* LEFT EAR */}
        <div className={Style.leftPanel}>
          <h3>Left Ear (dB HL)</h3>
          {Object.keys(leftHL).map((freq) => (
            <Slider
              key={freq}
              label={`${freq} Hz`}
              value={leftHL[freq]}
              min={0}
              max={80}
              step={1}
              onChange={(val) => updateLeftHL(freq, val)}
            />
          ))}
        </div>

        {/* CENTER SECTION */}
        <center className={Style.body1}>
          <div className={Style.audioContainer}>
            <div className={Style.tunningBox}>
              <h3>Tunning Gain (%)</h3>
              <Slider1
                label="Gain"
                value={tuningGain}
                min={50}
                max={85}
                step={1}
                onChange={setTuningGain}
              />
            </div>

            <div className={Style.box}>
              <h2>Original Audio</h2>
              <audio ref={audioRef1} src={audioSrc} controls></audio>
            </div>

            <div className={Style.box}>
              <h2>Enhanced Audio</h2>
              <audio ref={audioRef2} src={enhancedAudio} controls></audio>
            </div>
          </div>

          <input
            type="file"
            accept="audio/*"
            ref={fileInputRef}
            onChange={handleAudioUpload}
            style={{ display: "none" }}
          />

          <button
            className={Style.import}
            onClick={() => fileInputRef.current.click()}
            disabled={uploading}
          >
            {uploading ? "⏳ Uploading..." : "📂 Import"}
          </button>

          <div className={Style.exportContainer}>
            <label className={Style.ex}>
              <h2>Download as:</h2>
            </label>

            <select
              value={selectedFormat}
              onChange={(e) => setSelectedFormat(e.target.value)}
              disabled={!isExportable}
            >
              <option value="wav">WAV</option>
              <option value="mp3">MP3</option>
            </select>

            <button
              className={Style.export}
              onClick={handleDownload}
              disabled={!isExportable}
            >
              ⬇️ Export
            </button>
          </div>
        </center>

        {/* RIGHT EAR */}
        <div className={Style.rightPanel}>
          <h3>Right Ear (dB HL)</h3>
          {Object.keys(rightHL).map((freq) => (
            <Slider
              key={freq}
              label={`${freq} Hz`}
              value={rightHL[freq]}
              min={0}
              max={80}
              step={1}
              onChange={(val) => updateRightHL(freq, val)}
            />
          ))}
        </div>
      </div>
    </>
  );
}

export default Aaes;
