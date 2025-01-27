<?php
include 'connect.php';
$error_message = '';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    $sql = "SELECT * FROM users WHERE email='$email'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row['password'])) {
            // Redirect to dashboard
            header("Location: dashboard.php");
            exit();
        } else {
            $error_message = "Incorrect password!";
        }
    } else {
        $error_message = "Email does not exist!";
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - Video Summarizer</title>
    <link rel="stylesheet" href="static/styles.css" />
</head>

<body>
    <div class="container">
        <div class="image-section"></div>
        <div class="login-form">
            <h2>Login</h2>
            <form action="login.php" method="POST">
                <input type="email" name="email" placeholder="Enter your Email" required />
                <input type="password" name="password" placeholder="Enter your Password" required />
                <button type="submit">Login</button>
            </form>
            <div class="signup-link">
                New here? <a href="signup.php">Create an account</a>
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