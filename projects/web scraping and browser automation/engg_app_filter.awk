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
    if ($1 !~ /reseller|e-commerce|ecommerce|e commerce|purchase|listing|product listing|advertise|advertising|affiliate|marketing|brand|sales|growth|lead generation|campaign|email|business development|field executive|relations|relationship|call|telecall|cold call|tele|campus ambassador|hr|human resources|human resource|talent|recruitment|hiring|onboarding|operation|project management|product management|assistant|secretary|career associate|administration|finance|accounting|account|inventory|import|export|credit card|law|legal|compliance|dispute resolution|environmental|environment|nodal|political|public policy|fashion|interior|architecture|design|product design|CAD|AutoCAD|mechanical engineering|psychology|mental|physiotherapy|physio|humanities|counsellor|counselling|wellbeing|travel|tourism|hospitality|yoga|nutrition|diet|food|culinary|veterinary|fundraising|public relations|pr|communications|customer service|customer support|customer|customer success|client relations|chat support|chat|quality assurance|qa|volunteer|charity|social work|social impact|community|crowd|social media|reels|instagram|youtube|shorts|lofi|playlist|facebook|linkedin|video|audio|content creation|adobe|anchor|host|stage|event|event management|blog|content|content writing|artist|art|illustrator|graphic|visual|logo|animation|blender|creative arts|speech|music|editing|writing|writer|creative|copywriting|content editing|resume|cv|data entry|typing|translate|translation|transcription|proofreading|subject matter expert|sme|language|trainer|tutor|teach|education|edtech|edutech|school|college|university|tamil|regional|mentor|youth|young|student|intern|biology|chemistry|physics|french|mathematics|math|upsc|uspc|prelims|competitive exams|cybersecurity|cyber security|blockchain|cryptocurrency|trader|trading|trade|stock market|mobile|android|ios|game|game development|c\+\+|2D|3D|test|testing|response|rate|rating|evaluate|front end|ui|ux|user interface|user experience|java|javascript|react|wordpress|figma|framer|php|laravel|mern|flutter|nodejs|node\.js|shopify|power bi|\.net|c#|sql|software development|web development|programming|coding|full stack web dev\.|market research|business research|course developer|photography|journalism/ && $2 !~ /aadhvik|mentorboxx|pawzz|remote-internship|welfare|society|foundation|school|college|education|edtech|edutech/) {
        if (!($0 in applied)) {
            print $0
        }
    }
}
