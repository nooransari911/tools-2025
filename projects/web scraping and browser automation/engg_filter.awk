BEGIN {
    RS = "\n"      # Record separator: Two newlines
    FS = ": "        # Field separator: Single newline
    IGNORECASE = 1   # Make regex case-insensitive
}


# {
#   print $2 ": " $1
# }



# Process the "Ilist.txt" file
{
    # Apply the usual filter and ensure the line is not in "Iapplied.txt"
    if ($1 !~ /reseller|e-commerce|ecommerce|e commerce|purchase|listing|product listing|advertise|advertising|affiliate|marketing|brand|sales|growth|lead generation|campaign|email|business development|field executive|relations|relationship|call|telecall|cold call|tele|campus ambassador|environmental|environment|hr|finance|accounting|account|inventory|import|export|nodal|operation|credit card|journalism|law|legal|political|public policy|fashion|interior|architecture|psychology|mental|physiotherapy|physio|humanities|counsellor|project management|product management|travel|tourism|human resources|talent|career associate|assistant|secretary|yoga|nutrition|diet|food|veterinary|fundraising|public relations|customer service|customer support|customer|customer success|quality|volunteer|charity|social|community|crowd|reels|instagram|youtube|shorts|lofi|playlist|facebook|video|audio|adobe|anchor|host|stage|event|blog|content|artist|art|graphic|visual|logo|animation|blender|speech|music|editing|writing|writer|creative|copywriting|resume|cv|data entry|typing|translate|transcription|subject matter expert|language|trainer|tutor|teach|education|edtech|edutech|school|tamil|regional|mentor|youth|young|student|biology|french|mathematics|upsc|uspc|prelims|cybersecurity|cyber security|blockchain|trader|trading|trade|mobile|android|ios|game|c\+\+|2D|3D|QA|quality|test|response|rate|rating|evaluate|front end|ui|ux|java|react|wordpress|figma|framer|php|laravel|mern|flutter|nodejs|node\.js|shopify|power bi|\.net|c#/ && $2 !~ /aadhvik|mentorboxx|pawzz|remote-internship|welfare|society|foundation|school|college|education|edtech|edutech/) {
            print $0
    }
}
