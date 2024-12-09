// Filter functionality
const filterButtons = document.querySelectorAll(".filter-btn");
const galleryItems = document.querySelectorAll(".gallery-item");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    // Update active button
    filterButtons.forEach((btn) =>
      btn.classList.remove("bg-purple-600", "text-white")
    );
    button.classList.add("bg-purple-600", "text-white");

    const filter = button.getAttribute("data-filter");

    galleryItems.forEach((item) => {
      if (filter === "all" || item.classList.contains(filter)) {
        item.classList.remove("hidden");
      } else {
        item.classList.add("hidden");
      }
    });
  });
});

// Modal functionality
function openImageModal(imageSrc) {
  const modal = document.getElementById("imageModal");
  const modalImage = modal.querySelector("img");
  modalImage.src = imageSrc;
  modal.classList.add("active");
}

function openVideoModal(videoSrc) {
  const modal = document.getElementById("videoModal");
  const modalVideo = modal.querySelector("video source");
  modalVideo.src = videoSrc;
  modal.querySelector("video").load();
  modal.classList.add("active");
}

function closeModal() {
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.classList.remove("active");
    const video = modal.querySelector("video");
    if (video) video.pause();
  });
}

// Add click handlers to gallery items
document.querySelectorAll(".gallery-item.foto").forEach((item) => {
  item.addEventListener("click", () => {
    const imageSrc = item.querySelector("img").src;
    openImageModal(imageSrc);
  });
});

document.querySelectorAll(".gallery-item.video").forEach((item) => {
  item.addEventListener("click", () => {
    // Replace with actual video source
    const videoSrc = "content/video/testing.mp4";
    openVideoModal(videoSrc);
  });
});

// Close modal when clicking outside
document.querySelectorAll(".modal").forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
});

// Close modal with escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});
