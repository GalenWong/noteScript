# NoteScript
LA Hacks 2018
By: Devyan Biswas, Galen Wong, Rishab Sukumar, Siddarth Joshi

### NoteScript is our solution to note-taking in class. 

UCLA spends a lot of money on hiring notetakers. To save the unnecessary spending, we created NoteScript to let technology handle the job of note taking.

### Inspiration
Our inspiration for this project comes from the following:

The Centre of Accessible Education at UCLA spends thousands of dollars every year to hire notetakers for students who are unable to do so themselves. Our app works to solve this fundamental problem of interpreting the information of a lecture into concise notes – potentially saving organizations like this across institutions of thousands of dollars.
Solves a pertinent problem for all college and school students who may struggle to catch when they miss class or are simply too lazy to take notes themselves :p

### What it does
Record a lecture or scan info and store text transcript using speech to text [API relevant here] -Using Google NLP API syntactically analyze transcript and identify key entities and their relative salient scores to determine the most important concepts in the transcript -We also use dependencies to map sentence structures -Using this information and the appropriate data structs(explained in detail below) to format and generate relevant notes for users to read through
### How we built it
-FrontEnd: A swift app that does Speech to Text recognition with Native Apple Swift Speech Module. Store the note into the user's iPhone database with Core Data module. -BackEnd: A django server with python script to analyze the text with Google Cloud Platform NLP API, and process it to output concise, formatted and organized notes.

#### LINGUISTIC ANALYSIS:
-Create dependency tree for individual sentences based on the syntactic analysis of GCP NLP API. -With the dependency tree, merge all subtree under the root node (root verb of the sentence) into a phrase, represented as an array of index. (e.g. [ [1, 2, 3], [5 ,6], [7, 8, 9, 10] ]) -Analysis each sub-phrase to check their grammatical function with Google's Syntactic Analysis, decide to remove it from the sentence or not. (PUNCT, CONJ are not very helpful in note abstracts) -Compile each sentence into a Tree structure

### Challenges we ran into
-Voice to text conversion does not punctuate the text. -We were unable to find an accurate punctuator API to punctuate entire transcripts -Figuring out how to represent sentences and develop logical relations that allow for easy traversal -Developing an algorithm to simplify and organize sentences by important concepts and the ideas that come under those headings

### Accomplishments that we're proud of
-Figuring out how to represent sentences and develop logical relations that allow for easy traversal -Developing an algorithm to simplify and organize sentences by important concepts and the ideas that come under those headings -We are proud of our packing of the api response -We are also proud of the organization of the information that Google’s API gives to create a graph that logically represents the relations between the nouns in the ‘lecture’ by classifying nouns as subjects and objects – depicting them as nodes with verbs that relate them being the edges connecting them.

-We are proud of networkx lib utilization for representing dependencies between subject/object nodes in graph structure -Visualization of the graph structure using matplotlib.pyplot, which was useful for debugging purposes(#kamada_kawai) 

## What we learned
-How to use Google's Natural Language API and how the information returned by it can be parsed and packed into custom data structures.

-How to represent logical relations between different syntactical elements of speech using a graph and how such a graph can be traversed to output a reasonably concise and organized version of this information. 

## What's next for NoteScript 
-Improving our parsing to make input information even more concise by using further heuristics to accurately represent relations represented by relational conjunctions and modifiers. While we had pseudocode to achieve this ready, due to the limited time we were unable to actually implement this. Such heuristics would allow us to not only take more concise notes but also process more complicated information. -Increasing functionality of the app for different media input -A cleaner and more accurate punctuator
