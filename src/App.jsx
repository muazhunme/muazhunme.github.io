import { useState } from "react";

const projects = [
  {
    code: "P01",
    title: "Data Project",
    type: "Analytics / Python",
    description:
      "A future case study for cleaning, modelling, and turning messy data into useful decisions.",
    status: "Placeholder",
  },
  {
    code: "P02",
    title: "Web App",
    type: "React / Full Stack",
    description:
      "A polished project slot for a real application, live demo, GitHub repository, and build notes.",
    status: "Coming soon",
  },
  {
    code: "P03",
    title: "Automation Tool",
    type: "Software / Workflow",
    description:
      "A space for tools that save time, connect systems, or make repetitive work feel lighter.",
    status: "Queued",
  },
];

const games = ["Browser game", "Puzzle demo", "Interactive prototype", "Creative experiment"];

const skills = [
  "React",
  "JavaScript",
  "Python",
  "SQL",
  "Data analysis",
  "Three.js",
  "Creative tech",
  "GitHub",
];

function App() {
  const [view, setView] = useState("home");
  const isHome = view === "home";

  const showView = (nextView) => {
    setView(nextView);
    window.scrollTo({ top: 0 });
  };

  return (
    <div className="site-shell">
      <div className="scanline" />
      <header className="nav">
        <button
          className="brand nav-button"
          type="button"
          onClick={() => showView("home")}
          aria-label="Muaz home"
        >
          <span className="brand-mark">MK</span>
          <span>Muaz Khan</span>
        </button>
        <nav className="nav-links" aria-label="Main navigation">
          <button type="button" onClick={() => showView("projects")}>
            Projects
          </button>
          <button type="button" onClick={() => showView("games")}>
            Experiments
          </button>
          <button type="button" onClick={() => showView("about")}>
            About
          </button>
          <button type="button" onClick={() => showView("contact")}>
            Contact
          </button>
        </nav>
      </header>

      <main>
        {isHome && (
          <>
            <section className="hero">
              <div className="hero-copy">
                <p className="eyebrow">
                  Hi, I am Muaz
                </p>
                <h1 className="hero-title">
                  I am a software developer
                </h1>
                <p className="hero-text">
                  I build software, data projects, and interactive web
                  experiences. This portfolio will collect my projects, games,
                  and resume in one polished place.
                </p>
                <div className="hero-actions">
                  <button
                    className="button button-primary"
                    type="button"
                    onClick={() => showView("projects")}
                  >
                    View my projects
                  </button>
                </div>
              </div>
              <div className="hero-art">
                <div className="art-ring art-ring-one" />
                <img
                  src="/muaz-cartoon-portrait.webp"
                  alt="Cartoon portrait of Muaz Khan"
                  width="1100"
                  height="1100"
                />
              </div>
            </section>

          </>
        )}

        {view === "projects" && (
          <section className="page-view">
            <div className="section-heading">
              <p className="eyebrow">Featured work</p>
              <h2>Project slots ready for real case studies.</h2>
            </div>
            <div className="project-grid">
              {projects.map((project) => (
                <article
                  className="project-card"
                  key={project.code}
                >
                  <div className="card-topline">
                    <span>{project.code}</span>
                    <span>{project.status}</span>
                  </div>
                  <h3>{project.title}</h3>
                  <p className="project-type">{project.type}</p>
                  <p>{project.description}</p>
                </article>
              ))}
            </div>
          </section>
        )}

        {view === "games" && (
          <section className="page-view section-split">
            <div className="section-heading">
              <p className="eyebrow">Game shelf</p>
              <h2>Games and experiments will live here.</h2>
              <p>
                These placeholders will later become playable demos, GitHub
                links, build notes, and short clips.
              </p>
            </div>
            <div className="game-list">
              {games.map((game, index) => (
                <div
                  className="game-tile"
                  key={game}
                >
                  <span>0{index + 1}</span>
                  <strong>{game}</strong>
                </div>
              ))}
            </div>
          </section>
        )}

        {view === "about" && (
          <section className="page-view about-panel">
            <div>
              <h2>Software, data, and interactive ideas.</h2>
            </div>
            <p>
              This section will grow into a fuller resume profile once the final
              content is ready. For now it sets the tone: thoughtful
              engineering, clear presentation, and a site that feels alive
              without getting loud.
            </p>
            <div className="skill-grid">
              {skills.map((skill) => (
                <span key={skill}>{skill}</span>
              ))}
            </div>
          </section>
        )}

        {view === "contact" && (
          <section className="page-view contact-section">
            <h2>Ready for real projects, game embeds, and the resume file.</h2>
            <div className="contact-actions">
              <a className="button button-primary" href="mailto:7muazkhan@gmail.com">
                7muazkhan@gmail.com
              </a>
              <a className="button button-secondary" href="https://github.com/muazhunme">
                GitHub profile
              </a>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
