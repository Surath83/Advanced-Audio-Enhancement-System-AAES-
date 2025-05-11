import styles from './Navbar.module.css';

const Navbar = () => {
  return (
    <header className={styles.navbar}>
      <div className={styles.logo}>
        Advanced Audio Enhancement System
      </div>
      <nav aria-label="Main Navigation">
        <ul className={styles.navLinks}>
          <li>
            <a href="#AAES">AAES</a>
          </li>
          <li>
            <a href="#research">Research Papers</a>
          </li>
          <li>
            <a href="#contact">About Us</a>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
