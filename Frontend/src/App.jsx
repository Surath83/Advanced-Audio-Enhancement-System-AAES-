import Style from "./App.module.css";
import Navbar from './Navbar';
import Aaes from './Aaes';
import Rp from './Rp';
import Contact from './Contact';

function App() {
  return (
    <>
      <div className={Style.bb}>
        <Navbar />
        <section id="AAES" className={Style.section}>
          <div className={Style.aaes}>
            <Aaes />
          </div>
        </section>
        
        <section id="research" className={Style.section}>
          <Rp />
        </section>

        <section id="contact" className={Style.section}>
          <Contact />
        </section>
      </div>

      <footer className={Style.member}>
        <p>© Copyright Reserved 2025</p>
      </footer>
    </>
  );
}

export default App;
