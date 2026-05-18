import { useState } from "react";

const projects = [
  {
    code: "P01",
    title: "AI-Powered Community Intelligence Dashboard",
    type: "Data Science / NLP / Business Intelligence",
    description:
      "A generalized analytics pipeline that turns community posts, comments, and user data into dashboard-ready CSVs and business insight reports.",
    tools: "Python, Pandas, NLP, Sentence-Transformers, VADER, KeyBERT",
    status: "In progress",
  },
  {
    code: "P02",
    title: "SaaS Churn Analysis Report",
    type: "Data Analysis",
    description:
      "A subscription business analysis focused on churn rate, cancelled users, retention patterns, customer lifetime value, and revenue risk.",
    tools: "Python, Pandas, SQL, Excel",
    status: "Demo project",
  },
  {
    code: "P03",
    title: "Customer Segmentation Analysis",
    type: "Data Science / Marketing Analytics",
    description:
      "A customer analytics project that groups customers by spending behaviour, purchase frequency, value, and marketing potential.",
    tools: "Python, Pandas, Scikit-learn, Excel",
    status: "Demo project",
  },
  {
    code: "P04",
    title: "Product Review Sentiment Analysis",
    type: "AI / NLP",
    description:
      "An NLP project that analyses customer reviews to identify sentiment, common complaints, praised features, and product improvement opportunities.",
    tools: "Python, NLP, VADER Sentiment, Pandas, Matplotlib",
    status: "Demo project",
  },
  {
    code: "P05",
    title: "CSV-to-Business-Insights Generator",
    type: "AI Automation",
    description:
      "A tool concept that takes a business CSV file, cleans basic issues, detects useful columns, creates summary charts, and generates plain-English insights.",
    tools: "Python, Pandas, Streamlit, AI-assisted analysis",
    status: "Demo project",
  },
];

const focusAreas = [
  {
    title: "Data Cleaning",
    description:
      "Clean messy Excel, CSV, CRM, ecommerce, subscription, and marketing datasets so they are ready for analysis and dashboards.",
    deliverables: "Cleaned dataset, data quality report, duplicate and missing value summary",
  },
  {
    title: "Dashboard Development",
    description:
      "Build clear Excel or Power BI-style dashboards for sales, ecommerce, SaaS, marketing, finance, and operations data.",
    deliverables: "KPI dashboard, interactive visuals, business summary",
  },
  {
    title: "Business Data Analysis",
    description:
      "Analyse business data to find trends, customer segments, churn patterns, product performance, and pricing insights.",
    deliverables: "Analysis report, charts, recommendations",
  },
  {
    title: "Customer Feedback & Sentiment Analysis",
    description:
      "Analyse reviews, surveys, support tickets, app store reviews, and social media comments to find sentiment, themes, complaints, and opportunities.",
    deliverables: "Sentiment report, theme breakdown, action recommendations",
  },
  {
    title: "AI Insight Generation",
    description:
      "Create simple tools or scripts that turn CSV files, reviews, or business data into automated summaries, charts, and insight reports.",
    deliverables: "Python script, Streamlit-style prototype, automated report output",
  },
];

const skills = [
  "Python",
  "SQL",
  "R",
  "React",
  "HTML/CSS",
  "JavaScript",
  "Excel",
  "Power BI",
  "Pandas",
  "NumPy",
  "Matplotlib",
  "Scikit-learn",
  "PyTorch",
  "Sentence-Transformers",
  "Transformers",
  "KeyBERT",
  "VADER Sentiment",
  "OpenPyXL",
  "Data cleaning",
  "Data validation",
  "Feature engineering",
  "Exploratory data analysis",
  "NLP",
  "Topic modelling",
  "Semantic embeddings",
  "Sentiment analysis",
  "Audience segmentation",
  "Dashboards",
  "Automated data pipelines",
  "Report automation",
  "AI-assisted analysis",
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
            Focus
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
                  <span className="title-line">Data</span>
                  <span className="title-line">science</span>
                  <span className="title-line developer-word">and AI insights</span>
                </h1>
                <p className="hero-text">
                  I am a Data Science-focused IT student building practical
                  analytics, dashboards, NLP systems, and AI-supported tools
                  that turn raw data into clear decisions.
                </p>
                <div className="hero-actions">
                  <button
                    className="button button-primary"
                    type="button"
                    onClick={() => showView("projects")}
                  >
                    View data projects
                  </button>
                </div>
              </div>
              <div className="hero-art" aria-label="Floating cartoon portrait of Muaz Khan">
                <img
                  className="hero-character"
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
              <h2>Data projects built around real business questions.</h2>
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
                  <p className="project-tools">{project.tools}</p>
                </article>
              ))}
            </div>
          </section>
        )}

        {view === "games" && (
          <section className="page-view section-split">
            <div className="section-heading">
              <p className="eyebrow">Focus areas</p>
              <h2>Data science skills I am building into real projects.</h2>
              <p>
                My work sits around practical analytics, dashboard-ready data,
                NLP, automated reporting, and AI-assisted decision support.
              </p>
            </div>
            <div className="game-list">
              {focusAreas.map((service, index) => (
                <div
                  className="game-tile"
                  key={service.title}
                >
                  <span>0{index + 1}</span>
                  <div>
                    <strong>{service.title}</strong>
                    <p>{service.description}</p>
                    <small>{service.deliverables}</small>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {view === "about" && (
          <section className="page-view about-panel">
            <div>
              <h2>Data science, analytics, and practical AI tools.</h2>
            </div>
            <p>
              I am Muaz Ahmad Khan, based in Sydney and studying a Bachelor of
              Information Technology in Data Science at Macquarie University.
              I work with Python, SQL, R, dashboards, NLP, machine learning,
              and automated reporting to turn raw data into clear,
              evidence-based insights.
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
            <h2>Want to talk data, dashboards, or AI projects?</h2>
            <p>
              I am interested in data science, analytics, business
              intelligence, NLP, dashboarding, and AI-supported decision-making
              opportunities.
            </p>
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
