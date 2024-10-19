<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>scotti Home Page</title>

    <link rel="icon" href="./images/scotti-logo.png" type="image/x-icon">

    <link rel="stylesheet" href="./styles/main.css">
    <link rel="stylesheet" href="./styles/support.css">

    <script src="./scripts/teammembers.js" defer></script>
</head>
<body>
    <header>
        <div class="logo-title">
            <img src="./images/scotti-logo.png" alt="scotti logo image">
            <h1>scotti</h1>
        </div>
        <div class="navigation-tab">
            <nav>
                <a href="./index.html">Home</a>
                <a href="./summarizer.html">Summarizer</a>
                <a href="./support.html">Support</a>
            </nav>
        </div>
    </header>
    <main>
    <?php
    // Check if the form was submitted
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        
        // Sanitize and retrieve the form data
        $name = htmlspecialchars($_POST['name']);
        $issueType = htmlspecialchars($_POST['issue-type']);
        $description = htmlspecialchars($_POST['description']);
        
        // Simple validation
        if (empty($name) || empty($issueType) || empty($description)) {
            echo "<p style='color: red;'>Please fill in all fields before submitting the form.</p>";
        } else {
            // Example: Display the form data back to the user
            echo "<h2>Thank you, $name, for submitting your issue.</h2>";
            echo "<p><strong>Issue Type:</strong> $issueType</p>";
            echo "<p><strong>Description:</strong></p>";
            echo "<p>$description</p>";

            // Example: Saving data to a file (optional)
            $file = fopen("support-requests.txt", "a");
            fwrite($file, "Name: $name\nIssue Type: $issueType\nDescription: $description\n\n");
            fclose($file);

            // Optionally, you could send the data via email (PHP mail function):
            // mail('support@yourdomain.com', 'New Support Request', "Name: $name\nIssue Type: $issueType\nDescription: $description");
        }
    }
    ?>

    </main>
    <footer>
        <div>
            <p>&copy scotti corporations - 2024</p>
        </div>
        <div class="socials">
            <a href="#"><img src="./images/instagramlogo.png" alt="instagram link image"></a>
            <a href="#"><img src="./images/twitterSlashXlogo.avif" alt="x link image"></a>
            <a href="#"><img src="./images/facebookicon.png" alt="facebook link image"></a>
        </div>
    </footer>
</body>
</html>