import styles from "./Contact.module.css";

function Contact() {
  return (
    <><div className={styles.container}>
      <h1 className={styles.heading}>About Us</h1>
      <div className={styles.teamSection}>
        <div className={styles.member}>
          <h2>Description</h2>
          <h3><b>AAES</b> is a digital signal processing (DSP) based solution designed to enhance audio quality by reducing noise, improving stereo separation, and optimizing frequency balance. Built with a React frontend and a Python backend, AAES offers a seamless and efficient user experience. The system leverages advanced algorithms for real-time audio enhancement, making it suitable for various applications like music streaming, VoIP communication, gaming, and assistive technologies.</h3>
        </div>
        <div>
          <div className={styles.member}>
      <h2 className="title">Tech Stack</h2>
      <div className="category">
        <h3>Frontend</h3>
        <p>React, CSS, HTML</p>
      </div>
      <div className="category">
        <h3>Backend</h3>
        <p>Flask / FastAPI – API & Request Handling</p>
      </div>
      <div className="category">
        <h3>Audio Processing</h3>
        <p>
          NumPy, SciPy – Signal Processing <br />
          PyDub – Format Conversion & Manipulation <br />
          FFmpeg – Encoding / Decoding <br />
          Librosa – Feature Extraction <br />
          NoiseReduce – LMS Filter & MMSE Filter <br />
          Soundfile – WAV / FLAC I/O
        </p>
      </div>
    </div>
        </div>
        <div className={styles.member}>
          <h2>Team members</h2>
          <h3>Sameer Kumar Choudhury</h3>
          <p>Email: sameer133@gmail.com</p>
          <h3>Sneha Mal</h3>
          <p>Email: snehamal@gmail.com</p>
          <h3>Shristi Priya</h3>
          <p>Email: shristipriya@gmail.com</p>
          <h3>Surath Choudhury</h3>
          <p>Email: surath172003@gmail.com</p>
        </div>
        
      </div>
    </div>
    </>
  );
}

export default Contact;
