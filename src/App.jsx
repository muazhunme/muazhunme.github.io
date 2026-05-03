import { Float, MeshTransmissionMaterial, Stars, Text } from "@react-three/drei";
import { Canvas, useFrame } from "@react-three/fiber";
import { motion as Motion } from "framer-motion";
import { useRef } from "react";

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

const games = [
  "Arcade prototype",
  "Browser game",
  "3D experiment",
  "Interactive demo",
];

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

function ArcadeCore() {
  const group = useRef(null);
  const coin = useRef(null);

  useFrame((state) => {
    const t = state.clock.getElapsedTime();

    if (group.current) {
      group.current.rotation.y = Math.sin(t * 0.45) * 0.26;
      group.current.rotation.x = Math.sin(t * 0.32) * 0.08;
    }

    if (coin.current) {
      coin.current.rotation.y = t * 1.4;
      coin.current.position.y = Math.sin(t * 1.8) * 0.12 + 0.5;
    }
  });

  return (
    <>
      <color attach="background" args={["#05070d"]} />
      <ambientLight intensity={0.7} />
      <pointLight position={[3.2, 2.8, 4]} intensity={7} color="#00d9ff" />
      <pointLight position={[-3.5, -1, 3]} intensity={5} color="#ff3d9a" />
      <spotLight
        position={[0, 4.2, 3]}
        angle={0.42}
        penumbra={0.75}
        intensity={7}
        color="#fff0a6"
      />
      <Stars radius={80} depth={38} count={900} factor={3} fade speed={0.45} />

      <group ref={group} position={[0, -0.1, 0]}>
        <Float speed={1.8} rotationIntensity={0.18} floatIntensity={0.35}>
          <mesh position={[0, 0, 0]} rotation={[0.08, -0.18, 0]}>
            <boxGeometry args={[2.8, 2.2, 0.34]} />
            <MeshTransmissionMaterial
              backside
              thickness={0.28}
              chromaticAberration={0.08}
              anisotropy={0.28}
              distortion={0.18}
              distortionScale={0.34}
              temporalDistortion={0.1}
              color="#3cecff"
              roughness={0.12}
              transmission={0.28}
            />
          </mesh>
          <mesh position={[0, 0, 0.22]}>
            <boxGeometry args={[2.25, 1.36, 0.08]} />
            <meshStandardMaterial color="#09101c" emissive="#12345a" emissiveIntensity={0.6} />
          </mesh>
          <mesh position={[-0.8, -0.94, 0.25]}>
            <cylinderGeometry args={[0.14, 0.14, 0.08, 32]} />
            <meshStandardMaterial color="#ff3d9a" emissive="#ff3d9a" emissiveIntensity={1.8} />
          </mesh>
          <mesh position={[-0.42, -0.94, 0.25]}>
            <cylinderGeometry args={[0.14, 0.14, 0.08, 32]} />
            <meshStandardMaterial color="#ffe66d" emissive="#ffcc2f" emissiveIntensity={1.4} />
          </mesh>
          <mesh position={[0.64, -0.94, 0.25]}>
            <boxGeometry args={[0.72, 0.12, 0.08]} />
            <meshStandardMaterial color="#00f0ff" emissive="#00d9ff" emissiveIntensity={1.6} />
          </mesh>
          <Text
            position={[0, 0.22, 0.31]}
            fontSize={0.22}
            letterSpacing={0.08}
            anchorX="center"
            anchorY="middle"
            color="#e8fbff"
          >
            MUAZ.EXE
          </Text>
          <Text
            position={[0, -0.12, 0.31]}
            fontSize={0.105}
            letterSpacing={0.04}
            anchorX="center"
            anchorY="middle"
            color="#7ff7ff"
          >
            PORTFOLIO SYSTEM ONLINE
          </Text>
        </Float>

        <mesh ref={coin} position={[1.78, 0.5, 0.2]}>
          <cylinderGeometry args={[0.34, 0.34, 0.08, 44]} />
          <meshStandardMaterial color="#ffe66d" emissive="#d69d00" emissiveIntensity={0.9} />
        </mesh>
      </group>
    </>
  );
}

