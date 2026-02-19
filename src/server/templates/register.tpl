<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Happy Plants - Register</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #9cd49c;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: 'Nunito', sans-serif;
        }

        .login-container {
            text-align: center;
            width: 100%;
            max-width: 500px;
            position: relative;
        }

        .logo-area {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }

        .logo-circle {
            width: 80px;
            height: 80px;
            background: #b8e2b8;
            border-radius: 50%;
            border: 4px dashed #4e944e;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 40px;
            margin-right: 15px;
        }

        h1 {
            color: white;
            font-family: 'Fredoka One', cursive;
            font-size: 2.5rem;
            margin: 0;
            line-height: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .login-box {
            background-color: rgba(255, 255, 255, 0.2);
            border: 2px solid #333;
            border-radius: 5px;
            padding: 40px 30px;
            position: relative;
            z-index: 1;
        }

        .plant-left, .plant-right {
            position: absolute;
            font-size: 50px;
            z-index: 10;
            top: -40px;
        }
        .plant-left { left: -20px; }
        .plant-right { right: -20px; }

        h2 {
            color: white;
            font-size: 2.5rem;
            margin-top: 0;
            margin-bottom: 30px;
            font-family: 'Fredoka One', cursive;
        }

        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 2px solid #4da3ff;
            background-color: #e8f5e9;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 1rem;
            font-family: 'Nunito', sans-serif;
        }

        button {
            background-color: #7cb342;
            color: #1a3300;
            border: 1.5px solid #558b2f;
            padding: 10px 40px;
            font-size: 1.1rem;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 4px #558b2f;
            font-weight: bold;
            transition: all 0.2s;
        }

        button:active {
            box-shadow: 0 1px #558b2f;
            transform: translateY(3px);
        }

        .error-message {
            color: #d32f2f;
            background-color: #ffcdd2;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            display: none;
            font-weight: bold;
        }

        .login-link {
            display: block;
            margin-top: 25px;
            color: #0099cc;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
        }
    </style>
</head>
<body>

<div class="login-container">
    <div class="logo-area">
        <div class="logo-circle">🪴</div>
        <h1>My Happy<br>Plants</h1>
    </div>

    <div class="login-box">
        <div class="plant-left">🪴</div>
        <div class="plant-right">🪴</div>

        <h2>Register</h2>

        <div id="error" class="error-message"></div>

        <form id="registerForm" action="/register" method="POST">
            <input type="email" name="email" placeholder="E-mail" required value="test@mail.com">
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input type="password" id="confirm_password" placeholder="Confirm Password" required>

            <button type="submit">Sign Up</button>
        </form>

        <a href="/home" class="login-link">Already have an account? Login!</a>
    </div>
</div>

<script>
    const form = document.getElementById('registerForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const errorDiv = document.getElementById('error');

    // When the user submits the form, I.E presses the "sign up" button,
    // we first check if password and confirm password are the same,
    // and if the password is longer than 6 characters.
    // If they are, the form sends a POST request to /register
    // We prevent it from sending the request with "event.preventDefault()"
    form.addEventListener('submit', function(event) {
        if (password.value !== confirmPassword.value) {
            event.preventDefault();
            errorDiv.innerHTML = "Passwords do not match!"
            errorDiv.style.display = 'block';
        }
        else if(password.value.length < 6) {
            event.preventDefault();
            errorDiv.innerHTML = 'Password must be at least 6 characters long!';
            errorDiv.style.display = 'block';
        }
        else {
            errorDiv.style.display = 'none';
        }
    });

    if ('{{errorCode}}' !== '') {
        errorDiv.innerHTML = '{{errorCode}}';
        errorDiv.style.display = 'block';
    }
</script>

</body>
</html>