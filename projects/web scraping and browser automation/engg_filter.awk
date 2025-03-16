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
    if ($(NF-1) !~ /reseller|e-commerce|ecommerce|e commerce|purchase|listing|product listing|advertise|advertising|affiliate|marketing|brand|sales|growth|lead generation|campaign|email|business development|field executive|relations|relationship|call|telecall|cold call|tele|campus ambassador|hr|human resources|human resource|talent|recruitment|hiring|onboarding|operation|project management|product management|assistant|founders office|founder office|founder's office|consult|secretary|career associate|administration|sponsor|management|loan|finance|accounting|account|inventory|import|export|credit card|journalism|law|legal|compliance|dispute resolution|environmental|environment|nodal|political|public policy|fashion|interior|architecture|design|product design|CAD|AutoCAD|mechanical engineering|psychology|mental|dental|physiotherapy|physio|humanities|counsellor|counselling|wellbeing|travel|tourism|hospitality|yoga|nutrition|diet|food|culinary|veterinary|fundraising|public relations|pr|communications|customer service|customer support|customer|customer success|client relations|chat support|chat|quality assurance|qa|volunteer|charity|social work|social impact|community|crowd|acting|media|social media|influencer|reels|reel|instagram|youtube|shorts|lofi|playlist|facebook|linkedin|video|audio|content creation|adobe|anchor|host|stage|event|event management|blog|content|content writing|artist|art|photography|illustration|illustrator|thumbnail|graphic|visual|logo|animation|blender|creative arts|speech|music|editing|writing|writer|creative|copywriting|content editing|resume|cv|data entry|typing|translate|translation|transcription|caption|proofreading|subject matter expert|sme|language|trainer|tutor|teach|faculty|education|edtech|edutech|school|college|university|tamil|regional|mentor|youth|young|student|doubt|english|biology|chemistry|physics|french|mathematics|math|upsc|uspc|prelims|competitive exams|cybersecurity|cyber security|blockchain|cryptocurrency|trader|trading|trade|stock|stock market|foreign exchange|mobile|android|ios|game|game development|c\+\+|2D|3D|test|testing|response|rate|rating|evaluate|front end|ui|ux|user interface|user experience|java|javascript|react|wordpress|SEO|search engine|figma|framer|php|laravel|mern|flutter|nodejs|node\.js|shopify|power bi|data analyst|data analytics|data mining|\.net|c#|sql|full stack web dev|full stack development|market research|business research|course developer/ && $(NF) !~ /bangalore|chennai|delhi|gurgaon|noida|aadhvik|mentorboxx|pawzz|remote-internship|request-it-support|big-bulls|zean-lithos|lawtech|welfare|society|foundation|school|college|education|edtech|edutech|edu/) {









    
        print $0
    }
}
