document.getElementById("generate").addEventListener("click", async () => {
  const sentence = "Did you sleep well?";
  const word = "sleep";

  try {
    const res = await fetch("/suggestions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sentence, word }),
    });

    if (!res.ok) {
      const txt = await res.text();
      console.error(`Server Error ${res.status}:\n`, txt);
      alert("Oops, something went wrong—check the console for details.");
      return;
    }

    const { suggestions } = await res.json();
    const list = document.getElementById("suggestions");
    list.innerHTML = "";

    suggestions.forEach(text => {
      const li = document.createElement("li");
      li.textContent = text;

      // Create the audio-play button
      const btn = document.createElement("button");
      btn.textContent = "🔊";
      btn.style.marginLeft = "0.5rem";
      btn.addEventListener("click", () => {
        const utter = new SpeechSynthesisUtterance(text);
        // Optionally pick a language or voice here:
        // utter.lang = 'en-US';
        window.speechSynthesis.speak(utter);
      });

      li.appendChild(btn);
      list.appendChild(li);
    });

  } catch (err) {
    console.error("Fetch failed:", err);
    alert("Network error—check your console.");
  }
});
