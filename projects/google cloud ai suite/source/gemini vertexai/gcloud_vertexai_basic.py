# Use wire project only
import time

import vertexai
from vertexai.language_models import TextGenerationModel


time_start = time.time_ns()


# TODO(developer): update project_id & location
vertexai.init(project="optimum-task-411411", location="us-west1")

parameters = {
    "temperature": 0,
    "max_output_tokens": 256,
    "top_p": 0.95,
    "top_k": 40,
}

"""
for deterministic prompts like classification, detection, extraction, using
temperature = 0,
top-K = 1
"""



model = TextGenerationModel.from_pretrained("text-bison@002")
prompt = "Provide a summary of this"
reference = """
A NOTE ON PICKING UP SKILLS On getting started: This is the step where you will face the most inertia, as there will always be a college assignment, an old project that will take priority unless you take a hard call that you need to excel and land this role in the next 6 months anyhow. Don't get stuck in analysis paralysis, in life the speed of decisions is as important as the quality of your decisions. If you're under the age of 24, losing 3-6 months to a skill that can has potential to make you 5-6L in the next one year is a better bet than a college project from a tier 3 project. On learning: Learning isn't always meant to be fun; it should feel like hard work. There are a lot of videos on YouTube etc. that give the appearance of education, but if you look closely they are really just entertainment. This is very convenient for everyone involved: the people watching enjoy thinking they are learning (but actually they are just having fun). So make sure you're not just pseudo learning the skill we only have 3-6 months! If you're an individual who is not self motivated join online communities where you can learn in a group or with a partner, there are enough and more discord communities of students upskilling and sharing progress with each other On building portfolio & posting on social media: Don't wait for you to become the best in the field, start posting your work as soon as you have learnt the basics, this will show your progress on how you went from point A to point B. This will also put social pressure and hold you accountable to keep getting better as you share your work with the world. Posting your work on social media also increases chances of a recruiter stumbling upon your work and reaching out to you, it increases your surface area of luck. Create a kickass portfolio using canva/ framer/webflow/ or any no- code website platforms that are easy to use. Show your work but also make your personality stand out -- here's a portfolio I received few years back that I really liked (https://aaryamanbasu.com/ please don't spam this person :P) On cold outreaches: Remember the other person has no idea who you are, so worst thing that you'll get from the outreach is a no reply. Write the best email about yourself and how your skills help this other person's company's needs. Use Chat gpt or claude to give you ideas and improve your personal voice. On networking: Think of your network as leverage. Most hires in startups are made through connections, with people bringing in others they know. Companies even pay bonuses for good referrals. By building a strong network within top startups, you make it easier for them to bring you on board. Leverage your network to get introductions, referrals, and insider info. This is not just about knowing people, but about being known by the right people. Your network can be the difference between struggling to find a job and having multiple offers on the table! On AI: Most people around you are still very slow to adopt AI, but if you can leverage these tools to improve workflows, the hard work you need to put in can be reduced by 50%. This makes you far more valuable to any company, as you possess specific knowledge that others don't. By using AI tools in your specific role, you can accomplish more work in less time. Don't sleep on AI tools - if you can pick them up right now, you'll be far ahead of your peers and significantly more valuable to companies. Something I read recently: "Undergrads tend to have tunnel vision about their classes. They want to get good grades, etc. The crucial fact to realize is that no one will care about your grades unless they are bad. For example, I always used to say that the smartest student would get 85% in all of his courses. This way, you end up with somewhere around a 4.0 score, but you did not over-study, and you did not under-study. Your time is a precious, limited resource. Get to a point where you don't screw up on a test and then switch your attention to much more important endeavors. What are they? Getting actual, real-world experience, working on real code bases, projects, or problems, outside of silly course exercises is extremely important. Get out there and create (or help create) something cool. Document it well. Blog about it. These are the things people will care about a few years down the road. Your grades? They are an annoyance you have to deal with along the way. Use your time well and good luck." - Andrej Karpathy
"""


response = model.predict ("".join ([prompt, reference]))
print (f"\n\n\n\n{response.text}")
time_end = time.time_ns()
elapsed_time = (time_end - time_start) / (10**9)
print (f"\nSummarize text string; Bison model;\nElapsed Time for Bison model: {elapsed_time} seconds;\n")

"""
------------------------------------------------------------------
------------------------------------------------------------------
------------------------------------------------------------------
------------------------------------------------------------------
"""


import vertexai
from vertexai.generative_models import GenerativeModel, Part

time_start = time.time_ns()

vertexai.init(project="optimum-task-411411", location="us-west1")

model = GenerativeModel("gemini-1.5-flash-001")

response = model.generate_content(
    "".join ([prompt, reference])
)

print (f"\n\n\n\n{response.text}")

time_end = time.time_ns()
elapsed_time = (time_end - time_start) / (10**9)
print (f"\nSummarize text string; Gemini 1.5 Flash model;\nElapsed Time for Gemini 1.5 Flash model: {elapsed_time} seconds;\n")


"""
------------------------------------------------------------------
------------------------------------------------------------------
------------------------------------------------------------------
------------------------------------------------------------------
"""



import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="optimum-task-411411", location="us-west1")
model = GenerativeModel("gemini-1.5-pro-001")
prompt = "briefly describe this "

"""
------------------------------------------------------------------
------------------------------------------------------------------
"""


time_start = time.time_ns()

video_file = Part.from_uri(
    uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
    mime_type="video/mp4",
)
video_contents = [video_file, prompt+"video"]
response = model.generate_content(video_contents)
print (f"\n\n\n\n{response.text}")
time_end = time.time_ns()
elapsed_time = (time_end - time_start) / (10**9)
print (f"\nDescribe video; Gemini 1.5 Pro model;\nElapsed Time for Gemini 1.5 Pro model: {elapsed_time} seconds;\n")


"""
------------------------------------------------------------------
------------------------------------------------------------------
"""


time_start = time.time_ns()

image_file = Part.from_uri(
    "gs://cloud-samples-data/generative-ai/image/scones.jpg",
    mime_type="image/jpeg",
)
image_contents = [image_file, prompt+"image"]
response = model.generate_content(image_contents)
print (f"\n\n\n\n{response.text}")
time_end = time.time_ns()
elapsed_time = (time_end - time_start) / (10**9)
print (f"\nDescribe image; Gemini 1.5 Pro model;\nElapsed Time for Gemini 1.5 Pro model: {elapsed_time} seconds;\n")

"""
------------------------------------------------------------------
------------------------------------------------------------------
"""


"""
model = GenerativeModel("gemini-1.5-pro-001")

prompt = prompt
For video: Provide a description of the video.
The description should also contain anything important which people say in the video.

video_file = Part.from_uri(
    uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
    mime_type="video/mp4",
)
image_file = Part.from_uri(
    "gs://cloud-samples-data/generative-ai/image/scones.jpg",
    mime_type="image/jpeg",
)

contents = [video_file, prompt]
contents = [image_file, prompt]

response = model.generate_content(contents)

"""