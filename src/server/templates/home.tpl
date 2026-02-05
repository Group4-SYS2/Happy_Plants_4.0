<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-green: #9cd49c;
            --sidebar-border: #333;
            --accent-green: #7cb342;
            --glass-white: rgba(255, 255, 255, 0.2);
        }

        body {
            background-color: var(--bg-green);
            margin: 0;
            display: flex;
            height: 100vh;
            font-family: 'Nunito', sans-serif;
            color: #333;
        }

        /* Side Navigation */
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
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 2px solid var(--sidebar-border);
            object-fit: cover;
            background-color: white;
        }

        .user-email {
            font-size: 0.9rem;
            word-break: break-all;
            font-weight: bold;
        }

        main {
            flex-grow: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        .logo-badge {
            display: inline-block;
            background-color: var(--accent-green);
            padding: 5px 20px;
            border-radius: 10px;
        }

        h1 {
            color: white;
            font-family: 'Fredoka One', cursive;
            font-size: 3rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        /* Content Card Styling */
        .content-card {
            background-color: var(--glass-white);
            border: 2px solid var(--sidebar-border);
            border-radius: 40px;
            padding: 40px 50px;
            max-width: 650px;
            width: 100%;
            position: relative;
            line-height: 1.7;
            font-size: 1.1rem;
            color: #1a3300;
        }

        .content-card h2 {
            font-family: 'Fredoka One', cursive;
            margin-top: 0;
            margin-bottom: 20px;
            color: #2e7d32;
            font-size: 1.8rem;
        }

        .content-card p {
            margin-bottom: 20px;
        }

        .plant-decoration {
            position: absolute;
            font-size: 40px;
            bottom: -20px;
            right: 20px;
        }
    </style>
</head>
<body>

<nav>
    <a href="#" class="nav-item active">Home</a>
    <a href="/myPlants" class="nav-item">My plants</a>
    <a href="#" class="nav-item">Add a plant</a>
    <a href="/account" class="nav-item">My account</a>
    <div style="flex-grow: 1;"></div>

    <a href="/logout" class="sign-out-btn">Sign out</a>
    <div class="user-profile">
        <img src="https://via.placeholder.com/50" class="profile-pic">
        <span class="user-email">{{email}}</span>
    </div>
</nav>

<main>
    <header>
        <div class="logo-badge">
            <h1>My Happy Plants</h1>
        </div>
    </header>

    <section class="content-card">
        <h2>About the Project</h2>

        <p>My Happy Plants is an website designed to help users care for their indoor plants while providing them with information about those plants.</p>

        <p>My Happy Plants utilizes information retrieved from Trefle.io, which was an open and free API offering data on over one million plant species and hybrids.</p>

        <p>My Happy Plants features a colorful graphical user interface developed in JavaFX with illustrated plant imagery, and allows users to search through tens of thousands of plants, name them, and add them to their personal library.</p>

        <p>My Happy Plants also reminds the user when it is time to water, based on calculations done behind the scene.</p>

        <div class="plant-decoration">🪴</div>
    </section>
</main>

</body>
</html>