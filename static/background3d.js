// 3D animated background using Three.js
const container = document.getElementById('bg3d');
let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setClearColor(0x111111, 1);
renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// Create a group of moving particles
const particles = new THREE.Group();
const particleCount = 120;
for (let i = 0; i < particleCount; i++) {
    let geometry = new THREE.SphereGeometry(0.18, 8, 8);
    let material = new THREE.MeshBasicMaterial({ color: 0x00c6ff, wireframe: true });
    let particle = new THREE.Mesh(geometry, material);
    particle.position.set(
        (Math.random() - 0.5) * 16,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 16
    );
    particles.add(particle);
}
scene.add(particles);

// Add a rotating wireframe sphere
const sphereGeometry = new THREE.SphereGeometry(4, 32, 32);
const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0x0072ff, wireframe: true, opacity: 0.5, transparent: true });
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
scene.add(sphere);

camera.position.z = 18;

function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.0015;
    particles.rotation.x += 0.0007;
    sphere.rotation.y += 0.002;
    sphere.rotation.x += 0.001;
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}); 