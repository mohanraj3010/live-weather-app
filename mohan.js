onload = () => {
  const c = setTimeout(() => {
    document.body.classList.remove("not-loaded");
    clearTimeout(c);
  }, 1000);
};
const apiKey = "c987f0222775d9ef5e7d53f001b6113f"; 

async function getWeather() {
  const city = document.getElementById("cityInput").value;
  if (!city) return alert("Please enter a city");

  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
    );
    const data = await response.json();

    if (data.cod !== 200) {
      alert("City not found!");
      return;
    }

    document.getElementById("cityName").textContent = data.name;
    document.getElementById("temperature").textContent = `${data.main.temp}°C`;
    document.getElementById("description").textContent = data.weather[0].description;
    document.getElementById("humidity").textContent = `💧 Humidity: ${data.main.humidity}%`;
    document.getElementById("wind").textContent = `💨 Wind: ${data.wind.speed} m/s`;
    document.getElementById("weatherIcon").src =
      `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;

    const card = document.getElementById("weatherCard");
    card.classList.remove("hidden");

    
    gsap.fromTo(card,
      { opacity: 0, rotateY: 90, scale: 0.5 },
      { opacity: 1, rotateY: 0, scale: 1, duration: 1.2, ease: "back.out(1.7)" }
    );
    gsap.fromTo("#weatherIcon",
      { y: -50, opacity: 0, rotate: -30 },
      { y: 0, opacity: 1, rotate: 0, duration: 1, ease: "elastic.out(1, 0.5)", delay: 0.3 }
    );

  } catch (err) {
    alert("⚠️ Network error. Try again later.");
  }
}

// Cloud animations
gsap.to("#cloudLayer1", {
  x: "100%",
  duration: 60,
  ease: "linear",
  repeat: -1
});
gsap.to("#cloudLayer2", {
  x: "100%",
  duration: 100,
  ease: "linear",
  repeat: -1
});

// 3D tilt effect
const card = document.getElementById("weatherCard");
document.addEventListener("mousemove", (e) => {
  if (!card.classList.contains("hidden")) {
    let x = (window.innerWidth / 2 - e.pageX) / 25;
    let y = (window.innerHeight / 2 - e.pageY) / 25;
    gsap.to(card, { rotationY: x, rotationX: y, duration: 0.5 });
  }
});
document.addEventListener("mouseleave", () => {
  gsap.to(card, { rotationY: 0, rotationX: 0, duration: 0.8, ease: "power3.out" });
});

// Dark/Light toggle
const themeToggle = document.getElementById("themeToggle");
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  document.body.classList.toggle("light");

  if (document.body.classList.contains("dark")) {
    themeToggle.textContent = "☀️ Light Mode";
  } else {
    themeToggle.textContent = "🌙 Dark Mode";
  }
});
