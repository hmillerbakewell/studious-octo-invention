# Plan and progress

This file will show the thought trail for the project.

## The Idea

Part of modelling sentences as conceptual spaces involves treating words as functions.
For example: A noun word may take the form of a function from the monoidal unit to the Noun Space.

A harder example is with transitive verbs; in the paper [Bolt et al.] they are given the form $N \tensor S \tensor N$.
This form was chosen based on inspection of the sentence "Chickens cross roads."
The idea is to try and derive some notion of this structure from a large corpus of text.
The Brown Corpus ("Brown University Standard Corpus of Present-Day American English") is a readily available and well known corpus,
it has the added benefit of having each word tagged by Part Of Speech (POS).
There are, however, 81 such tags used in the Brown corpus, which may prove computationally burdensome.

The Brown Corpus will sit in the ./brown location relative to this file.
It will not be included in the repository, for reasons of space.
We are using it for reasearch, non-commercial purposes, abiding by:
https://creativecommons.org/licenses/by-nc/3.0/ (the license and source files are from: https://archive.org/details/BrownCorpus .)

### Example from the Corpus:

This example is taken from line 15 of ./brown/ca01.

~~~
The/at jury/nn said/vbd it/pps did/dod find/vb that/cs many/ap of/in Georgia's/np$ registration/nn and/cc election/nn laws/nns ``/`` are/ber outmoded/jj or/cc inadequate/jj and/cc often/rb ambiguous/jj ''/'' ./.
~~~

### Part Of Speech tags

The codes interpretations are the ones taken from Wikipedia, where they are presented without citation:

~~~
Tag 	Definition
. 	sentence (. ; ? *)
( 	left paren
) 	right paren
* 	not, n't
-- 	dash
, 	comma
: 	colon
ABL 	pre-qualifier (quite, rather)
ABN 	pre-quantifier (half, all)
ABX 	pre-quantifier (both)
AP 	post-determiner (many, several, next)
AT 	article (a, the, no)
BE 	be
BED 	were
BEDZ 	was
BEG 	being
BEM 	am
BEN 	been
BER 	are, art
BEZ 	is
CC 	coordinating conjunction (and, or)
CD 	cardinal numeral (one, two, 2, etc.)
CS 	subordinating conjunction (if, although)
DO 	do
DOD 	did
DOZ 	does
DT 	singular determiner/quantifier (this, that)
DTI 	singular or plural determiner/quantifier (some, any)
DTS 	plural determiner (these, those)
DTX 	determiner/double conjunction (either)
EX 	existential there
FW 	foreign word (hyphenated before regular tag)
HV 	have
HVD 	had (past tense)
HVG 	having
HVN 	had (past participle)
IN 	preposition
JJ 	adjective
JJR 	comparative adjective
JJS 	semantically superlative adjective (chief, top)
JJT 	morphologically superlative adjective (biggest)
MD 	modal auxiliary (can, should, will)
NC 	cited word (hyphenated after regular tag)
NN 	singular or mass noun
NN$ 	possessive singular noun
NNS 	plural noun
NNS$ 	possessive plural noun
NP 	proper noun or part of name phrase
NP$ 	possessive proper noun
NPS 	plural proper noun
NPS$ 	possessive plural proper noun
NR 	adverbial noun (home, today, west)
OD 	ordinal numeral (first, 2nd)
PN 	nominal pronoun (everybody, nothing)
PN$ 	possessive nominal pronoun
PP$ 	possessive personal pronoun (my, our)
PP$$ 	second (nominal) possessive pronoun (mine, ours)
PPL 	singular reflexive/intensive personal pronoun (myself)
PPLS 	plural reflexive/intensive personal pronoun (ourselves)
PPO 	objective personal pronoun (me, him, it, them)
PPS 	3rd. singular nominative pronoun (he, she, it, one)
PPSS 	other nominative personal pronoun (I, we, they, you)
PRP 	Personal pronoun
PRP$ 	Possessive pronoun
QL 	qualifier (very, fairly)
QLP 	post-qualifier (enough, indeed)
RB 	adverb
RBR 	comparative adverb
RBT 	superlative adverb
RN 	nominal adverb (here, then, indoors)
RP 	adverb/particle (about, off, up)
TO 	infinitive marker to
UH 	interjection, exclamation
VB 	verb, base form
VBD 	verb, past tense
VBG 	verb, present participle/gerund
VBN 	verb, past participle
VBP 	verb, non 3rd person, singular, present
VBZ 	verb, 3rd. singular present
WDT 	wh- determiner (what, which)
WP$ 	possessive wh- pronoun (whose)
WPO 	objective wh- pronoun (whom, which, that)
WPS 	nominative wh- pronoun (who, which, that)
WQL 	wh- qualifier (how)
WRB 	wh- adverb (how, where, when)

