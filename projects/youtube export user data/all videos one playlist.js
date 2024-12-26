var links = document.getElementsByTagName("a");
var csvContent = "data:text/csv;charset=utf-8,Title,Link\n"; // CSV header
var videoLinks = new Set(); // Set to store unique video links

for (var i = 0; i < links.length; i++) {
    if (links[i].href.includes("watch?v")) {
        var title = links[i].innerText; // Get the title from the anchor text
        var url = links[i].href; // Get the URL
        csvContent += `${title},${url}\n`; // Append the title and URL to the CSV string
        videoLinks.add(url); // Use a Set to ensure uniqueness
    }
}

// Create a downloadable link
var encodedUri = encodeURI(csvContent);
var downloadLink = document.createElement("a");
downloadLink.setAttribute("href", encodedUri);
downloadLink.setAttribute("download", "youtube_links.csv"); // Filename for download
document.body.appendChild(downloadLink); // Required for Firefox

downloadLink.click(); // Trigger the download
document.body.removeChild(downloadLink); // Clean up

// Print the length of unique video links
console.log(`Total unique video links collected: ${videoLinks.size}`);
