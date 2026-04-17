<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - My Plants</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">

    <style>
        .watering-wrapper {
            margin-top: 10px;
        }

        .watering-bar {
            width: 220px;
            height: 16px;
            background: #eee;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #999;
        }

        .watering-fill {
            height: 100%;
            transition: width 0.4s ease;
        }

        .watering-text {
            font-size: 0.85rem;
            margin-top: 4px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<nav>
    <a href="/home" class="nav-item">Home</a>
    <a href="#" class="nav-item active">My plants</a>
    <a href="/allPlants" class="nav-item">Add a plant</a>
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
        <h2>Your plants</h2>
        <form method="post" action="/myPlants/water">
            <button class="tool-btn" type="submit">Water all plants</button>
        </form>
        <button class="tool-btn" onClick="expandAll()">Expand all</button>
        <button class="tool-btn" onClick="collapseAll()">Collapse all</button>

        <span class="sort-label">Sort by:</span>
        <form method="get" action="/myPlants">
    <select name="sort_by" onchange="this.form.submit()">
    <option value="nickname"
        {% if request.query_params.get('sort_by') == 'nickname' %}selected{% endif %}>
        Nickname
    </option>
    <option value="species"
        {% if request.query_params.get('sort_by') == 'species' %}selected{% endif %}>
        Species
    </option>
    <option value="last_watered"
        {% if request.query_params.get('sort_by') == 'last_watered' %}selected{% endif %}>
        Last Watered
    </option>
</select>
</form>
    </div>

    <div class="plant-list-container">
        {% if plants %}
        {% for plant in plants %}
        <details class="plant-row" id='{{plant.row_id}}' style="background-color: #E8F5E9;">
            <summary>
                <div class="plant-summary-content">
                    <span style="flex: 2;">
                        🌿 {{ plant.common_name if plant.common_name else plant.scientific_name }}
                    </span>

                    <span style="flex: 1; text-align: center; font-size: 0.85rem;">
                        {% if plant.watering_status and plant.watering_status.needs_water %}
                            🔴 Needs water
                        {% elif plant.watering_status %}
                            🟢 OK
                        {% else %}
                            ⚪ Unknown
                        {% endif %}
                    </span>

                    <span style="flex: 1; text-align: right; font-size: 0.8rem; color: #555;">
                        Last watered: {{ plant.last_watered }} ▾
                    </span>
                </div>
            </summary>

            <div class="plant-details-extra">

                                <!-- Watering status -->
                {% if plant.watering_status %}
                <div class="watering-wrapper">
                    <div class="watering-bar">
                        <div class="watering-fill"
                            style="width: {{ plant.watering_status.percent }}%;
                                    background-color:
                                        {% if plant.watering_status.percent < 50 %}
                                            #4caf50
                                        {% elif plant.watering_status.percent < 80 %}
                                            #ff9800
                                        {% else %}
                                            #f44336
                                        {% endif %};">
                        </div>
                    </div>

                    <div class="watering-text">
                        {{ plant.watering_status.days_since }} days since watering
                    </div>
                </div>
                {% endif %}
                <div style="margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap;">

                    <!-- Water button -->
                    <form method="post" action="/myPlants/water/{{ plant.row_id }}">
                        <button class="tool-btn" type="submit">
                            💧 Mark as watered
                        </button>
                    </form>

                    <!-- Rename button -->
                    <button
                        class="tool-btn"
                        type="button"
                        onClick="renamePlant('{{plant.row_id}}', '{{(plant.common_name if plant.common_name else plant.scientific_name) | e }}')">
                            Rename
                    </button>

                    <!-- Remove button -->
                    <button
                        class="tool-btn"
                        style="border-color: #d32f2f; color: #d32f2f;"
                        onclick="deletePlant('{{ plant.row_id }}')">
                        Remove
                    </button>

                </div>
            </div>
        </details>
        {% endfor %}
        {% else %}
        <div class="loading-state">
            <span>You haven't added any plants yet!</span>
        </div>
        {% endif %}
    </div>
</main>

</body>

<script>
    async function deletePlant(rowId) {
        try {
            const response = await fetch(`/myPlants/delete/` + rowId, {
              method: 'DELETE',
              headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
              document.getElementById(rowId).remove();
            } else {
              let msg = response.statusText;
              try {
                const errorData = await response.json();
                msg = errorData.detail || msg;
              } catch (_) {}
              alert('Could not delete plant: ' + msg);
            }
      } catch (error) {
        console.error('Network error while deleting plant:', error);
      }
    }

    async function renamePlant(rowId, currentName) {
        const newName = prompt("Enter a new name for your plant:", currentName);

        if (newName === null) {
            return;
        }

        if(!newName.trim()) {
            alert("Name cannot be empty.");
            return;
        }

        try {
            const response = await fetch(`/myPlants/rename/${rowId}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    new_name: newName
                })
            });

            const data = await response.json();

            if (response.ok && data.ok) {
                window.location.reload();
            } else {
                alert("Could not rename plant: " + (data.error || response.statusText));
            }

        } catch (error) {
            console.error("Network error while renaming plant:", error);
            alert("Network/server error when renaming plant.");
        }
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