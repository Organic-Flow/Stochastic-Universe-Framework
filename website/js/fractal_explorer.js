/* ── Fractal Explorer Engine ── */

const canvas = document.getElementById('fractalCanvas');
const ctx = canvas.getContext('2d');
const slider = document.getElementById('stochasticSlider');
const valueLabel = document.getElementById('stochasticValueLabel');

const START_FRAME = 801;
const END_FRAME = 1000;
const FRAME_COUNT = END_FRAME - START_FRAME + 1;

// Base path for images - relative to index.html
const IMAGE_BASE_PATH = '../naturalist_fractal/fractal_frames/frames4/';

const frames = [];
let loadedCount = 0;
let currentFrameIndex = 0;

// Preload routine
function preloadFrames() {
  for (let i = START_FRAME; i <= END_FRAME; i++) {
    const img = new Image();
    img.onload = () => {
      loadedCount++;
      if (loadedCount === FRAME_COUNT) {
        console.log('All frames loaded');
        render(); // Initial render
      }
    };
    img.src = `${IMAGE_BASE_PATH}frame_${i}.png`;
    frames.push(img);
  }
}

function render() {
  const index = parseInt(slider.value) - START_FRAME;
  const factor = (0.803 + (index * 0.001)).toFixed(3);
  
  valueLabel.textContent = factor;
  
  // Basic rendering
  if (frames[index] && frames[index].complete) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Cross-fade logic for smoother transition if needed
    // For now, simpler direct render for performance, 
    // but the frame rate is high enough that it might feel smooth.
    ctx.drawImage(frames[index], 0, 0, canvas.width, canvas.height);
  }
}

// Event Listeners
slider.addEventListener('input', () => {
    requestAnimationFrame(render);
});

// Initialization
preloadFrames();

// Optional: handle window resize for canvas resolution
window.addEventListener('resize', () => {
    // Keep 1:1 aspect ratio or responsive sizing
});
