<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - All Plants</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">
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
        <button class="tool-btn" onClick="expandAll()">Expand all</button>
        <button class="tool-btn" onClick="collapseAll()">Collapse all</button>

        <input
    type="text"
    id="searchInput"
    placeholder="Search plants..."
>
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
        <details class="plant-row" id="plant-{{ plant.id }}" style="background-color: {{ '#E8F5E9' if plant.id % 2 == 0 else '#E8F5E9' }};">
            <summary>
                <div class="plant-summary-content">
                    <span style="flex: 2;">
                        🌿
                        {{ plant.common_name if plant.common_name else plant.scientific_name }}
                    </span>
                    <button onclick="addPlant({{ plant.id }}, '{{ (plant.common_name or plant.scientific_name) | e }}')">Add</button>
                </div>
            </summary>

            <div class="plant-details-extra">
                <div><span class="detail-label">Scientific name:</span> {{ plant.scientific_name }}</div>
                <div><span class="detail-label">Family:</span> {{ plant.family }}</div>
                <div>
                    <span class="detail-label">Light need:</span>
                    {{ plant.light_text }}
                </div>

                <div>
                    <span class="detail-label">Water need:</span>
                    {{ plant.water_text }}
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
              alert("Plant successfully added to your library🌱");
          } else {
              console.error('Failed to add plant:', data);
              alert('Could not add plant: ' + (data.error || response.statusText));
          }
      } catch (error) {
          console.error('Network error while adding plant:', error);
          alert("Network/server error when adding plant.");
      }
  }

  let timeout = null;

document.getElementById("searchInput").addEventListener("input", function() {
    const query = this.value;

    clearTimeout(timeout);

    timeout = setTimeout(() => {
        searchPlants(query);
    }, 300);
});

async function searchPlants(query) {
    if (!query) {
    location.reload();
    return;
}

    try {
        const response = await fetch(`/api/searchPlants?search=${encodeURIComponent(query)}`);
        const data = await response.json();

        renderPlants(data.data);

    } catch (error) {
        console.error("Search error:", error);
    }
}

function renderPlants(plants) {
    const container = document.querySelector(".plant-list-container");

    if (!plants.length) {
        container.innerHTML = "<div>No plants found</div>";
        return;
    }

    container.innerHTML = plants.map(plant => `
        <details class="plant-row">
            <summary>
                <div class="plant-summary-content">
                    <span style="flex: 2;">
                        🌿 ${plant.common_name || plant.scientific_name}
                    </span>

                    <button
                        style="margin-left: auto;"
                        onclick="addPlant(${plant.id}, '${plant.common_name || plant.scientific_name}')">
                        Add
                    </button>
                </div>
            </summary>

            <div class="plant-details-extra">
                <div>Scientific: ${plant.scientific_name || "-"}</div>
                <div>Family: ${plant.family || "-"}</div>
            </div>
        </details>
    `).join("");
}

    function expandAll(){
        document.body.querySelectorAll('details')
            .forEach((e) => {e.setAttribute('open',true);})
    }

    function collapseAll(){
        document.body.querySelectorAll('details')
            .forEach((e) => {e.removeAttribute('open')})
    }
</script>
</html>