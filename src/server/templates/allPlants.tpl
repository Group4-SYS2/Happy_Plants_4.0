<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - All Plants</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">

    <script type="text/javascript">
        let plants = JSON.parse({{ plants | tojson }}).data;
    </script>
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
        <select id="sort-label">
            <option>Common name</option>
            <option>Scientific name</option>
            <option>Something else</option>
        </select>
    </div>

    <div class="plant-list-container">
        {% if plants %}
        {% else %}
        <div class="loading-state">
            <span>No plants found!</span>
        </div>
        {% endif %}
    </div>
</main>

</body>

<script>
    document.addEventListener('DOMContentLoaded', async () => {
        console.log(plants);
        renderPlants("");
    });

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

    document.getElementById("searchInput").addEventListener("input", function() {
        const query = this.value;
        renderPlants(query);
    });

    document.getElementById("sort-label").addEventListener("input", function() {
        renderPlants(document.getElementById("searchInput").value);
    });

    function renderPlants(searchTerm) {
        const container = document.querySelector(".plant-list-container");

        if (!plants.length) {
            container.innerHTML = "<div>No plants found</div>";
            return;
        }

        const sortDropDown = document.getElementById("sort-label");
        if(sortDropDown.value === "Common name") {
            plants = plants.sort(sort_by("common_name"));
        }
        else if(sortDropDown.value === "Scientific name") {
            plants = plants.sort(sort_by("scientific_name"));
        }
        else{
            plants = plants.sort(sort_by("id"));
        }

        container.innerHTML = plants.filter(plant => plant.common_name.toLowerCase().includes(searchTerm.toLowerCase())).map(plant => `
            <details class="plant-row" id="plant-${plant.id}" style="background-color: #E8F5E9;">
                <summary>
                    <div class="plant-summary-content">
                        <span style="flex: 2;">
                            🌿
                            ${(plant.common_name) ? plant.common_name : plant.scientific_name}
                        </span>
                        <button onclick="addPlant(${plant.id}, ' ${(plant.common_name) ? plant.common_name : plant.scientific_name}')">Add</button>
                    </div>
                </summary>

                <div class="plant-details-extra">
                    <div><span class="detail-label">Scientific name:</span> ${plant.scientific_name}</div>
                    <div><span class="detail-label">Family:</span> ${plant.family}</div>
                    <div>
                        <span class="detail-label">Light need:</span>
                        ${plant.light_text}
                    </div>

                    <div>
                        <span class="detail-label">Water need:</span>
                        ${plant.water_text}
                    </div>

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

    const sort_by = (field) => {
        const key = function(x) {
            return x[field]
        };
        return function(a, b) {
            return a = key(a), b = key(b), ((a > b) - (b > a));
        }
    }
</script>
</html>