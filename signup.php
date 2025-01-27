<?php
include 'connect.php';

$error_message = '';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);

    // Check if the email already exists
    $checkEmail = "SELECT email FROM users WHERE email='$email'";
    $result = $conn->query($checkEmail);

    if ($result->num_rows > 0) {
        $error_message = "Email already exists!";
    } else {
        // Insert new user
        $sql = "INSERT INTO users (email, password) VALUES ('$email', '$password')";

        if ($conn->query($sql) === TRUE) {
            header("Location: login.php");
            exit();
        } else {
            $error_message = "Error: " . $conn->error;
        }
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sign Up - Video Summarizer</title>
    <link rel="stylesheet" href="static/styles.css" />
</head>
<body>
    <div class="container">
        <div class="image-section"></div>
        <div class="login-form">
            <h2>Sign Up</h2>
            <form action="signup.php" method="POST">
                <input type="email" name="email" placeholder="Enter your Email" required />
                <input type="password" name="password" placeholder="Enter your Password" required />
                <button type="submit">Sign Up</button>
            </form>
            <div class="signup-link">
                Already have an account? <a href="login.php">Login</a>
            </div>
            <?php if ($error_message): ?>
                <div class="error-message" style="color: red; margin-top: 10px;">
                    <?php echo $error_message; ?>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
