function App() {
  return (
    <>
      <header className="navbar">
        <div className="nav-logo">MK</div>

        <nav className="nav-links">
          <a href="#about">About</a>
          <a href="#projects">Projects</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main>
        <section className="hero">
          <div className="hero-content">
            <p className="eyebrow">Data Science • Software • Portfolio</p>
            <h1>Hi, I’m Muaz Khan</h1>
            <p className="hero-text">
              I’m an IT student focused on data science, software, and building
              practical projects that solve real problems.
            </p>

            <div className="hero-buttons">
              <a href="#projects" className="btn btn-primary">
                View Projects
              </a>
              <a href="#contact" className="btn btn-secondary">
                Contact Me
              </a>
            </div>
          </div>
        </section>

        <section id="about" className="section">
          <div className="section-container">
            <p className="section-label">About</p>
            <h2>Building practical skills in data and software</h2>
            <p className="section-text">
              I am currently studying IT with a focus on data science and enjoy
              working on projects involving Python, SQL, analytics, and web
              development. My goal is to create useful, well-designed solutions
              while continuing to grow as a developer.
            </p>

            <div className="about-grid">
              <div className="info-card">
                <h3>Education</h3>
                <p>Bachelor of IT – Data Science</p>
                <p>Macquarie University</p>
              </div>

              <div className="info-card">
                <h3>Skills</h3>
                <p>Python, SQL, R, React, Data Analysis</p>
              </div>

              <div className="info-card">
                <h3>Interests</h3>
                <p>AI, dashboards, software projects, sports analytics</p>
              </div>
            </div>
          </div>
        </section>

        <section id="projects" className="section">
          <div className="section-container">
            <p className="section-label">Projects</p>
            <h2>Some things I’ve worked on</h2>
            <p className="section-text">
              Here are a few example projects that show my interest in data,
              software, and solving practical problems.
            </p>

            <div className="projects-grid">
              <article className="project-card">
                <p className="project-type">Data Science</p>
                <h3>Airbnb Price Prediction</h3>
                <p>
                  Built regression models to predict Airbnb listing prices using
                  data cleaning, feature selection, and model evaluation.
                </p>
                <div className="project-tags">
                  <span>Python</span>
                  <span>Pandas</span>
                  <span>Scikit-learn</span>
                </div>
              </article>

              <article className="project-card">
                <p className="project-type">Web / Software</p>
                <h3>Portfolio Website</h3>
                <p>
                  Developed a personal website in React to showcase projects,
                  skills, and experience in a clean and modern design.
                </p>
                <div className="project-tags">
                  <span>React</span>
                  <span>CSS</span>
                  <span>Vite</span>
                </div>
              </article>

              <article className="project-card">
                <p className="project-type">Database</p>
                <h3>SQL Business Database</h3>
                <p>
                  Designed and queried a relational database with business rules,
                  structured tables, and practical SQL operations.
                </p>
                <div className="project-tags">
                  <span>SQL</span>
                  <span>MySQL</span>
                  <span>ERD</span>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section id="contact" className="section">
          <div className="section-container">
            <p className="section-label">Contact</p>
            <h2>Let’s connect</h2>
            <p className="section-text">
              You can reach me for internships, collaborations, or project
              opportunities.
            </p>

            <div className="contact-box">
              <p>Email: 7muazkhan@gmail.com</p>
              <p>Location: Sydney, Australia</p>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}

export default App;