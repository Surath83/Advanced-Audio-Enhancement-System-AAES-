import styles from './Rp.module.css';

const researchPapers = [
  { title: "Research Paper 1: DSP", url: "https://ieeexplore.ieee.org/document/1430249" },
  { title: "Research Paper 2: Filteration 1", url: "https://ieeexplore.ieee.org/document/10694208" },
  { title: "Research Paper 3: Filteration 2", url: "https://ieeexplore.ieee.org/document/9103036" },
  { title: "Research Paper 4: Noisereduction 1", url: "https://ieeexplore.ieee.org/document/10872040" },
  { title: "Research Paper 5: Noisereduction 2", url: "https://ieeexplore.ieee.org/document/10448279" },
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
