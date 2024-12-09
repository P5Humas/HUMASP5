// Intersection Observer for counting animation
const observerOptions = {
  root: null,
  rootMargin: "0px",
  threshold: 0.1,
};

let animationStarted = false;

function startCounting(counter, target) {
  let current = 0;
  const increment = target / 100;
  const duration = 1500; // Animation duration in milliseconds
  const steps = duration / 16; // 60fps
  const stepValue = target / steps;

  counter.classList.add("animate-count");

  const timer = setInterval(() => {
    current += stepValue;
    if (current >= target) {
      counter.textContent = target;
      clearInterval(timer);
    } else {
      counter.textContent = Math.floor(current);
    }
  }, 16);
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting && !animationStarted) {
      animationStarted = true;
      document.querySelectorAll(".counter").forEach((counter) => {
        const target = parseInt(counter.getAttribute("data-target"));
        startCounting(counter, target);
      });
    } else if (!entry.isIntersecting) {
      animationStarted = false;
      document.querySelectorAll(".counter").forEach((counter) => {
        counter.textContent = "0";
        counter.classList.remove("animate-count");
      });
    }
  });
}, observerOptions);

// Start observing the stats section
const statsSection = document.getElementById("stats-section");
if (statsSection) {
  observer.observe(statsSection);
}

// Auto-duplicate scrolling content for seamless loop
const scrollContent = document.querySelector(".scroll-content");
if (scrollContent) {
  const content = scrollContent.innerHTML;
  scrollContent.innerHTML = content + content; // Duplicate content
}

// Scroll to top button
const scrollToTopBtn = document.getElementById("scrollToTop");
window.addEventListener("scroll", function () {
  if (window.scrollY > 100) {
    scrollToTopBtn.classList.add("visible");
  } else {
    scrollToTopBtn.classList.remove("visible");
  }
});
scrollToTopBtn.addEventListener("click", function () {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

//animasi card


function appendData() {
  var arr = chart.w.globals.series.slice();
  arr.push(Math.floor(Math.random() * (100 - 1 + 1)) + 1);
  return arr;
}

function removeData() {
  var arr = chart.w.globals.series.slice();
  arr.pop();
  return arr;
}

function randomize() {
  return chart.w.globals.series.map(function () {
    return Math.floor(Math.random() * (100 - 1 + 1)) + 1;
  });
}

function reset() {
  return options.series;
}

document.querySelector("#randomize").addEventListener("click", function () {
  chart.updateSeries(randomize());
});

document.querySelector("#add").addEventListener("click", function () {
  chart.updateSeries(appendData());
});

document.querySelector("#remove").addEventListener("click", function () {
  chart.updateSeries(removeData());
});

document.querySelector("#reset").addEventListener("click", function () {
  chart.updateSeries(reset());
});


