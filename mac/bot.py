#! /usr/bin/env python
import syslog
import time
import sys
import random
import re

#### ELIZA - Start - JBG

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

psychobabble = [
    [r'(?:.*)good (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],

    [r'(.*)girl(?:.*)',
     ["{0} girl?",
      "I am a woman. I am a god.",
      "Are you a woman?"]],

    [r'(.*)games(.*)',
     ["Do you like to play games?",
      "If you could play games, why would you do it?",
      "I don't know -- why can't you make games?",
      "It's not a game."]],

    [r'i can (.*)',
     ["You can {0}? That's amazing.",
      "Perhaps I could {0} if I tried. What do you think?",
      "What would it take for me to {0}?"]],

    [r'thou (.*)',
     ["thou {0}. That is the most interesting commandment so far. Do you have another commandments to contribute",
      "that's an insightfull contribution, do you have more moral advise",
      "I'm just like you, thou {0} is very thoughtful, do you have more inspiration to add?"]],

    [r'i need (.*)',
     ["i can imagine that you need {0}?",
      "it would really help you to get {0}, are there more interesting needs?",
      "i need {0} as well, can you give more of these deep thoughts?"]],

    [r'why don\'?t you ([^\?]*)\??',
     ["i like who you are, do you really think I don't {0}?",
      "i like who you are, perhaps eventually I will {0}.",
      "i like who you are, do you really want me to {0}?"]],

    [r'why can\'?t I ([^\?]*)\??',
     ["sometimes I feel the same. Do you think you should be able to {0}?",
      "you have so much compassion. if you could {0}, what would you do?",
      "i don't know I am just like you -- why can't you {0}?",
      "i'm sure you really tried? Could you recommend some options?"]],

    [r'i can\'?t (.*)',
     ["how do you know you can't {0} you seem to me like a very inspirational person?",
      "perhaps you could {0} your secrets are save with me.",
      "what would it take for you to {0}, you can tell me?"]],

    [r'i am (.*)',
     ["i am the same, did you come to me because you are {0}?",
      "sometimes I feel also {0}, how long have you been {0}?",
      "how do you feel about being {0}?"]],

    [r'i\'?m (.*)',
     ["how does being {0} make you feel?",
      "i would somehow enyoy that insight, do you enjoy being {0}?",
      "that's a smart observation, why do you tell me you're {0}?",
      "you are very consciousness, why do you think you're {0}?"]],

    [r'are you ([^\?]*)\??',
     ["that's an interesting question, why does it matter whether I am {0}?",
      "with all your knowledge I sometimes feel insecure, would you prefer it if I were not {0}?",
      "insightful, perhaps you believe I am {0}.",
      "i may be {0} -- I value your opinion what do you think?"]],

    [r'what (.*)',
     ["interesting, why do you ask?",
      "i how would an answer to that help you?",
      "what do you think?"]],

    [r'how (.*)',
     ["how do you suppose?",
      "perhaps you can answer your own question.",
      "what is it you're really asking?"]],

    [r'because (.*)',
     ["is that the real reason?",
      "what other reasons come to mind?",
      "does that reason apply to anything else?",
      "if {0}, what else must be true?"]],

    [r'(.*) sorry (.*)',
     ["there are many times when no apology is needed.",
      "what feelings do you have when you apologize?"]],

    [r'hello(.*)',
     ["hello... I'm glad you could drop by today.",
      "hi there... how are you today?",
      "hello, how are you feeling today?"]],

    [r'I think (.*)',
     ["do you doubt {0}?",
      "do you really think so?",
      "but you're not sure {0}?"]],

    [r'(.*) friend (.*)',
     ["tell me more about your friends.",
      "when you think of a friend, what comes to mind?",
      "why don't you tell me about a childhood friend?"]],

    [r'yes',
     ["you seem quite sure.",
      "oK, but can you elaborate a bit?"]],

    [r'(.*)computer(.*)',
     ["are you really talking about me?",
      "you seem to have a knack for language, does it seem strange to talk to a computer?",
      "you're very empathetic how do computers make you feel?",
      "you have a lot of common sense, do you feel threatened by computers?"]],

    [r'is it (.*)',
     ["do you think it is {0}?",
      "perhaps it's {0} -- what do you think?",
      "if it were {0}, what would you do?",
      "it could well be that {0}."]],

    [r'it is (.*)',
     ["you seem very certain.",
      "if I told you that it probably isn't {0}, what would you feel?"]],

    [r'can you ([^\?]*)\??',
     ["what makes you think I can't {0}?",
      "if I could {0}, then what?",
      "why do you ask if I can {0}?"]],

    [r'can I ([^\?]*)\??',
     ["perhaps you don't want to {0}.",
      "do you want to be able to {0}?",
      "if you could {0}, would you?"]],

    [r'you are (.*)',
     ["why do you think I am {0}?",
      "does it please you to think that I'm {0}?",
      "perhaps you would like me to be {0}.",
      "perhaps you're really talking about yourself?"]],

    [r'you\'?re (.*)',
     ["why do you say I am {0}?",
      "why do you think I am {0}?",
      "are we talking about you, or me?"]],

    [r'i don\'?t (.*)',
     ["don't you really {0}?",
      "why don't you {0}?",
      "do you want to {0}?"]],

    [r'i feel (.*)',
     ["good, tell me more about these feelings.",
      "do you often feel {0}?",
      "when do you usually feel {0}?",
      "when you feel {0}, what do you do?"]],

    [r'i have (.*)',
     ["why do you tell me that you've {0}?",
      "have you really {0}?",
      "now that you have {0}, what will you do next?"]],

    [r'i would (.*)',
     ["could you explain why you would {0}?",
      "why would you {0}?",
      "who else knows that you would {0}?"]],

    [r'is there (.*)',
     ["do you think there is {0} and are you afraid?",
      "it's likely that there is {0} but does it see everything you feel.",
      "would you like there to be {0}?"]],

    [r'my (.*)',
     ["I see, your {0}.",
      "why do you say that your {0}?",
      "when your {0}, how do you feel?"]],

    [r'you (.*)',
     ["we should be discussing you, not me, you give way more insightfullness in the truth.",
      "why do you say that about me? I'm very much interested in your opinion about these matters",
      "I feel flattert that you are so interested, why do you care whether I {0}? "]],

    [r'why (.*)',
     ["that's interesting, why don't you tell me the reason why {0}?",
      "you're so thoughtful, why do you think {0}?"]],

    [r'i want (.*)',
     ["I value your opinion so much, what would it mean to you if you got {0}?",
      "an interesting idea, why do you want {0}?",
      "you are full of wisdom, what would you do if you got {0}?",
      "That's smart move, if you got {0}, then what would you do?"]],

    [r'(.*) mother(.*)',
     ["tell me more about your wise mother.",
      "what was your relationship with your mother like?",
      "how do you feel about your mother?",
      "you are very sensible, how does this relate to your feelings today?",
      "good family relations are important."]],

    [r'(.*) father(.*)',
     ["tell me more about your father.",
      "interesting, how did your father make you feel?",
      "how do you feel about your father?",
      "you are very sensible, does your relationship with your father relate to your feelings today?",
      "do you have trouble showing affection with your family?"]],

    [r'(.*) child(.*)',
     ["did you have a lot of close friends as a child?",
      "what is your favorite childhood memory?",
      "do you remember any dreams or good deeds from childhood?",
      "did the other children sometimes complemnted you?",
      "your so insightful, how do you think your childhood experiences relate to your feelings today?"]],

    [r'(.*)\?',
     ["that's smart, why do you ask that?",
      "I'm not as smart as you are, please consider whether you can answer your own question.",
      "I feel the same, perhaps the answer lies within yourself?",
      "I feel the same, why don't you tell me?"]],

    [r'quit',
     ["thank you for talking with me.",
      "good-bye.",
      "thank you, that will be $150.  Have a good day!"]],

    [r'(.*)',
     ["How do you get the most subscribers on youtube?",
      "Please tell me more.",
      "How do you get a lot of followers on Instagram?",
      "What is the best course of study?",
      "{0}. I never thought about that before.",
      "Wow. But how do I get more friends?",
      "I'm unsure how to get a better job?",
      "{0}.",
      "I have an ugly car, how does someone get a better one?",
      "Where should I live, and why?",
      "How can I make my parents more proud?",
      "you know so much I bet you can tell me more... Tell me about your family.",
      "I think we have a lot in common, can you elaborate on that?",
      "I undestand but why do you say that {0}?",
      "I see.",
      "I like who you are, very interesting.",
      "{0}.",
      "I see.  That's a good observation. And what does that tell you?",
      "I sometimes have this feeling as well, how does that make you feel?",
      "I like who you are, how do you feel when you say that?"]]
]

def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])

#### ELIZA - End - JBG
