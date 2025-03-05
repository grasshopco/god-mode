# Enhanced Prompts History

## Current Enhanced Prompt

*Last Updated: 2025-03-04 19:24:15*

The user requires detailed updates to the God Mode system to enforce a consistent workflow that includes:

1. Using XML-style tags (<TAG>content</TAG>) exclusively in all responses
2. Updating the script_prepare_response.sh to reference XML tags instead of bracket-style tags
3. Modifying the Cursor rules file to include a detailed step-by-step workflow
4. Implementing a proper prompt enhancement system that:
   - Stores verbatim user messages
   - Creates enhanced versions with additional context
   - Maintains versions in prompt_enhanced.md
   - Uses the enhanced prompt as the basis for responses
5. Ensuring the auto-commit script properly routes XML-tagged content verbatim
6. Updating documentation in memory_features.md and both documentation files
7. Maintaining the roadmap with completed and new tasks

The key insight is that content should be preserved VERBATIM without interpretation - we should be "literally taking chunks of your message and we're just taking the literal words verbatim from your message and filing them off in the correct memory files."

## Version History

### Version 1710485055 - 2025-03-04 19:24:15

**User's Message:**
```
You need to update the script_prepare_response.SH file such that where it says to remember how to include the appropriate tags it needs to be changed to the XML bracket blocks style while still detailing, which of the appropriate tags to include, including the multi tag and correctly, noting it as "feature" tag instead of "feature_log" tag

The first thing you did was the script prepared response. The next step you did was incorrect. You need to please refer to the message I gave you above of the exact process you're supposed to go through. I'm going to copy and paste it again below. The cursor rules file needs to get updated accordingly, so this doesn't happen again with incorrect ordering of what you're supposed to do or missing steps. And the prompt enhancement file will obviously need to get updated because you missed something because you didn't even check to look at the enhance prompt MD file.

here's what i said above, once more:

OK. This is what we need to do. One we have to update your cursor rules file such that it tells you to put the XML bracket blocks in every single response. Then you're going to give your response. Then at the end of your response, the cursor rules file is going to tell you that you need to allow me to run a script. This script will do a handful of things things.

The first thing that I will do is that I will look at your response and look at all the different tag blocks. Then it's going to route the text in between each of the tag blocks as well as my entire response to the corresponding file that corresponds to that tag block. It is going to do this for all of the tag blocks in your response. That means that my message will get sent to every single one of these files along with the text in each of those tag blocks.

The second thing that this script at the end of the response that has been given to me to run will do is that it will do the GIT commit.

The third thing that, I am not sure if it's actually possible, but the third thing that it's supposed to do at the end is that it needs to force you the AI to do the enhancement to the prompt enhancer file. That way it fills any gaps that were identified in the message. WAIT I KNOW HOW TO MAKE IT WORK. In your Cursor rules file there needs to also be a step in there that says that you need to include a prompt enhancement tag block. In this block will basically be you writing about your assessment of YOUR PREVIOUS RESPONSE (not the current one) IN RELATION TO MY MESSAGE THAT FOLLOWED IT. 
@script_enhance_prompt.py @script_enhance_message_content.py @script_enhance_prompt.py 

Then I am going to send you a message and when I hit send what needs to happen is that in your Cursor rules file it needs to say that you must look at the prompt enhancement file, which might actually need to be a "MD "file rather than a script or py file (however the script is editing /making additions to this prompt enhancement MD file).

And in the Cursor rules, it says that the first thing you have to do is take my message and input it into a file, Word for Word verbatim, and then below that it needs to add the enhanced version of that message of mine based on the prompt enhancement MD file.

The enhance prompt also needs to be added to another file where, at the very top is the most recent version of the enhanced prompt and below that is a running log of all the versions of the enhance prompt and you will need to update at the very top of the enhanced prompt and add to at the very bottom, the latest enhanced prompt.

Then your Cursor rules file needs to say that you need to look at this enhanced prompt MD file where all of the stuff is saved, and it needs to grab and look at the very top part where the most recent version of the enhanced prompt is. Then it needs to use that to base its response off of.

Then, it needs to also tell you in the Cursor rules file that you must look at roadmap plan file, which should be a file that has the entire roadmap. Then, what you must do is that the Cursor rules file needs to tell you that at the bottom of this roadmap file needs to be added all the things that need to be done THAT ARE NEW THINGS NOT ON THE ROADMAP FILE, but if it is already on the roadmap, then a bullet point needs to be added the issue that occurred based off my message to you in terms of the thing in that roadmap list item did or didn't go wrong or if it went right in the bullet point needs to be added, and the roadmap item needs to be checked off.

roadmap template is here: @template_roadmap_plan_update.md 

Then after this roadmap file has been updated. You will then begin your response to me with all of the message stuff with everything in the appropriate tag blocks and then everything else will continue in a loop as i have described above.

this should mean is that because we're literally snipping chunks of your message and we're just taking the literal words verbatim from your message and filing them off in the correct memory files and other appropriate files, then based off that logic we probably don't need those scripts that have to do assigning meaning to those things since we're literally just taking the words verbatim from your response along with my message that provoked your response.

We also need to make sure of a few more things in your Cursor rules file, which needs to be added in this roadmap overhaul system file. In the Cursor rules file it should say that just before you are told in your step-by-step list of what to do, the step before you're supposed to give the final script to auto run everything, this step before this you need to be instructed to add to the features file in the memory features file that way we have the running list of all of the features. Each feature in there should have just a small summary of what that feature is doing. If the feature already exists in the file, don't write it again.

n the Cursor rules file it needs to say before you run the last script and after you updated the individual features file, you need to update the meory documentation summarized file and the memory documentation detailed file.


This was verbatim what I told you as your instructions and the order of which to do it. I don't understand why it wasn't done properly. And why stuff was skipped. Does the Cursor rule file outline this extreme detailed exactly how to do this step-by-step? Yes or no? It needs to be exact like a very structured way of doing it. I need to be able to literally see every time in your response to the beginning that after you run the script response prepare that the next thing you're doing is that you're reading the enhance prompt file end reading at the very top, the enhanced prompt, and at the bottom of the file, you are adding to the list my exact message I sent to you along with the enhanced prompt that is taking that information from my message and enhancing it. This should all be done in the @prompt_enhanced.md file
```

