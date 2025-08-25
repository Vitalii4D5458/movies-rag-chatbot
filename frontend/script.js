const btn = document.getElementById("ask");
const txt = document.getElementById("q");
const out = document.getElementById("out");
const retr = document.getElementById("retr");
const statusEl = document.getElementById("status");

async function ask() {
  const query = txt.value.trim();
  if (!query) return;
  btn.disabled = true;
  statusEl.textContent = "Запит...";
  out.textContent = "";
  retr.textContent = "";

  try {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Server error");
    out.textContent = data.answer;
    const items = data.retrieved || [];
    if (items.length) {
      const list = items
        .map((d) => {
          const year = d.year ? ` (${d.year})` : "";
          const g = d.genres ? ` • ${d.genres.join(", ")}` : "";
          return `• ${d.title}${year}${g}`;
        })
        .join("\n");
      retr.textContent = "Знайдені релевантні:\n" + list;
    }
    statusEl.textContent = data.used_llm ? "LLM" : "Без LLM";
  } catch (e) {
    out.textContent = "Помилка: " + e.message;
    statusEl.textContent = "Помилка";
  } finally {
    btn.disabled = false;
  }
}

btn.addEventListener("click", ask);
txt.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) ask();
});
