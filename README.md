<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeathrIQ - 3D Project README</title>
    <style>
        /* Basic Reset and Body Styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #000005;
            color: #fff;
            overflow: hidden; /* Prevent scrollbars */
        }
        /* The 3D canvas will fill the screen */
        #bg {
            position: fixed;
            top: 0;
            left: 0;
            outline: none;
        }

        /* --- UI & Information Panels --- */
        #ui-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none; /* Allow clicking through to the canvas */
            display: flex;
            align-items: center;
            padding: 40px;
        }

        /* Holographic Information Panel */
        .info-panel {
            width: 400px;
            padding: 30px;
            background: rgba(10, 20, 45, 0.6);
            border: 1px solid rgba(0, 170, 255, 0.5);
            border-radius: 15px;
            backdrop-filter: blur(10px) saturate(120%);
            box-shadow: 0 0 30px rgba(0, 170, 255, 0.3);
            pointer-events: all; /* Make panels clickable */
            opacity: 0;
            transform: translateX(-50px) scale(0.95);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }

        .info-panel.visible {
            opacity: 1;
            transform: translateX(0) scale(1);
        }

        .info-panel h2 {
            font-size: 2rem;
            color: #00aaff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .info-panel h3 {
            font-size: 1.2rem;
            color: #ff9500;
            margin-top: 25px;
            margin-bottom: 10px;
            border-left: 3px solid #ff9500;
            padding-left: 10px;
        }

        .info-panel p, .info-panel li {
            font-size: 1rem;
            line-height: 1.7;
            color: #e0e0e0;
        }
        
        .info-panel ul {
            list-style: none;
            padding-left: 0;
        }

        .info-panel li {
            background: rgba(255,255,255,0.05);
            padding: 8px 12px;
            border-radius: 5px;
            margin-bottom: 8px;
        }

        .info-panel code {
            background-color: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 5px;
            display: block;
            margin-top: 10px;
            font-family: 'Courier New', Courier, monospace;
            white-space: pre;
        }
        
        /* --- Static UI Elements --- */
        #title-container {
            position: fixed;
            top: 40px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            pointer-events: none;
        }
        #title-container h1 {
            font-size: 3rem;
            font-weight: 700;
            text-shadow: 0 0 15px rgba(0, 170, 255, 0.8);
        }
        #title-container p {
            font-size: 1.1rem;
            color: #a1a1a6;
        }
        
        #instructions {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: #a1a1a6;
            font-size: 0.9rem;
            background: rgba(0,0,0,0.3);
            padding: 8px 15px;
            border-radius: 20px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 170, 255, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 170, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 170, 255, 0); }
        }
    </style>
    <!-- Import Poppins font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap" rel="stylesheet">
    <!-- Import Bootstrap Icons for UI -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
