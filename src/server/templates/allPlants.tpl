<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - All Plants</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-green: #9cd49c;
            --sidebar-border: #333;
            --accent-green: #7cb342;
            --glass-white: rgba(255, 255, 255, 0.2);
            --list-bg: #e8f5e9;
            --list-stripe: #dcedc8;
        }

        body {
            background-color: var(--bg-green);
            margin: 0;
            display: flex;
            height: 100vh;
            font-family: 'Nunito', sans-serif;
            color: #333;
        }

        /* Sidebar Navigation */
        nav {
            width: 280px;
            background-color: #c5e1c5;
            border-right: 2px solid var(--sidebar-border);
            display: flex;
            flex-direction: column;
        }

        .nav-item {
            padding: 30px 20px;
            font-family: 'Fredoka One', cursive;
            font-size: 1.8rem;
            color: #333;
            text-decoration: none;
            border-bottom: 2px solid var(--sidebar-border);
            transition: background 0.3s;
        }

        .nav-item:hover, .nav-item.active {
            background-color: var(--accent-green);
            color: white;
        }

        .sign-out-btn {
            padding: 15px 20px;
            font-family: 'Fredoka One', cursive;
            font-size: 1.2rem;
            color: #333;
            text-decoration: none;
            border-top: 2px solid var(--sidebar-border);
            text-align: center;
            background-color: rgba(255, 255, 255, 0.1);
            transition: background 0.3s;
        }

        .sign-out-btn:hover {
            background-color: #d32f2f;
            color: white;
        }

        .user-profile {
            display: flex;
            align-items: center;
            padding: 15px;
            border-top: 2px solid var(--sidebar-border);
            background-color: rgba(255, 255, 255, 0.1);
            gap: 12px;
        }

        .profile-pic {
            width: 50px; height: 50px;
            border-radius: 50%;
            border: 2px solid var(--sidebar-border);
            background-color: white;
        }

        /* Main Content Area */
        main {
            flex-grow: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
        }

        /* Plant List Toolbar (Based on your image) */
        .plant-toolbar {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }

        .plant-toolbar h2 {
            font-family: 'Fredoka One', cursive;
            color: white;
            font-size: 2rem;
            margin: 0;
            margin-right: 10px;
        }

        .tool-btn {
            background-color: #b8e2b8;
            border: 1px solid #7cb342;
            color: #4e944e;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }

        .sort-label {
            margin-left: auto;
            font-weight: bold;
        }

        select {
            background-color: #7cb342;
            color: #1a3300;
            border: 1px solid #333;
            padding: 5px 10px;
            border-radius: 4px;
            font-family: 'Nunito', sans-serif;
            font-weight: bold;
        }

        /* Plant List Container */
        .plant-list-container {
            flex-grow: 1;
            background-color: var(--list-bg);
            border: 2px solid #333;
            border-radius: 10px;
            overflow: scroll;
            background-image: repeating-linear-gradient(
                    var(--list-bg),
                    var(--list-bg) 40px,
                    var(--list-stripe) 40px,
                    var(--list-stripe) 80px
            );
        }

        .plant-row {
            border-bottom: 1px solid rgba(0,0,0,0.05);
            transition: background 0.2s;
        }

        .plant-row:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }

        .plant-summary-content {
            display: flex;
            align-items: center;
            height: 40px; /* Matches your stripe height */
            padding: 0 20px;
            font-weight: bold;
        }

        .plant-details-extra {
            padding: 15px 40px;
            background-color: rgba(255, 255, 255, 0.5);
            border-top: 1px dashed var(--sidebar-border);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .detail-label {
            color: var(--accent-green);
            font-weight: bold;
            margin-right: 5px;
        }

        .plant-name { flex: 2; }
        .plant-species { flex: 2; font-style: italic; color: #555; }
        .plant-status { flex: 1; text-align: right; }

        .loading-state {
            display: flex;
            align-items: center;
            padding: 20px;
            gap: 15px;
            font-size: 1.2rem;
            color: #4e944e;
        }

        details summary {
            list-style: none;
            cursor: pointer;
            outline: none;
        }
        details summary::-webkit-details-marker {
            display: none;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

<nav>
    <a href="/home" class="nav-item">Home</a>
    <a href="/myPlants" class="nav-item">My plants</a>
    <a href="/allPlants" class="nav-item active">Add a plant</a>
    <a href="/account" class="nav-item">My account</a>
    <div style="flex-grow: 1;"></div>

    <a href="/logout" class="sign-out-btn">Sign out</a>
    <div class="user-profile">
        <img src="https://via.placeholder.com/50" class="profile-pic">
        <span class="user-email">{{email}}</span>
    </div>
</nav>

<main>
    <div class="plant-toolbar">
        <h2>All plants</h2>
        <button class="tool-btn">Expand all</button>
        <button class="tool-btn">Collapse all</button>

        <span class="sort-label">Sort by:</span>
        <select>
            <option>Common name</option>
            <option>Scientific name</option>
            <option>Something else</option>
        </select>
    </div>

    <div class="plant-list-container">
        {% if plants %}
        {% for plant in plants.data %}
        <details class="plant-row" id='{{plant.row_id}}' style="background-color: {{ '#E8F5E9' if plant.id % 2 == 0 else '#E8F5E9' }};">
            <summary>
                <div class="plant-summary-content">
                    <span style="flex: 2;">🌿 {{ plant.common_name if plant.common_name else plant.scientific_name }}</span>
                    <button onclick="addPlant({{ plant.id }}, '{{ (plant.common_name or plant.scientific_name) | e }}')">Add</button>
                </div>
            </summary>

            <div class="plant-details-extra">
                <div><span class="detail-label">Scientific name:</span> {{ plant.scientific_name }}</div>
                <div><span class="detail-label">Family:</span> {{ plant.family }}</div>
                <div style="margin-top: 10px;">
                    <button
                            class="tool-btn"
                            style="border-color: #d32f2f; color: #d32f2f;"
                            onclick="deletePlant('{{ plant.plant_id }}', '{{plant.row_id}}')">
                        Remove
                    </button>
                </div>
            </div>
        </details>
        {% endfor %}
        {% else %}
        <div class="loading-state">
            <span>No plants found!</span>
        </div>
        {% endif %}
    </div>
</main>

</body>

<script>
  async function addPlant(plantId, commonName) {
      try {
          const response = await fetch(`/myPlants/addPlant`, {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                  plant_id: plantId,
                  common_name: commonName
              })
          });

          const data = await response.json();

          if (response.ok && data.ok) {
              console.log(`Plant ${plantId} added successfully.`);
              alert("Plant added!");
          } else {
              console.error('Failed to add plant:', data);
              alert('Could not add plant: ' + (data.error || response.statusText));
          }
      } catch (error) {
          console.error('Network error while adding plant:', error);
          alert("Network/server error when adding plant.");
      }
  }

</script>
</html>