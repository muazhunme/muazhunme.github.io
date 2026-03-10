import { motion } from "framer-motion";
import HoverText from "./HoverText";

const fadeLeft = {
  hidden: { opacity: 0, x: -40 },
  show: { opacity: 1, x: 0, transition: { duration: 0.7, ease: "easeOut" } },
};

const fadeRight = {
  hidden: { opacity: 0, x: 40 },
  show: { opacity: 1, x: 0, transition: { duration: 0.8, ease: "easeOut" } },
};

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.7, ease: "easeOut" } },
};

function App() {
  return (
    <>
      <header className="navbar">
        <div className="nav-logo">MUAZ</div>

        <nav className="nav-links">
          <a href="#about">About</a>
          <a href="#work">Work</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main>
        <section className="hero-creative">
          <div className="hero-grid">
            <motion.div
              className="hero-left"
              initial="hidden"
              animate="show"
              variants={fadeLeft}
            >
              <p className="hero-kicker">DATA SCIENCE • SOFTWARE • CREATIVE TECH</p>

              <h1 className="hero-title">
                <HoverText
                  text="Building digital work that feels"
                  className="interactive-heading"
                  as="span"
                />
                <br />
                <HoverText
                  text="sharp, modern, and"
                  className="interactive-heading gradient-text"
                  as="span"
                />
                <br />
                <HoverText
                  text="alive."
                  className="interactive-heading gradient-text"
                  as="span"
                />
              </h1>

              <p className="hero-description">
                I’m Muaz Khan, an IT student focused on data science, software,
                analytics, and building projects that look good and solve real
                problems.
              </p>

              <div className="hero-actions">
                <a href="#work" className="btn btn-main">
                  Explore Work
                </a>
                <a href="#contact" className="btn btn-ghost">
                  Let’s Talk
                </a>
              </div>
            </motion.div>

            <motion.div
              className="hero-right"
              initial="hidden"
              animate="show"
              variants={fadeRight}
            >
              <div className="floating-card card-one">
                <p className="mini-label">FEATURED</p>
                <h3>
                  <HoverText
                    text="Portfolio System"
                    className="card-hover-title"
                    as="span"
                  />
                </h3>
                <p>
                  React-based personal website with motion, modern layout, and
                  interactive sections.
                </p>
              </div>

              <div className="floating-card card-two">
                <p className="mini-label">PROJECT</p>
                <h3>
                  <HoverText
                    text="Airbnb Prediction"
                    className="card-hover-title"
                    as="span"
                  />
                </h3>
                <p>
                  Data cleaning, feature engineering, regression modelling, and
                  evaluation workflow.
                </p>
              </div>

              <div className="floating-card card-three">
                <p className="mini-label">SKILLS</p>
                <h3>
                  <HoverText
                    text="Python • SQL • React"
                    className="card-hover-title"
                    as="span"
                  />
                </h3>
                <p>
                  Data analysis, dashboards, databases, and front-end
                  development.
                </p>
              </div>

              <div className="hero-orb orb-one"></div>
              <div className="hero-orb orb-two"></div>
            </motion.div>
          </div>
        </section>

        <section id="about" className="placeholder-section">
          <motion.div
            className="placeholder-content"
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
          >
            <p className="section-tag">About</p>
            <h2>
              <HoverText
                text="A more designed portfolio starts here."
                className="section-hover-title"
                as="span"
              />
            </h2>
            <p>
              Next we’ll turn this into a stronger portfolio with editorial
              sections, better project showcases, and richer interactions.
            </p>
          </motion.div>
        </section>

        <section id="work" className="placeholder-section alt">
          <motion.div
            className="placeholder-content"
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
          >
            <p className="section-tag">Work</p>
            <h2>
              <HoverText
                text="Projects should feel showcased, not listed."
                className="section-hover-title"
                as="span"
              />
            </h2>
            <p>
              The next stage is replacing simple cards with featured project
              panels, visual hierarchy, and real links.
            </p>
          </motion.div>
        </section>

        <section id="contact" className="placeholder-section">
          <motion.div
            className="placeholder-content"
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
          >
            <p className="section-tag">Contact</p>
            <h2>
              <HoverText
                text="7muazkhan@gmail.com"
                className="section-hover-title"
                as="span"
              />
            </h2>
            <p>Sydney, Australia</p>
          </motion.div>
        </section>
      </main>
    </>
  );
}

export default App;