function App() {
  return (
    <div className="site-shell">
      <div className="scanline" />
      <header className="nav">
        <a className="brand" href="#top" aria-label="Muaz home">
          <span className="brand-mark">MK</span>
          <span>Muaz Khan</span>
        </a>
        <nav className="nav-links" aria-label="Main navigation">
          <a href="#projects">Projects</a>
          <a href="#games">Games</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <Motion.p
              className="eyebrow"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              Data science / software / creative tech
            </Motion.p>
            <Motion.h1
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.65, delay: 0.08 }}
            >
              Arcade-inspired portfolio, built with a professional edge.
            </Motion.h1>
            <Motion.p
              className="hero-text"
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.65, delay: 0.16 }}
            >
              I am Muaz Khan, an IT student in Sydney building software, data
              projects, and interactive web experiences. This space will become
              the playable map of my projects, games, and resume.
            </Motion.p>
            <Motion.div
              className="hero-actions"
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.65, delay: 0.24 }}
            >
              <a className="button button-primary" href="#projects">
                View projects
              </a>
              <a className="button button-secondary" href="#games">
                Enter arcade
              </a>
            </Motion.div>
          </div>

          <Motion.div
            className="hero-stage"
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.12 }}
          >
            <Canvas
              camera={{ position: [0, 0.2, 5.1], fov: 42 }}
              dpr={[1, 1.6]}
              gl={{ antialias: true, alpha: false }}
            >
              <ArcadeCore />
            </Canvas>
          </Motion.div>
        </section>

        <section className="status-strip" aria-label="Portfolio status">
          <span>Portfolio build: redesign branch</span>
          <span>Resume: placeholder</span>
          <span>Projects: placeholders</span>
          <span>Games: coming soon</span>
        </section>

        <section id="projects" className="section">
          <div className="section-heading">
            <p className="eyebrow">Featured work</p>
            <h2>Project slots ready for real case studies.</h2>
          </div>
          <div className="project-grid">
            {projects.map((project) => (
              <Motion.article
                className="project-card"
                key={project.code}
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.4 }}
                transition={{ duration: 0.5 }}
              >
                <div className="card-topline">
                  <span>{project.code}</span>
                  <span>{project.status}</span>
                </div>
                <h3>{project.title}</h3>
                <p className="project-type">{project.type}</p>
                <p>{project.description}</p>
              </Motion.article>
            ))}
          </div>
        </section>

        <section id="games" className="section section-split">
          <div className="section-heading">
            <p className="eyebrow">Game shelf</p>
            <h2>A clean arcade wall for future playable work.</h2>
            <p>
              These placeholders will later become playable demos, GitHub links,
              build notes, and short clips. The layout is ready for games without
              making the whole portfolio feel childish.
            </p>
          </div>
          <div className="game-list">
            {games.map((game, index) => (
              <Motion.div
                className="game-tile"
                key={game}
                initial={{ opacity: 0, x: 18 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, amount: 0.5 }}
                transition={{ duration: 0.45, delay: index * 0.05 }}
              >
                <span>0{index + 1}</span>
                <strong>{game}</strong>
              </Motion.div>
            ))}
          </div>
        </section>

        <section id="about" className="section about-panel">
          <div>
            <p className="eyebrow">Player profile</p>
            <h2>Software, data, and interactive ideas.</h2>
          </div>
          <p>
            This section will grow into a fuller resume profile once the final
            content is ready. For now it sets the tone: thoughtful engineering,
            clear presentation, and a site that feels alive without getting loud.
          </p>
          <div className="skill-grid">
            {skills.map((skill) => (
              <span key={skill}>{skill}</span>
            ))}
          </div>
        </section>

        <section id="contact" className="section contact-section">
          <p className="eyebrow">Continue</p>
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
      </main>
    </div>
  );
}

export default App;
