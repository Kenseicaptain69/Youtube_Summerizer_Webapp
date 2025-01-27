<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Summarizer - Dashboard</title>
    <link rel="stylesheet" href="static/styles.css">
    <script>
        async function summarize() {
            const url = document.getElementById('url').value;
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            const result = await response.json();

            const summaryDiv = document.getElementById('summary');
            if (response.ok) {
                summaryDiv.textContent = result.summary;
            } else {
                summaryDiv.textContent = result.error;
            }
        }
    </script>
</head>
<body>
    <div class="container-dashboard">
        <h1>Enter your YouTube URL</h1>
        <form id="dashboard" onsubmit="event.preventDefault(); summarize();">
            <input type="url" id="url" placeholder="Enter your YouTube URL" required>
            <button type="submit">Summarize</button>
        </form>
        <div id="summary" style="margin-top: 20px; color: blue;"></div>
    </div>
</body>
</html>




<!-- <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Summarizer - Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    <script>
        async function summarize() {
            const url = document.getElementById('url').value;
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            const result = await response.json();

            const summaryDiv = document.getElementById('summary');
            if (response.ok) {
                summaryDiv.textContent = result.summary;
            } else {
                summaryDiv.textContent = result.error;
            }
        }
    </script>
</head>
<body>
    <div class="container-dashboard">
        <h1>Enter your YouTube URL</h1>
        <form id="dashboard" onsubmit="event.preventDefault(); summarize();">
            <input type="url" id="url" placeholder="Enter your YouTube URL" required>
            <button type="submit">Summarize</button>
        </form>
        <div id="summary" style="margin-top: 20px; color: blue;"></div>
    </div>
</body>
</html> -->
