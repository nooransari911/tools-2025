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
    if ($1 !~ /(marketing|business development|lead generation|brand|campus|ambassador|sales|field executive|growth|hr|accounting|law|legal|fundraising|public relations|customer service|customer support|quality|volunteering|charity|social|reels|instagram|youtube|facebook|community|crowd|anchor|host|stage|2D|3D|content|translate|transcription|trader|blog|video|audio|graphic|animation|blender|editing|writing|creative|copywriting|subject matter expert|upsc|uspc|prelims|biology|nutrition|diet|french|language|trainer|front end|ui|ux|java|react|wordpress|android|ios)/ && 
        !($0 in applied)) {
        print $0
    }
}
