<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - My Account</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-green: #9cd49c;
            --sidebar-border: #333;
            --accent-green: #7cb342;
            --glass-white: rgba(255, 255, 255, 0.2);
            --input-bg: #e8f5e9;
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

        .user-profile {
            display: flex;
            align-items: center;
            padding: 15px;
            border-top: 2px solid var(--sidebar-border);
            background-color: rgba(255, 255, 255, 0.1);
            gap: 12px;
        }

        /* Account Content Styles */
        main {
            flex-grow: 1;
            padding: 40px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }

        .account-card {
            background-color: var(--glass-white);
            border: 2px solid var(--sidebar-border);
            border-radius: 40px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
            position: relative;
        }

        h2 {
            font-family: 'Fredoka One', cursive;
            color: white;
            font-size: 2.5rem;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .profile-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
        }

        .large-profile-pic {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px dashed var(--sidebar-border);
            background-color: white;
            object-fit: cover;
            padding: 5px;
        }

        .info-group {
            text-align: left;
            margin-bottom: 30px;
            width: 100%;
        }

        .info-label {
            display: block;
            font-weight: bold;
            color: #1a3300;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }

        .info-value {
            width: 100%;
            padding: 12px;
            background-color: var(--input-bg);
            border: 2px solid #333;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 1rem;
            color: #555;
        }

        .btn-action {
            background-color: var(--accent-green);
            color: #1a3300;
            border: 1.5px solid #558b2f;
            padding: 12px 25px;
            font-size: 1rem;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px #558b2f;
            font-weight: bold;
            font-family: 'Nunito', sans-serif;
            transition: all 0.2s;
            width: 100%; /* Making it a full-width action button */
        }

        .btn-action:active {
            box-shadow: 0 1px #558b2f;
            transform: translateY(3px);
        }

        .sign-out-btn:hover {
            background-color: #d32f2f;
            color: white;
        }

        .plant-decoration {
            position: absolute;
            font-size: 50px;
            bottom: -25px;
            left: 20px;
            transform: rotate(-15deg);
        }

        /* Modal Overlay */
        .modal-overlay {
            display: none; /* Hidden by default */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        /* Modal Box */
        .modal-content {
            background-color: #c5e1c5;
            padding: 30px;
            border: 3px solid var(--sidebar-border);
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .modal-content h3 {
            font-family: 'Fredoka One', cursive;
            margin-top: 0;
            color: #1a3300;
        }

        .modal-actions {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
    </style>
</head>
<body>

<nav>
    <a href="/home" class="nav-item">Home</a>
    <a href="/myPlants" class="nav-item">My plants</a>
    <a href="/allPlants" class="nav-item">Add a plant</a>
    <a href="#" class="nav-item active">My account</a>
    <div style="flex-grow: 1;"></div>

    <a href="/logout" class="sign-out-btn">Sign out</a>
    <div class="user-profile">
        <img src="https://via.placeholder.com/50" style="width:50px; height:50px; border-radius:50%; border: 2px solid #333;">
        <span style="font-size: 0.9rem; font-weight: bold;">{{email}}</span>
    </div>
</nav>

<main>
    <div class="account-card">
        <h2>Account Settings</h2>

        <div class="profile-section">
            <img src="https://via.placeholder.com/150" class="large-profile-pic" alt="User Profile">
            <button class="btn-action" style="background-color: #b8e2b8; font-size: 0.8rem; padding: 5px 15px; width: auto; box-shadow: 0 2px #4e944e;">Update Photo</button>
        </div>

        <div class="info-group">
            <span class="info-label">Email Address</span>
            <div class="info-value">{{email}}</div>
        </div>

        <div class="info-group">
            <button class="btn-action" onclick="openModal()">Change Password</button>
        </div>

        <div class="plant-decoration">🌿</div>
    </div>
</main>

<div id="passwordModal" class="modal-overlay">
    <div class="modal-content">
        <h3>Change Password</h3>
        <p>Enter your new password below:</p>
        <input type="password" id="newPassword" class="info-value" placeholder="New password" style="background: white; margin-bottom: 20px;">

        <div class="modal-actions">
            <button class="btn-action" onclick="submitPasswordChange()" style="width: auto;">Update Password</button>
            <button class="btn-action" onclick="closeModal()" style="background-color: #ccc; box-shadow: 0 4px #999; width: auto; border-color: #999;">Cancel</button>
        </div>
    </div>
</div>

</body>

<script>
    function openModal() {
        document.getElementById('passwordModal').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('passwordModal').style.display = 'none';
        document.getElementById('newPassword').value = ''; // Clear input
    }

    async function submitPasswordChange() {
        const newPassword = document.getElementById('newPassword').value;

        if (newPassword.length < 6) {
            alert("Password must be at least 6 characters long.");
            return;
        }

        try {
            const response = await fetch('/account/change_password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // We wrap the password in an object to match standard JSON structures
                body: JSON.stringify({ "new_password": newPassword })
            });

            if (response.ok) {
                alert("Success! Your password has been updated.");
                closeModal();
            } else {
                const errorData = await response.json();
                alert("Error: " + (errorData.detail || "Could not update password."));
            }
        } catch (error) {
            console.error('Network error:', error);
            alert("Network error. Please check if the server is running.");
        }
    }
</script>
</html>