const playlistLinks = [
    'https://www.youtube.com/playlist?list=PL5WDcBjA0p6E00I31haEGiMXPyLN9_pTu',
    'https://www.youtube.com/playlist?list=PLUl4u3cNGP62UTc77mJoubhDELSC8lfR0'
];

async function fetchVideosFromPlaylist(playlistUrl) {
    console.log(`Starting to fetch videos from playlist: ${playlistUrl}`);
    try {
        const response = await fetch(playlistUrl);
        if (!response.ok) {
            console.error(`Error fetching playlist: ${response.status} ${response.statusText}`);
            return;
        }

        console.log(`Successfully fetched playlist HTML for: ${playlistUrl}`);
        const text = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');

        // Fetch the playlist title from the <title> tag
        const titleElement = doc.querySelector('title');
        const playlistTitle = titleElement ? titleElement.innerText : 'Unknown Playlist Title';
        console.log(`Playlist Title: ${playlistTitle}`);

        // Use the provided CSS selector to fetch video links
        const videoLinks = doc.querySelectorAll('ytd-playlist-video-renderer h3 > a#video-title');
        console.log(`Found ${videoLinks.length} video links in playlist: ${playlistUrl}`);

        if (videoLinks.length === 0) {
            console.warn(`No video links found in playlist: ${playlistUrl}`);
        } else {
            videoLinks.forEach(link => {
                const videoUrl = link.href.split('&list=')[0]; // Clean up the URL
                const title = link.innerText || link.title;
                console.log(`Video Title: ${title} | Video Link: ${videoUrl}`);
            });
        }
    } catch (error) {
        console.error(`Failed to fetch from ${playlistUrl}: ${error.message}`);
    }
}

// Fetch videos from both playlists
playlistLinks.forEach(link => {
    console.log(`Processing playlist link: ${link}`);
    fetchVideosFromPlaylist(link);
});
