I have a lot of information on various topics/domains. I have written into markdown files. I need a way to:
- anonymously/publicly view them over the internet
- with pretty aesthetics and rendered, beautiful, modern form
- with excellent organization

Here is what I currently have:
I use a dedicated S3 bucket to host and serve a static website through cloudfront. Every new topic/domain gets a dedicated route of form /<name/reference to topic>/. For instance, the full URL for notes/information related to say maintaining/building expenditure records/planning for my household would be: "https://<cloudfront domain name>/household-expenditure/", or simply "https://<cloudfront domain name>/house-exp/". All information is stored in markdown files with appropriate prefixes in the bucket. The website is just a static "index.html" page. Upon a hit, the HTML page is served. The HTML page then fetches a JSON file. The JSON file contains paths to relevant markdown content with proper prefixes. Then HTML page fetches the content and renders and displays it. When I need to update my website, I just upload to the bucket. The HTML page uses custom CSS.


This worked well, but its extremely rudimentary and primitive:
- creating and maintaining new routes is a major hassle. I have tried to automate it with bash, but it remains a hassle. thus, more generally, adding new topics/information is a hassle
- building and maintaining JSON file. I have automated this as well, but the automation is extremely dumb and just overwrites everything in the JSON file for changes. Meaning every once in a while, I would have to manually maintain the JSON file. Again not ideal
- since I use only root level, very limited scalability. I would need to use more obscure/creative/non-sequitur names in future for newer topics
- Multiple related markdown files are required to be displayed on the same page. I can dedicate dedicated pages to every markdown file, but that would be a nightmare to build and maintain.
- No "preview"/"home page". I don't have trouble remembering the routes, but that would be needed for what I want (more on it in a moment)
- Custom CSS looks reasonably good, but is not perfect. Ocassionally can look bad


Let me illustrate what i actually want with example. Suppose I have a topic "personal finance". On that I have files: "how to plan expenditure for your household", "build a diversified investment portfolio", "overview of various investment classes (gold, bonds, equity, real estate, etc.)", etc. What I would want is:
- https://<cloudfront domain name>/ would display a list of all topics. In this case, the home landing page would include link: "Personal Finance". Cicking on the link will take me to "Personal Finance" topic. Example link to personal finance topic: https://<cloudfront domain name>/personal-finance-optional-unique-numeric-identifier/
- On landing page for personal finance, there would be list of all articles and optionally with a brief overview. So the landing page for personal finance would include articles: "planning household expenditure: <brief overview/summary>", "investment classes for individuals: <brief overview/summary>", "building a diversified investment portfolio for individuals: <brief overview/summary>"
- Then clicking on specific article will take me to the corresponding article.
- publily accessible over internet
- pretty, modern, beautiful aesthetics and design for the article display. should look good
- Support for even more levels of nesting
- seamless, hassle-free creation and updating of information, needing very minimal human interference/labor
- out-of-the-box good looking/pleasing/attractive rendering of content and broader website



Basically a more robust, scalable directory-like tree structure for organizing my information.

Suggest me a solution. Your solution can be:
- Existing product/service, ideally free
- Github project/repo
- Existing open-source project
- Custom full-blown web application using API Gateway, Lambda, etc.

I have minimal desire to dedicate a lot of effort on this. So custom full-blown web app should remain last resort. Thoroughly and exhaustively search the internet for existing existing/prebuilt solutions before suggesting custom one.

I think blogger is a reasonable solution. It does not have explicit "directory-like" organization, but I think tags can build a rudimentary/primitive form of organization. 








