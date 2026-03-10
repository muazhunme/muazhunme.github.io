import { useMemo, useState } from "react";

const COLORS = [
  "#ffffff",
  "#e5e7eb",
  "#cbd5e1",
  "#94a3b8",
  "#7dd3fc",
  "#93c5fd",
  "#a5b4fc",
  "#fde68a",
  "#fcd34d",
  "#86efac",
  "#5eead4",
  "#67e8f9",
  "#ffffff",
  "#00f5ff",
  "#00e5ff",
  "#22d3ee",
  "#38bdf8",
  "#3b82f6",
  "#60a5fa",
  "#818cf8",
  "#8b5cf6",
  "#a855f7",
  "#c084fc",
  "#e879f9",
  "#ff4dff",
  "#f472b6",
  "#fb7185",
  "#facc15",
  "#a3e635",
  "#4ade80",
  "#00ffff",
  "#7df9ff",
  "#00eaff",
  "#00bfff",
  "#1e90ff",
  "#7b61ff",
  "#9d4edd",
  "#ff00ff",
  "#ff4fd8",
  "#ff4d6d",
  "#ff6b00",
  "#ffd60a",
  "#b8ff00",
  "#39ff14",
  "#00ff85",
  "#c4b5fd",
  "#a5b4fc",
  "#99f6e4",
  "#86efac",
  "#fde68a",
  "#fdba74",
  "#cbd5e1",
  "#94a3b8",
  "#64748b",
  "#475569",
  "#7dd3fc",
  "#93c5fd"
 
];

const FONTS = [
  "Inter, Arial, sans-serif",
  "Georgia, serif",
  "'Trebuchet MS', sans-serif",
  "'Courier New', monospace",
  "'Times New Roman', serif",
  "Verdana, sans-serif",
  "'Helvetica Neue', Helvetica, Arial, sans-serif",
  "Tahoma, sans-serif",
  "'Lucida Sans Unicode', 'Lucida Grande', sans-serif",
  "'Palatino Linotype', 'Book Antiqua', Palatino, serif",
  "Garamond, serif",
  "'Bookman Old Style', serif",
  "'Arial Black', Gadget, sans-serif",
  "'Comic Sans MS', cursive, sans-serif",
  "Impact, Charcoal, sans-serif",
  "'Lucida Console', Monaco, monospace",
  "'Courier Prime', 'Courier New', monospace",
  "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  "'Gill Sans', 'Gill Sans MT', Calibri, sans-serif",
  "'Optima', sans-serif",
  "'Candara', sans-serif",
  "'Geneva', sans-serif",
  "'Baskerville', serif",
  "'Cambria', serif",
  "'Didot', serif",
  "'American Typewriter', serif",
  "'Andale Mono', monospace",
  "'Monaco', monospace",
  "'Brush Script MT', cursive",
  "'Copperplate', fantasy"
];

const WEIGHTS = [400, 500, 600];

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function makeStyle() {
  const useGradient = Math.random() > 0.9;

  return {
    color: useGradient ? "transparent" : randomItem(COLORS),
    fontFamily: randomItem(FONTS),
    fontWeight: randomItem(WEIGHTS),
    transform: `rotate(${Math.random() * 8 - 4}deg) translateY(${Math.random() * 2 - 1}px)`,
    textShadow:
      Math.random() > 0.6
        ? `0 0 8px ${randomItem(COLORS)}55`
        : "none",
    backgroundImage: useGradient
      ? `linear-gradient(135deg, ${randomItem(COLORS)}, ${randomItem(COLORS)})`
      : "none",
    WebkitBackgroundClip: useGradient ? "text" : "border-box",
    backgroundClip: useGradient ? "text" : "border-box",
    WebkitTextFillColor: useGradient ? "transparent" : "currentColor",
    opacity: 1,
    fontStyle: Math.random() > 0.88 ? "italic" : "normal",
  };
}

export default function HoverText({ text, as: Tag = "span", className = "" }) {
  const initialLetters = useMemo(
    () =>
      text.split("").map((char, index) => ({
        id: index,
        char,
        style: {},
      })),
    [text]
  );

  const [letters, setLetters] = useState(initialLetters);

  const handleLetterHover = (index) => {
    setLetters((prev) =>
      prev.map((letter, i) =>
        i === index && letter.char !== " "
          ? { ...letter, style: makeStyle() }
          : letter
      )
    );
  };

  return (
    <Tag className={`hover-text-wrap ${className}`}>
      {letters.map((letter) =>
        letter.char === " " ? (
          <span key={letter.id} className="hover-letter-space">
            {" "}
          </span>
        ) : (
          <span
            key={letter.id}
            className="hover-letter"
            style={letter.style}
            onMouseEnter={() => handleLetterHover(letter.id)}
          >
            {letter.char}
          </span>
        )
      )}
    </Tag>
  );
}