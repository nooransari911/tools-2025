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
    if ($1 !~ /marketing|brand|sales|growth|lead generation|business development|field executive|call|telecall|cold call|campus ambassador|hr|accounting|law|legal|fashion|interior|architecture|fundraising|public relations|customer service|customer support|quality|volunteering|charity|social|community|crowd|reels|instagram|youtube|shorts|lofi|playlist|facebook|video|audio|anchor|host|stage|blog|content|graphic|animation|blender|editing|writing|writer|creative|copywriting|data entry|translate|transcription|subject matter expert|language|trainer|teach|biology|nutrition|diet|french|upsc|uspc|prelims|front end|ui|ux|java|react|wordpress|android|ios|game|2D|3D|trader|flutter|nodejs|node\.js|shopify|power bi|human resources|humanities|yoga|operation/ && $2 !~ /mentorboxx/) {

        if (!($0 in applied)) {
            print $0
        }
    }
}
