const socket = io();

const feedEl      = document.getElementById("live-feed");
const badge       = document.getElementById("fall-badge");
const statusDot   = document.getElementById("status-dot");
const streamStatus= document.getElementById("stream-status");
const fpsEl       = document.getElementById("fps-val");
const angleEl     = document.getElementById("angle-val");
const fallCountEl = document.getElementById("fall-count");
const uptimeEl    = document.getElementById("uptime-val");
const eventListEl = document.getElementById("event-list");
const eventBadge  = document.getElementById("event-badge");
const mFps        = document.getElementById("m-fps");
const mAngle      = document.getElementById("m-angle");
const mStatus     = document.getElementById("m-status");
const mPersons    = document.getElementById("m-persons");

let frameCount  = 0;
let lastFpsTime = Date.now();
let totalFalls  = 0;
let totalEvents = document.querySelectorAll(".event-item").length;
const startTime = Date.now();
const angleHistory = Array(80).fill(null);

// ── Uptime counter ──────────────────────────────────────
setInterval(() => {
  const s   = Math.floor((Date.now() - startTime) / 1000);
  const h   = Math.floor(s / 3600);
  const m   = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  uptimeEl.textContent = h > 0
    ? `${h}h ${m}m`
    : m > 0
    ? `${m}m ${sec}s`
    : `${sec}s`;
}, 1000);

// Update event badge
function updateEventBadge() {
  totalEvents++;
  eventBadge.textContent = totalEvents;
}

// ── Socket: live frame ──────────────────────────────────
socket.on("frame", data => {
  feedEl.src = "data:image/jpeg;base64," + data.img;
  statusDot.className = "brand-dot online";
  streamStatus.textContent = "Live";

  frameCount++;
  const now = Date.now();
  if (now - lastFpsTime >= 1000) {
    const fps = (frameCount * 1000 / (now - lastFpsTime)).toFixed(1);
    fpsEl.textContent  = fps;
    mFps.textContent   = fps;
    frameCount  = 0;
    lastFpsTime = now;
  }
});

// ── Socket: events ──────────────────────────────────────
socket.on("event", data => {
  const isFall = data.status && data.status.includes("fall");

  // Update angle display
  if (data.angle !== undefined && data.angle !== null) {
    const a = parseFloat(data.angle).toFixed(1);
    angleEl.textContent  = a + "°";
    mAngle.textContent   = a + "°";
    angleHistory.shift();
    angleHistory.push(parseFloat(data.angle));
    drawAngleChart();
  }

  // Update status
  if (data.status) {
    mStatus.textContent = data.status.replace("_", " ");
    mStatus.style.color = isFall ? "var(--danger)" : "var(--accent)";
  }

  // Fall alert
  if (isFall) {
    badge.classList.add("visible");
    statusDot.className = "brand-dot danger";
    totalFalls++;
    fallCountEl.textContent = totalFalls;
    // auto-clear badge after 6s
    setTimeout(() => {
      badge.classList.remove("visible");
      statusDot.className = "brand-dot online";
    }, 6000);
  }

  // Prepend event to list
  const li = document.createElement("li");
  li.className = "event-item" + (isFall ? " event-fall" : "");
  const ts = new Date().toISOString().slice(0, 19).replace("T", " ");
  const angleStr = (data.angle !== undefined && data.angle !== null)
    ? `<span class="event-angle">${parseFloat(data.angle).toFixed(1)}°</span>`
    : "";
  li.innerHTML = `
    <span class="event-ts">${ts}</span>
    <span class="event-label">${(data.status || "").replace("_", " ")}</span>
    ${angleStr}
  `;
  eventListEl.prepend(li);
  if (eventListEl.children.length > 150) {
    eventListEl.lastChild.remove();
  }
  updateEventBadge();
});

// ── Socket: connection state ────────────────────────────
socket.on("connect", () => {
  statusDot.className   = "brand-dot online";
  streamStatus.textContent = "Connected";
});
socket.on("disconnect", () => {
  statusDot.className   = "brand-dot";
  streamStatus.textContent = "Disconnected";
});

// ── Angle chart ─────────────────────────────────────────
function drawAngleChart() {
  const canvas = document.getElementById("angle-chart");
  const ctx    = canvas.getContext("2d");
  const W      = canvas.offsetWidth;
  const H      = 90;
  canvas.width  = W;
  canvas.height = H;

  ctx.clearRect(0, 0, W, H);

  // Threshold line at 60°
  const threshY = H - (60 / 90 * H);
  ctx.strokeStyle = "rgba(255,59,59,0.35)";
  ctx.lineWidth   = 1;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(0, threshY);
  ctx.lineTo(W, threshY);
  ctx.stroke();
  ctx.setLineDash([]);

  // Angle line
  ctx.strokeStyle = "#00e5a0";
  ctx.lineWidth   = 1.5;
  ctx.lineJoin    = "round";
  ctx.beginPath();
  let started = false;
  angleHistory.forEach((v, i) => {
    if (v === null) return;
    const x = (i / (angleHistory.length - 1)) * W;
    const y = H - Math.min(v / 90, 1) * H;
    if (!started) { ctx.moveTo(x, y); started = true; }
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Fill under line
  ctx.strokeStyle = "transparent";
  ctx.fillStyle   = "rgba(0,229,160,0.06)";
  ctx.lineTo(W, H);
  ctx.lineTo(0, H);
  ctx.closePath();
  ctx.fill();
}

// Initial chart draw
drawAngleChart();

