import styles from './Rp.module.css';

const researchPapers = [
  { title: "Research Paper 1: MMSE (noise reduction)", url: "https://ieeexplore.ieee.org/document/6554705" },
  { title: "Research Paper 2: LMS (dsp,noise/error)", url: "https://www.academia.edu/download/82056394/a265103-1050.pdf" },
  { title: "Research Paper 3: STFT (dsp)", url: "https://ieeexplore.ieee.org/abstract/document/7009929" },
  { title: "Research Paper 4: L-filter (filter,dsp)", url: "https://ieeexplore.ieee.org/abstract/document/8301696/" },
  { title: "Research Paper 5: Tuning (channel,dB gain)", url: "https://link.springer.com/article/10.1007/s10772-019-09599-5" },
];

const Rp = () => {
  const openInNewTab = (url) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className={styles.container}>
      <div className={styles.paperBox}>
        <h1 className={styles.title}>Research Papers for References</h1>
        <p className={styles.subtitle}>Browse and read the IEEE research papers:</p>
        <ul className={styles.papersList}>
          {researchPapers.map((paper, index) => (
            <li key={index}>
              <span
                className={styles.paperLink}
                onClick={() => openInNewTab(paper.url)}
                style={{ cursor: 'pointer', color: '#0072ff', textDecoration: 'underline' }}
              >
                {paper.title}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Rp;