</head>
<body>

    <!-- 3D Scene Canvas -->
    <canvas id="bg"></canvas>

    <!-- Main Title -->
    <div id="title-container">
        <h1>WeathrIQ</h1>
        <p>Interactive Project Overview</p>
    </div>

    <!-- Instructions for user -->
    <div id="instructions">
        Click on the crystal facets to explore the project
    </div>

    <!-- Container for dynamic UI panels -->
    <div id="ui-container">
        <!-- Panels will be dynamically generated here by JavaScript -->
    </div>

    <!-- Three.js library -->
    <script type="importmap">
        {
            "imports": {
                "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
            }
        }
    </script>

    <!-- Main 3D Application Logic -->
    <script type="module">
        import * as THREE from 'three';

        // --- SCENE SETUP ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector('#bg'), antialias: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.position.setZ(30);

        // --- LIGHTING ---
        const pointLight = new THREE.PointLight(0xffffff, 100);
        pointLight.position.set(5, 5, 5);
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(pointLight, ambientLight);

        // --- README CONTENT ---
        // This object holds all the information for our panels.
        const readmeContent = {
            about: {
                title: "About The Project",
                icon: "bi-info-circle-fill",
                content: `
                    <p>WeathrIQ is a real-time weather forecasting application that leverages machine learning to provide not just current weather data, but also predictions for future conditions.</p>
                    <p>This project was built to demonstrate the integration of a Django backend with a dynamic, visually appealing frontend, powered by AI models.</p>
                `
            },
            features: {
                title: "Core Features",
                icon: "bi-star-fill",
                content: `
                    <ul>
                        <li><strong>Live Weather Data:</strong> Fetches up-to-the-minute weather for any city.</li>
                        <li><strong>Hourly Forecast:</strong> Predicts temperature and humidity for the next 5 hours.</li>
                        <li><strong>AI Rain Prediction:</strong> A trained RandomForest model predicts the likelihood of rain tomorrow.</li>
                        <li><strong>Dynamic UI:</strong> The interface changes based on the current weather conditions.</li>
                        <li><strong>Interactive 3D Visuals:</strong> Engaging animations and effects for a premium user experience.</li>
                    </ul>
                `
            },
            techStack: {
                title: "Technology Stack",
                icon: "bi-hdd-stack-fill",
                content: `
                    <h3>Backend</h3>
                    <ul>
                        <li>Python & Django</li>
                        <li>Scikit-learn, Pandas, NumPy</li>
                        <li>OpenWeatherMap API</li>
                    </ul>
                    <h3>Frontend</h3>
                    <ul>
                        <li>HTML5, CSS3, JavaScript</li>
                        <li>Chart.js for data visualization</li>
                        <li>Three.js for this 3D scene</li>
                    </ul>
                `
            },
            setup: {
                title: "Setup & Installation",
                icon: "bi-gear-fill",
                content: `
                    <p>To run this project locally, follow these steps:</p>
                    <h3>1. Clone the repository</h3>
                    <code>git clone [your-repo-link]</code>
                    <h3>2. Install dependencies</h3>
                    <code>pip install -r requirements.txt</code>
                    <h3>3. Set up environment variables</h3>
                    <p>Create a .env file and add your OPENWEATHER_API_KEY.</p>
                    <h3>4. Train the models</h3>
                    <code>python main/forecast/train_models.py</code>
                    <h3>5. Run the server</h3>
                    <code>python manage.py runserver</code>
                `
            }
        };

        // --- 3D OBJECTS ---
        // The main interactive crystal
        const geometry = new THREE.IcosahedronGeometry(10, 0);
        const material = new THREE.MeshStandardMaterial({
            color: 0x00aaff,
            roughness: 0.1,
            metalness: 0.8,
            emissive: 0x003366,
            flatShading: true,
        });
        const crystal = new THREE.Mesh(geometry, material);
        scene.add(crystal);
        
        // Add "hotspots" to the crystal facets for interaction
        const hotspotGeometry = new THREE.SphereGeometry(0.5);
        const hotspotMaterial = new THREE.MeshBasicMaterial({ color: 0xff9500 });
        const hotspots = [];
        const facetPositions = [
            geometry.attributes.position.getX(0), geometry.attributes.position.getX(3),
            geometry.attributes.position.getX(12), geometry.attributes.position.getX(24)
        ];
        
        const contentKeys = Object.keys(readmeContent);
        for(let i = 0; i < 4; i++) {
            const hotspot = new THREE.Mesh(hotspotGeometry, hotspotMaterial.clone());
            const pos = new THREE.Vector3(
                geometry.attributes.position.getX(i * 6),
                geometry.attributes.position.getY(i * 6),
                geometry.attributes.position.getZ(i * 6)
            ).multiplyScalar(1.1);
            hotspot.position.copy(pos);
            hotspot.userData.id = contentKeys[i]; // Link hotspot to content
            crystal.add(hotspot);
            hotspots.push(hotspot);
        }

        // Starfield background
        const starVertices = [];
        for (let i = 0; i < 10000; i++) {
            const x = THREE.MathUtils.randFloatSpread(2000);
            const y = THREE.MathUtils.randFloatSpread(2000);
            const z = THREE.MathUtils.randFloatSpread(2000);
            starVertices.push(x, y, z);
        }
        const starGeometry = new THREE.BufferGeometry();
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
        const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.7 });
        const stars = new THREE.Points(starGeometry, starMaterial);
        scene.add(stars);


        // --- INTERACTION ---
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        let activePanelId = null;

        function onMouseClick(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(hotspots);

            if (intersects.length > 0) {
                const hotspotId = intersects[0].object.userData.id;
                toggleInfoPanel(hotspotId);
            }
        }
        window.addEventListener('click', onMouseClick);

        // --- UI MANAGEMENT ---
        function toggleInfoPanel(id) {
            // Hide currently active panel if there is one
            if (activePanelId && activePanelId !== id) {
                const currentPanel = document.getElementById(`panel-${activePanelId}`);
                if (currentPanel) currentPanel.classList.remove('visible');
            }
            
            // Show the new panel
            let panel = document.getElementById(`panel-${id}`);
            if (!panel) {
                panel = createInfoPanel(id);
                document.getElementById('ui-container').appendChild(panel);
            }

            // Use a timeout to allow the DOM to update before adding the class
            setTimeout(() => {
                panel.classList.toggle('visible');
                activePanelId = panel.classList.contains('visible') ? id : null;
            }, 50);
        }

        function createInfoPanel(id) {
            const data = readmeContent[id];
            const panel = document.createElement('div');
            panel.id = `panel-${id}`;
            panel.className = 'info-panel';
            panel.innerHTML = `
                <h2><i class="bi ${data.icon}"></i> ${data.title}</h2>
                ${data.content}
            `;
            return panel;
        }

        // --- RESIZE HANDLER ---
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- ANIMATION LOOP ---
        function animate() {
            requestAnimationFrame(animate);

            // Animate crystal rotation
            crystal.rotation.y += 0.001;
            crystal.rotation.x += 0.0005;
            
            // Animate hotspots
            hotspots.forEach(hotspot => {
                hotspot.material.color.set(0xff9500);
                hotspot.material.opacity = Math.sin(Date.now() * 0.005) * 0.5 + 0.5;
            });
            
            if (activePanelId) {
                const activeHotspot = hotspots.find(h => h.userData.id === activePanelId);
                if(activeHotspot) activeHotspot.material.color.set(0x00ffaa); // Highlight active hotspot
            }

            renderer.render(scene, camera);
        }

        animate();
    </script>
</body>
</html>
