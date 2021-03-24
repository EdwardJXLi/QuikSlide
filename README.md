# QuikSlide
An AI powered presentation generator that helps you create visual aids. Quikly.  
Hackathon Submission for Hack The North 2020++

## Disclaimer:
To safely remove keys and other private information, all sensitive content has been removed and all previous commits have been squashed down. Since keys were previously hardcoded (what did you expect it was a hackathon), the project most likely does not work out of the box. Some tinkering will be needed to get this server running! Nevertheless, the code is now public for archival purposes.  
> Security on the webserver was also not the greatest! Please do not use your bank password!!!

## Authors
* [Ayan Hafeez](https://github.com/ayan-dot) - Grade 12, Ottawa \
Backend, Frontend, API Integration, Slideshow Generation 

* [Edward Li](https://github.com/RadioactiveHydra) - Grade 11, Ottawa \
Backend, ML/NLP, Azure Infrastructure, Login System

* [Malav Mehta](https://github.com/malav-mehta) - Grade 12, Ottawa \
Backend, Frontend, Tokenizer, Google Slides API

# Project Information

Live Demo: https://quikslide.herokuapp.com  
Project Demo: https://vimeo.com/504236639  
Project Advertisement: https://vimeo.com/501433188  
Devpost Page: https://devpost.com/software/quikslide-qmphlr  

## Inspiration

**Quikslide** was ideated through a common problem that we had all faced in the past - creating effective slideshows under time constraints. Each team member agreed that a AI-Powered Presentation Generator that adaptively created slides based on an input script would be useful in many use cases, and thus Quikslide was born.

## What it does

Quikslide uses multiple refined APIs in delivering the final product, a complete slideshow, into your hands. The app first takes in speech input, either typed from your own notes, or spoken directly into the browser and processed through _web speech_. The app then summarizes and tokenizes text in order to come up with headers and body text (bullet points) for slides, and searches web browsers for relevant images to use as guidance for each slide. The presentation is created, designed, and shared with the user for further usage and alteration. We don't want to impede the creative process, but rather help the users on their way. On average, an employee uses approximately 10 hours to create a slideshow. By using our service, they are able to optimize out the tedious portions, allowing them to make beautful and dynamic presentations in the fraction of the time.

## How we built it

We first use the Chrome Adaptive Speech Recognition API to understand the users input. By processing the speech using the Azure Language Analytics Engine and the Azure Cognitive Engine, we are able to categorize data. We also integrated NLTK alongside the Azure Cognitive API to deliver precise and accurate text summarization. We then take this tokenized and summarized data to create lively slideshows using the Google Sides and Google Drive API. Then by using the Bing Search API, we are able to use our custom image searching algorithm to deliver precise and relevant images. By building our app with the Flask web-server, we are able to deliver high performance web throughput while creating a dynamic dashboard. We also used Flask-Login, SQLAlchemy, Jinja2, and NLP for the backend, and we used Html+CSS+jQuery to create the frontend.

## Challenges we ran into

As like any challenge, we faced any difficulties with a dynamic mindset. We had never used many of the technologies we needed to make our app a reality and it was a challenge to bring together unknown APIs in a limited time frame to create the final product. Specifically, we had issues with managing API call limits—such as the Google Drive share API—and with creating the summarization functions on our own with NLP, a library none of us had experience with. We also faced challenges tweaking the NLP Algorithms to deliver on high-percision analysis.

## Accomplishments that we're proud of

Quikslide's functionality is admirable for the early-stage development it has undergone. It can effectively seperate slides and categorize their titles based off of contextual tokenization that is done throughout the process. The slideshows are coherent and the formatting of the slide is consistent without overflows, or collisions. We're quite proud of the backend that was programmed on a really short time constraint, and we're confident that we're able to improve it for future purposes.

## What we learned

The biggest lessons we learned were the importance of being flexible with the scope of our project and altering it in favor of time and resource constraints.

We also learned:

- Flask
- SQLAlchemy
- Jinja
- NLP (text summarization, keyword extraction)
- Working with Azure Cognitive APIs
- Working with the Google Docs and Slides APIs
- Limiting API calls to avoid exceeding limits
- Working with Domains and DNS
- Power of working in a team

## What we improved

Over the course of this hackathon, we've improved the concept of QuikSlide significantly. The project, which was a very rough outline at its original submission hackathon has been fleshed out drastically. We improved not only processing for slideshow generation, but we _elaborated on the vision we had for the project_. Some of the alterations made are listed below:

- Improved speech summarization, using a custom summarization function implemented through **NLTK**.
- Improved image searching capabilities through altering API setup, using **SerpAPI** to run "smart" google searches to return relevant images
- Fixed crashes stemming from **Google Slides API** overloading on sharing limitations
- Added connectivity fixes, **eliminating 95% of crashes** stemming from API connections and otherwise.  
-Added loader for slideshow generation to improve fluidity of web application.
-Added minimums and maximums for speech input - avoids crashes
- Other QOL updates

The final product boasts significant growth from the original project, bringing QuikSlide closer to its intended proficiency level. With more relevant images due to Google's Image Indexing software, slideshows contain visual information that can aid the reader in comprehending the user's points. The improved summarization allows for more concise, and thematically correct points on the slideshows themselves. The improvement of the UI allows for a more pleasant user experience, in the hopes of increasing user retention and approval. We are very proud of the progress that has been made at XdHacks, and are excited for where QuikSlide takes us next!

## What's next for QuikSlide

We're excited to expand QuikSlide by increasing the configurations and slide templates that can be produced by our application. For example, we're looking to expand the theming available for our slideshows and adding company specific theming that adheres to design guidelines as well as expanding the generated content, through the addition of more variable templating and adding functionality for graphs and custom images. We also want to expand the natural language processing component so we can create more impactful slides—such as slides that focus on numbers—as well as more concisely shorten the summary of the script and automatically make bullet points more grammatically correct. Our vision for Quikslide is for it to become a product used by millions worldwide and which saves billions of hours of time and resources.
