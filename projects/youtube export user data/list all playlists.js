let allVideosData = [];

// Function to fetch video titles and links from a playlist
async function fetchVideosFromPlaylist(url) {
    const response = await fetch(url);
    const text = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, 'text/html');

    let arrayVideos = [];
    const links = doc.querySelectorAll('a#video-title');

    links.forEach(link => {
        arrayVideos.push(`${link.title};${link.href.split('&list=')[0]}`);
    });

    let data = arrayVideos.join('\n');
    allVideosData.push(`Playlist: ${url}\n${data}\n\n`);
}

// Main function to process all playlists
async function processPlaylists(playlistLinks) {
    for (const link of playlistLinks) {
        await fetchVideosFromPlaylist(link);
    }

    // Create CSV
    const finalData = allVideosData.join('\n');
    const blob = new Blob([finalData], { type: 'text/csv' });
    const elem = document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = 'list-all-playlists.csv';
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);
}

// Select all playlist links again (if necessary)
const playlistElements = document.querySelectorAll('ytd-rich-item-renderer a.yt-core-attributed-string__link');
const allLinks = Array.from(playlistElements).map(link => link.href);
const playlistLinks = allLinks.filter(link => !link.includes('/@'));

// Execute the processing function
processPlaylists(playlistLinks);
