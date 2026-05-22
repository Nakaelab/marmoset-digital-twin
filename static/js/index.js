window.HELP_IMPROVE_VIDEOJS = false;

// More Works Dropdown Functionality
function toggleMoreWorks() {
    const dropdown = document.getElementById('moreWorksDropdown');
    const button = document.querySelector('.more-works-btn');
    
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    } else {
        dropdown.classList.add('show');
        button.classList.add('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const container = document.querySelector('.more-works-container');
    const dropdown = document.getElementById('moreWorksDropdown');
    const button = document.querySelector('.more-works-btn');
    
    if (container && !container.contains(event.target)) {
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

// Close dropdown on escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const dropdown = document.getElementById('moreWorksDropdown');
        const button = document.querySelector('.more-works-btn');
        dropdown.classList.remove('show');
        button.classList.remove('active');
    }
});

// Copy BibTeX to clipboard
function copyBibTeX() {
    const bibtexElement = document.getElementById('bibtex-code');
    const button = document.querySelector('.copy-bibtex-btn');
    const copyText = button.querySelector('.copy-text');
    
    if (bibtexElement) {
        navigator.clipboard.writeText(bibtexElement.textContent).then(function() {
            // Success feedback
            button.classList.add('copied');
            copyText.textContent = 'Cop';
            
            setTimeout(function() {
                button.classList.remove('copied');
                copyText.textContent = 'Copy';
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = bibtexElement.textContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            button.classList.add('copied');
            copyText.textContent = 'Cop';
            setTimeout(function() {
                button.classList.remove('copied');
                copyText.textContent = 'Copy';
            }, 2000);
        });
    }
}

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/hide scroll to top button
window.addEventListener('scroll', function() {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (window.pageYOffset > 300) {
        scrollButton.classList.add('visible');
    } else {
        scrollButton.classList.remove('visible');
    }
});

// Video carousel autoplay when in view
function setupVideoCarouselAutoplay() {
    const carouselVideos = document.querySelectorAll('.results-carousel video');
    
    if (carouselVideos.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const video = entry.target;
            if (entry.isIntersecting) {
                // Video is in view, play it
                video.play().catch(e => {
                    // Autoplay failed, probably due to browser policy
                    console.log('Autoplay prevented:', e);
                });
            } else {
                // Video is out of view, pause it
                video.pause();
            }
        });
    }, {
        threshold: 0.5 // Trigger when 50% of the video is visible
    });
    
    carouselVideos.forEach(video => {
        observer.observe(video);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Setup video autoplay for carousel (if any exist)
    setupVideoCarouselAutoplay();
});

let cameraControlInterval = null;

window.startCameraControl = function(viewerId, action) {
    // Clear any existing active control loop
    window.stopCameraControl();
    
    // Execute action immediately on pointer down
    window.controlCamera(viewerId, action);
    
    // Start continuous execution loop every 50ms
    cameraControlInterval = setInterval(function() {
        window.controlCamera(viewerId, action);
    }, 50);
};

window.stopCameraControl = function() {
    if (cameraControlInterval) {
        clearInterval(cameraControlInterval);
        cameraControlInterval = null;
    }
};

// Camera controls helper for model-viewer overlay buttons
window.controlCamera = function(viewerId, action) {
    const mv = document.getElementById(viewerId);
    if (!mv) return;
    
    const orbit = mv.getCameraOrbit();
    if (!orbit) return;
    
    let { theta, phi, radius } = orbit;
    const thetaStep = 0.05; // radians (about 2.8 degrees)
    const phiStep = 0.04;  // radians (about 2.3 degrees)
    const zoomFactor = 0.98; // multiplier for zoom in / zoom out
    
    switch(action) {
        case 'left':
            theta -= thetaStep;
            break;
        case 'right':
            theta += thetaStep;
            break;
        case 'up':
            phi = Math.max(0.05, phi - phiStep);
            break;
        case 'down':
            phi = Math.min(Math.PI - 0.05, phi + phiStep);
            break;
        case 'zoom-in':
            radius = radius * zoomFactor;
            break;
        case 'zoom-out':
            radius = radius / zoomFactor;
            break;
    }
    
    mv.cameraOrbit = `${theta}rad ${phi}rad ${radius}m`;
};

