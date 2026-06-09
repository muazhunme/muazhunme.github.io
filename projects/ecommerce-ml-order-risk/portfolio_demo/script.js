const fields = {
  delay: document.getElementById("delay"),
  sellerRisk: document.getElementById("sellerRisk"),
  categoryRisk: document.getElementById("categoryRisk"),
  itemCount: document.getElementById("itemCount"),
};

const labels = {
  delay: document.getElementById("delayValue"),
  sellerRisk: document.getElementById("sellerRiskValue"),
  categoryRisk: document.getElementById("categoryRiskValue"),
  itemCount: document.getElementById("itemCountValue"),
};

const riskScore = document.getElementById("riskScore");
const riskBand = document.getElementById("riskBand");
const riskReason = document.getElementById("riskReason");
const riskFill = document.getElementById("riskFill");
const resetButton = document.getElementById("resetButton");

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function getBand(score) {
  if (score >= 0.8) return ["Critical risk", "critical"];
  if (score >= 0.6) return ["High risk", "high"];
  if (score >= 0.3) return ["Medium risk", "medium"];
  return ["Low risk", "low"];
}

function getReasons(delay, sellerRisk, categoryRisk, itemCount) {
  const reasons = [];

  if (delay > 0) reasons.push("delivery is delayed");
  if (delay > 14) reasons.push("delivery delay is severe");
  if (sellerRisk >= 20) reasons.push("seller has an elevated bad-review history");
  if (categoryRisk >= 18) reasons.push("category has higher customer-experience risk");
  if (itemCount >= 3) reasons.push("multi-item order adds operational complexity");

  if (!reasons.length) {
    return "This order has no single extreme risk driver, so it would usually stay in normal monitoring.";
  }

  return `${reasons.slice(0, 3).join(", ")}.`;
}

function updateDemo() {
  const delay = Number(fields.delay.value);
  const sellerRisk = Number(fields.sellerRisk.value);
  const categoryRisk = Number(fields.categoryRisk.value);
  const itemCount = Number(fields.itemCount.value);

  labels.delay.textContent = String(delay);
  labels.sellerRisk.textContent = `${sellerRisk}%`;
  labels.categoryRisk.textContent = `${categoryRisk}%`;
  labels.itemCount.textContent = String(itemCount);

  const delayScore = (delay + 10) / 35;
  const sellerScore = sellerRisk / 40;
  const categoryScore = categoryRisk / 35;
  const itemScore = (itemCount - 1) / 5;
  const score = clamp(
    0.08 + delayScore * 0.32 + sellerScore * 0.31 + categoryScore * 0.22 + itemScore * 0.07,
    0.03,
    0.98
  );

  const [bandText, bandClass] = getBand(score);
  riskScore.textContent = score.toFixed(2);
  riskFill.style.width = `${Math.round(score * 100)}%`;
  riskBand.textContent = bandText;
  riskBand.className = `risk-band ${bandClass}`;
  riskReason.textContent = getReasons(delay, sellerRisk, categoryRisk, itemCount);
}

function resetDemo() {
  fields.delay.value = 6;
  fields.sellerRisk.value = 22;
  fields.categoryRisk.value = 17;
  fields.itemCount.value = 2;
  updateDemo();
}

Object.values(fields).forEach((field) => {
  field.addEventListener("input", updateDemo);
});

resetButton.addEventListener("click", resetDemo);
updateDemo();
