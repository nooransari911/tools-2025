BEGIN {
    RS = "\n"      # Record separator: Two newlines
    FS = ": "        # Field separator: Single newline
    IGNORECASE = 1   # Make regex case-insensitive
}


# {
#   print $2 ": " $1
# }



# Exclude unwanted roles based on title
{
    if ($1 !~ /(marketing|business development|lead generation|brand|campus|ambassador|sales|field executive|growth|hr|accounting|law|legal|fundraising|public relations|customer service|customer support|quality|volunteering|charity|social|reels|instagram|youtube|facebook|community|crowd|anchor|host|stage|2D|3D|content|translate|transcription|trader|blog|video|audio|graphic|animation|blender|editing|writing|creative|copywriting|subject matter expert|upsc|uspc|prelims|biology|nutrition|diet|french|language|trainer|front end|ui|ux|java|react|wordpress|android|ios)/)
        print $0
}
