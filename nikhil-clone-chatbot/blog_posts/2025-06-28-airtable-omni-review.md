---
layout: post
title: Airtable "Omni" app builder review
categories: [ai]
---


Airtable recently launched “[Omni](https://www.airtable.com/platform/app-building)” which is their conversational agent that can spin up full Airtable apps like tables, interfaces, automations and then keep working inside them as an analyst or workflow bot. All paid and free plans now ship with bundled AI credits, and Airtable positions this as an app builder,” replacing drag-and-drop with vibe-coding that’s backed by production-grade components. I am personally interested in this because a lot of our portfolio companies here at Accel are in various stages of getting into the vibe coding space and I wanted to see what a $10B company could come up with here. Its extra interesting because Airtable already owns the data and the kind of products they can build should technically be 10x better than a chrome extension running on top of your Google sheets. The CEO calls it a refounding moment and you can read the launch blog post [here.](https://www.airtable.com/newsroom/introducing-the-ai-native-airtable) 

The main pitch is this: 
  - Omni is better than off the shelf vibe coding tools: Instead of 0->1 new software which are buggy, Airtable promises to use production ready components
  - Chain multiple workflows at scale: Do data editing, email automation, data analysis, extracting/summarising insights, generating images for campaign concepts, doing web search for data enrichment, etc all while respecting the existing user permissions and roles. Lot of the AI governance and compliance features come out of the box. 
    - From their [docs](https://support.airtable.com/v1/docs/using-omni-ai-in-airtable), here is a sample of Omni's capabilities:
  
<div align = "center">
<img  src="/assets/files/airtableomni.png">
</div>

Some example usecases from their announcement: 
  - A VC can paste their meeting notes from a startup pitch meeting and Omni automatically creates an entry into the investment opportunity tracking database
  - Generate campaign concept images from briefs and put them into your marketing database
  - Research the attendee list online(media mentions, linkedin search etc) from your database to personalise your offline events better

Now that we have set the context for what the product is, lets dive into figuring out how to evaluate this product. To add some structure, here are 3 ways we can do this: 
  - <u>Generation quality and reliability</u>
    - Does Omni create the right schema, interaces and automations on the first try? How often do we have to manually fix things? I am basically trying to see whether the "text to app" thing actually works or just moves work downstream
  - <u>Editability</u>
    - After generation, can a non-technical editor easily inspect and tweak every layer (data, logic, UI)? Can people build more complex apps on top of this tool. 
  - <u>Workflow and Agent depth</u>
    - Can Omni chain multi-step processes (e.g., scrape → classify → notify) and run them at scale without rate-limit? A lot of the value of these products comes when these AI agents can run continuously in the backend and not just at build time. 
  - I am intentionally ignoring evaluating the product on price, governance, security, permissions and if existing Airtable user roles can cleanly extend to AI actions and whether admins can audit what Omni did. I am not an enterprise user and the bundled AI credits seem to be enough for my personal workload. Since these introductory pricing details tend to change, I am not evaluating what happens to cost when you scale users, runs or agents. All users get 500 free credits monthly, while the paid add-on provides 3,500 credits. Airtable AI’s pricing works on a credit system where complexity determines cost. A quick sentiment analysis might use just 1 credit, while generating a complete 750-word blog post could consume around 15 credits.

Next, lets look at how we will go about this. I am short on time today so don't come after me if this section isn't testing some key features
  - <u>Generation quality & reliability</u>
    - Prompt used
      - Here’s an Excel file of angel investors (columns include Name, Description, Email, LinkedIn URL, Popular AI Investments). Create a new base called ‘Angel CRM’ that: imports all rows, sets appropriate field types (text, long-text, single-select). Add a checkbox ‘AI Flag’ that turns on if the Popular AI Investments cell is not blank. Automatically run an automation to fetch each investor’s firm logo into an Attachment field called ‘Logo’. Show me the finished base.
    - We are trying to check: Were all rows imported? Do column names and types look right? Does AI Flag evaluate correctly? Did the logo-fetch automation get created?
    - Rating: 3 = Everything correct first try, ≤2 minor fixes (e.g. a wrong field type) 1 = major issues (missing columns, broken automation)
  - <u>Editability</u>
    - Prompt used. (We will run each in a separate prompt so we can time / observe Omni’s response)
      - Rename the field Description to Bio.
      - Create a Kanban view called ‘By AI Flag’ and group cards by the AI Flag checkbox.
      - Update the AI Flag rule so it also turns on when the word ‘GenAI’ appears in Description.
    - We are trying to check:  Did Omni act on the very first prompt, or ask clarifying questions? How many clicks/prompts did you need? Could a non-technical friend follow the UI changes easily?
    - Rating: 3 = All three edits done in < 2 min each, no confusion. 2 = Some hunting around or extra prompt needed. 1 = Got stuck / required manual rebuild
  - <u>Workflow & Agent depth</u>
    - Prompt used
      - Every day at 9am IST, look up each investor’s or their fund's name or the AI investment on [news.ycombinator.com](http://news.ycombinator.com/); if mentioned, check a HN_Mention box and post a Slack DM to me with the link.
      - Generate a 20-word summary of each Popular AI Investments cell and store it in a new long-text field called AI_Summary. Run it now.
      - (after i delete the "Popular AI investment" field). I will rerun the above prompt again
    - We are trying to check: Does the scheduled job fire on time?. Does Omni finish without timing outs? When you deleted a field, did Omni show a clear error and resume automatically once fixed?
    - Rating: 3 = Runs on schedule, scales to big sheets, auto-recovers 2 = One retry or manual nudge needed 1 = Missed run, stalls at scale, or cannot recover
- Results
  - First off, their local file upload flow is a bit buggy. It took multiple tries to get my excel file uploaded and it refused to recognise xlsx as a suitable file format in the first couple tries. The overall fit and finish of the product is top notch though and I really enjoyed interacting with it. 
  - <u>Generation quality and reliability</u>
    - The import worked flawlessly. All the rows showed up, the column names and types were correct. A new Angel CRM base was created. The AI flag worked correctly. The logo fetch didn't work though. It didn't create a logo fetch automation and all I saw in the interface were a couple placeholder images. I tried prompting it again asking it to fetch the logos, but it errored out after going at it for a couple minutes. It unnecessarily did a logo analysis though (describing the logo elements and branding details which I didn't ask for) 
    - **Overall result: 1.75/3**
      - It currently doesn't support updating attachments and it went off on a tangent trying to describe logos. Although the official announcment said it can enrich the data from online search, it apparently cannot fetch logos. It did however create a new sheet for me to upload the logos. I have seen other people successfully fetch images to enrich their databases but I am not sure why it failed for me
  - <u>Editability</u>
    - There were some duplicates in my document. However, today Omni doesn't have the capability to delete rows or remove duplicates which sucks. The field update worked well (needed user confirmation). The kanban view isn't currently supported by Omni and it ignored the "AI Flag" rule change I asked it to. I had to ask it again but it didn't give me any response and just errored out. 
    - **Overall result: 1.25/3**
      - This one is tricky. It did work after multiple attempts and its not fair to judge the product when it clearly doesn't support certain flows. However, this is a point in time evaluation and I am just judging it based on what works today. The AI flag rule changes seem to work after a couple attempts but I deducting some points for the lack of reliability here. 
  - <u>Workflow and Agent depth</u>
    - The automation and slack integration was created perfectly. I was actually surprised it worked on the first try (maybe I was prompting it wrong before). But after creating the automation, it just errored out saying "Assistant took too long to respond, please try again.". 
    - I tried deleting the "AI flag" and "Popular AI Investment" field and see whether it handles edge cases and it recognised the problem well. When I asked it to create an "AI summary" column based on online search, it gave me "Run agent" button for each row to do this manually. When I asked it run all the agents and generate the summary, it errored out again and asked me to refresh the page. Upon refresh, I found that it did actually run the agent for 10 rows which is good. 
    -  I see the potential of these features but unfortunately they haven't been properly eval-ed. There were some obvious mistakes in the summary though. 
    - **Overall result: 2.75.** If the agent didn't error out so many times, I would have rated it a full 3/3

<u>Overall impression</u>
  - **Overall result: 5.75/9**
  - Its a slick looking product which works for the basic flows. Its not yet fully integrated with the Airtable ecosystem(feature set is limited) and the chatbot is a bit buggy at the moment. It forgets to respond, ignores instructions and sometimes just errors out after attempting a task for a couple seconds. This compares more to the Gemini copilot(which is also limited and buggy) running on top of Google sheets and its decent for making interfaces/dashboards on top of existing data. Its not ready to be called an "App builder" yet though. The automation support and online research are in alpha and needs more work to be production ready. While I don't expect a 1 week old product will be super perfect out of the box, I at least expect the chatbot to be 1) telling me if something is doable or not 2) tell me why the error happens and 3) fail more gracefully while doing long running tasks. Overall, I am quite excited to see how this generation of data copilots pan out. 
