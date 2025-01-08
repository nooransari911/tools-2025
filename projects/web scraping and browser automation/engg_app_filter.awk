BEGIN {
    RS = "\n"      # Record separator: Newline
    FS = ": "      # Field separator: Colon and space
    IGNORECASE = 1 # Case-insensitive regex matching
}

# Read the "Iapplied.txt" file and store its entries in an array
FNR == NR {
    applied[$0]     # Store each line from "Iapplied.txt" as a key in the array
    next            # Move to the next record in "Iapplied.txt"
}

# Process the "Ilist.txt" file
{
    # Apply the usual filter and ensure the line is not in "Iapplied.txt"
    if ($1 !~ /reseller|e-commerce|ecommerce|e commerce|purchase|listing|product listing|advertise|advertising|affiliate|marketing|brand|sales|growth|lead generation|campaign|email|business development|field executive|relationship|call|telecall|cold call|tele|campus ambassador|environmental|environment|hr|finance|accounting|account|inventory|import|export|nodal|operation|credit card|journalism|law|legal|fashion|interior|architecture|psychology|mental|humanities|project management|product management|travel|tourism|human resources|talent|assistant|secretary|yoga|nutrition|diet|veterinary|fundraising|public relations|customer service|customer support|customer|customer success|quality|volunteer|charity|social|community|crowd|reels|instagram|youtube|shorts|lofi|playlist|facebook|video|audio|anchor|host|stage|event|blog|content|graphic|logo|animation|blender|speech|music|editing|writing|writer|creative|copywriting|data entry|typing|translate|transcription|subject matter expert|language|trainer|tutor|teach|mentor|youth|young|student|biology|french|mathematics|upsc|uspc|prelims|cybersecurity|cyber security|blockchain|trader|mobile|android|ios|game|c++|2D|3D|front end|ui|ux|java|react|wordpress|php|laravel|mern|flutter|nodejs|node\.js|shopify|power bi/ && $2 !~ /aadhvik|mentorboxx|pawzz/) {
        if (!($0 in applied)) {
            print $0
        }
    }
}
