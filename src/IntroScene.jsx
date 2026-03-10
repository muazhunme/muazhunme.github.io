import { useEffect, useState } from "react";
import "./IntroScene.css";

export default function IntroScene() {
  const [stage, setStage] = useState("lights");
  const [activeLights, setActiveLights] = useState(0);

  useEffect(() => {
    const timers = [];
    const lightTimes = [700, 1500, 2300, 3100, 3900];

    lightTimes.forEach((time, index) => {
      timers.push(
        setTimeout(() => {
          setActiveLights(index + 1);
        }, time)
      );
    });

    timers.push(
      setTimeout(() => {
        setActiveLights(0);
        setStage("race");
      }, 4900)
    );

    timers.push(
      setTimeout(() => {
        setStage("message");
      }, 6100)
    );

    return () => timers.forEach(clearTimeout);
  }, []);

  const handleEnter = () => {
    if (stage !== "message") return;

    setStage("enter");

    setTimeout(() => {
      setStage("done");
    }, 1150);
  };

  if (stage === "done") return null;

  return (
    <div className={`intro-scene intro-scene--${stage}`}>
      <div className="intro-scene__bg" />
      <div className="intro-scene__vignette" />

      {(stage === "lights" || stage === "race") && (
        <div className="gantry-wrap">
          <div className="gantry">
            <div className="gantry__top" />
            <div className="gantry__row">
              {[0, 1, 2, 3, 4].map((i) => (
                <div className="gantry__col" key={i}>
                  <div
                    className={`gantry__light ${
                      activeLights > i ? "is-on" : ""
                    }`}
                  />
                  <div
                    className={`gantry__light ${
                      activeLights > i ? "is-on" : ""
                    }`}
                  />
                </div>
              ))}
            </div>
            <div className="gantry__base" />
          </div>
        </div>
      )}

      {(stage === "race" || stage === "message" || stage === "enter") && (
        <div className="race-layer">
          <div className="track-lines">
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>
        </div>
      )}

      {(stage === "message" || stage === "enter") && (
        <div className="intro-copy">
          <h1 className="lights-out-text">LIGHTS OUT</h1>

          <button
            type="button"
            className="begin-button"
            onClick={handleEnter}
          >
            <span className="begin-button__glow" />
            <span className="begin-button__beam" />
            <span className="begin-button__beamline" />
            <span className="begin-button__inner">let’s begin</span>
          </button>
        </div>
      )}

      {stage === "enter" && (
        <div className="reveal-transition">
          <div className="reveal-transition__shine" />
          <div className="reveal-transition__bar" />
        </div>
      )}
    </div>
  );
}