**Enhanced Prompt:**
The user requires detailed updates to the God Mode system to enforce a consistent workflow that includes:

1. Using XML-style tags (<TAG>content</TAG>) exclusively in all responses
2. Updating the script_prepare_response.sh to reference XML tags instead of bracket-style tags
3. Modifying the Cursor rules file to include a detailed step-by-step workflow
4. Implementing a proper prompt enhancement system that:
   - Stores verbatim user messages
   - Creates enhanced versions with additional context
   - Maintains versions in prompt_enhanced.md
   - Uses the enhanced prompt as the basis for responses
5. Ensuring the auto-commit script properly routes XML-tagged content verbatim
6. Updating documentation in memory_features.md and both documentation files
7. Maintaining the roadmap with completed and new tasks

The key insight is that content should be preserved VERBATIM without interpretation - we should be "literally taking chunks of your message and we're just taking the literal words verbatim from your message and filing them off in the correct memory files."

### Version 1 - 2025-03-04 17:56:10

The user wants to implement a fully automated God Mode system that:

1. Uses XML-style tags exclusively (<TAG>content</TAG>) in all responses
2. Processes these tags to route content to appropriate memory files
3. Enhances user prompts with context and improves them over time
4. Tracks roadmap progress and updates tasks automatically
5. Runs scripts before and after responses (prepare_response.sh and auto_commit.sh)
6. Creates a self-improving system that maintains its own documentation

The enhanced workflow should be:
- Before responding: Run script_prepare_response.sh
- When responding: Use XML-style tags for all content
- After responding: Run script_auto_commit.sh to process tags
- Regularly: Update roadmap with progress and new tasks

Focus on fixing indentation errors in script_enhance_message_content.py and adding XML tag processing to the message router.


