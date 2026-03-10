import { useMemo, useState } from "react";

const COLORS = [
  "#ffffff",
  "#7dd3fc",
  "#c084fc",
  "#f9a8d4",
  "#86efac",
  "#fde68a",
  "#93c5fd",
];

const FONTS = [
  "Inter, Arial, sans-serif",
  "Georgia, serif",
  "'Trebuchet MS', sans-serif",
  "'Courier New', monospace",
  "'Times New Roman', serif",
  "Verdana, sans-serif",
];

const WEIGHTS = [400, 500, 600, 700, 800];

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