Note that some versions of the tagged Brown corpus contain combined tags.
For instance the word "wanna" is tagged VB+TO, since it is a contracted form of the two words, want/VB and to/TO.
Also some tags might be negated, for instance "aren't" would be tagged "BER*", where * signifies the negation.
Additionally, tags may have hyphenations: The tag -HL is hyphenated to the regular tags of words in headlines.
The tag -TL is hyphenated to the regular tags of words in titles.
The hyphenation -NC signifies an emphasized word.
Sometimes the tag has a FW- prefix which means foreign word.
~~~

### Data merging and cleaning

The Brown Corpus comes as approximately 500 files, named by the convention
`cXYY`, where `c` is short for Corpus, `X` refers to the type of content, and `YY` a two-digit label.
For example: `ca01` is the first (`01`) of the journalistic (`a`) segments of the entire corpus (`c`).

In order to have all the data in one file, we used the following BASH commands:

~~~Bash
cat $(ls | grep '^c...$') > MERGE_ALL
~~~

(Which places all the data from the segments into a fille called `MERGE_ALL`.)

~~~Bash
grep --invert-match '^$' MERGE_ALL > MERGE_ALL_NO_BLANKS
~~~

The file `MERGE_ALL_NO_BLANKS` now contains each sentence from the entire corpus, one to a line.
Finally, we moved the `MERGE_ALL_NO_BLANKS` file into a separate /data_files folder.

The structure currently looks like:

~~~
/brown/
 + ca01
 + ca02
 + [etc.]
/data_files/
 + MERGE_ALL
 + MERGE_ALL_NO_BLANKS
 + TAG_LOOKUP
/scripts/
.gitignore
LICENSE
Plan.md
README.md
~~~

We are aware of the American English generated by GitHub, and apologise for any confusion caused.
The `TAG_LOOKUP` file is generated from the list of POS tags given above.

### Overview of data

Regarding the Brown Corpus:

 - Language: American English
 - File size: 10.1 MB (text files, uncompressed)
 - Sentences: 57341 (57,341)
 - Words: 1014312 (1,014,312)

# Plan of action

We wish to identify the arities of any given POS.
We will start with POS, and then move on to individual words later.
We realise that in some cases certain parts of speech may have different arities, depending on context.
As such we will therefore look for a sense of the probability distribution of arities for a given POS.

 - We are expecting to have to reduce the number of POS tags down from 81.
 - We are expecting to have to induce a bias of the form "Nouns have arity 1"
 - We are expecting to have to remove problematic sentences
 e.g. those that contain titles, quotations, or foreign words.

### Cleanup: Stripping out all but POS

For our initial research, we shall focus purely on the Parts Of Speech.


### Round 1: POS by sentence length

The first round will simply inform us:
For a given POS, what are the lengths of sentences that contain that POS.
If we link sentence length to sentence complexity, then this may give us a (weak) link
between POS and complexity.
We are asking this question to inform future questions, and to give us a benchmark against which we can gauge future outcomes.

On my home desktop `Round1.py` took 150s to run.

#### Method

Our first attempt took every sentence in the POS_ONLY file, and formed a histogram of POS against sentence length.
This gave us an output of 353 different POS recorded in the file; even after separating out negated and combined tags.
The reason for such a large count of POS is the existence of the `-hl`, `-tl` and `-nc` tags.
These tags denote the contextual information of titles, headlines and emphasised words respectively.

Noteworthy changes:
 - We have added the POS `SENTENCE` that records data for lengths of sentences
 - We have changed the `,` tag to `COM` to avoid conflict with comma-delineation
 - We append one final piece of data, which is the number of sentences containing hyphenated tags (`-hl`,`-tl`,`-nc`)

The reason for this final statistic is to see how many lines are affected by these hyphenated tags.
If there are very few we can ignore them as statistical noise.
If there are a significant number then we shall have to decide whether or not to include them in our data.
Our options for dealing with the hyphenated tags are:
 - Leave them in place (dramatically increases the number of tags we are dealing with)
 - Ignore just the hyphenated part (e.g. `nn-hl` becomes just `nn`)
 - Drop the line that contains them

#### Results

The number of sentences with hyphenated tags was 12,234.
This amounts to roughly 20% of our total number of sentences in the data.
Dropping the lines that contain hyphenated tags seems excessive,
however I am unwilling to decide between leaving them be and merging.
My hesitation comes from the `-tl` tag; it indicates that the word is part of a title.
Since, to my mind, it seems likely that titles will end up being treated in a similar way to nouns,
I wish to keep the tags as they are, and move on to looking at bigrams of POS.

### Round 2: Left and right bigrams

The purpose of Round 1 was to get a handle on the breakdown by POS of the data available.
Now we will start to take a look at how the POS are positioned relative to each other.

It was at this point that I found the nltk python library.
It does many of the things I want, but I don't know if it will do all of them.
Certainly most of the things I intend to investigate could be built on top of nltk.

#### Method

We loop through each sentence, and keep track of each occurence of a 1-gram or 2-gram.

#### Results

Here are the top ten most common 1-grams and 2-grams:

~~~
nn	152522
in	120572
at	97965
jj	64030
.	60638
COM	58156
nns	55112
at++nn	48393
in++at	43274
nn++in	42254
~~~

Recall that we have replaced `,` with `COM` for legibility.