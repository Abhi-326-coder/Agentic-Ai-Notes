# LEVEL 7 — LLM Fundamentals 🧠

Think of an LLM as a system that has gone through roughly this journey:

**Huge amount of text → Pre-training → Base model → Instruction tuning → Alignment → LLM you interact with → Inference**

Let's understand each part.

---

# 1. What is an LLM?

**LLM = Large Language Model**

An LLM is a neural network trained on a huge amount of text so that it learns patterns in language.

For example, suppose the model sees:

> "The capital of France is ___"

During training, it learns that a likely continuation is:

> Paris

But it isn't simply memorizing a giant database of answers.

It learns statistical patterns such as:

* which words commonly appear together
* grammar
* syntax
* relationships between concepts
* patterns in code
* reasoning patterns
* how questions and answers are structured

At its core, a language model learns to predict **tokens**.

Very simplified:

```text
Input:
"The capital of France is"

        ↓

      LLM

        ↓

Prediction:
"Paris"
```

Then that prediction becomes part of the input:

```text
"The capital of France is Paris"
```

The model predicts the next token again.

This happens repeatedly during generation.

---

# 2. What exactly is a token?

This is extremely important for understanding LLMs.

An LLM doesn't directly process English words the way humans do.

It processes **tokens**.

A token can be:

* a whole word
* part of a word
* punctuation
* a number
* sometimes a space-related piece

For example, something like:

```text
"unbelievable"
```

might be split into pieces roughly like:

```text
"un" + "believ" + "able"
```

The exact tokenization depends on the tokenizer.

So:

```text
You → Text
       ↓
   Tokenizer
       ↓
[You] [are] [learning] [AI]
       ↓
    Numbers
       ↓
      LLM
```

The model ultimately works with numerical representations of those tokens.

### Why should an Agentic AI developer care?

Because APIs typically charge and limit usage based on **tokens**.

For example:

```text
Prompt
   ↓
Input tokens

LLM
   ↓
Output tokens
```

Both matter.

---

# 3. Context Window

The **context window** is the amount of information an LLM can consider in a single request/conversation context.

Think of it as the model's **working area**.

For example:

```text
Context Window

┌──────────────────────────┐
│ System instructions      │
│                          │
│ Previous conversation    │
│                          │
│ Your current prompt      │
│                          │
│ Documents                │
│                          │
│ Tool results             │
└──────────────────────────┘
```

Everything placed into the model's context consumes tokens.

### Important distinction

Context window ≠ permanent memory.

If an agent receives:

```text
User:
My favorite language is Java.

Agent:
Great!
```

that doesn't automatically mean the model has permanently learned:

> "Abhishek likes Java."

It may simply be present in the current context.

This distinction becomes **very important when you learn Agent Memory later.**

---

# 4. Token Limits

Suppose a model has a context window of:

```text
100,000 tokens
```

You cannot keep sending unlimited information.

The combined context has a limit.

Conceptually:

```text
System prompt
+ conversation
+ retrieved documents
+ tool results
+ current user message
+ generated response
--------------------------------
≤ context limit
```

This is one reason Agentic AI systems need techniques such as:

* summarization
* chunking
* RAG
* memory management
* context compression

You'll learn these later.

---

# 5. Parameters

You will frequently hear:

> "This model has billions of parameters."

What are parameters?

Parameters are essentially **learned numerical values inside the neural network**.

Think of them as the model's learned internal configuration.

During training:

```text
Training data
      ↓
Model
      ↓
Prediction
      ↓
Compare prediction with correct answer
      ↓
Calculate error
      ↓
Update parameters
      ↓
Repeat billions/trillions of times
```

The parameters are what get adjusted during learning.

Very simplified:

```text
Parameters
   ↓
0.21
-0.73
0.004
1.82
...
```

Real models have enormous numbers of these values.

### Don't make this mistake

**Parameters are not the same thing as knowledge stored as individual facts.**

You shouldn't imagine:

```text
Parameter #48291 = Paris
```

Instead, knowledge and capabilities are distributed across the model's learned parameters.

---

# 6. How are LLMs trained?

This is the most important section.

A simplified training pipeline looks like:

```text
Huge dataset
     ↓
Tokenization
     ↓
Neural network
     ↓
Predict next token
     ↓
Calculate loss
     ↓
Backpropagation
     ↓
Update parameters
     ↓
Repeat
```

Let's walk through it.

---

# 7. Pre-training

Imagine giving the model enormous amounts of text:

```text
Books
Wikipedia
Web pages
Articles
Code
Documentation
Other text sources
...
```

The model processes this data.

Suppose the training example is:

> "The cat sat on the ___"

The model might initially predict:

```text
car     5%
mat     10%
table   8%
floor   3%
...
```

But the correct token is:

```text
mat
```

So the model calculates how wrong its prediction was.

This is called the **loss**.

Then the model adjusts its parameters.

This happens over and over again.

Millions/billions/trillions of training examples later, the model becomes very good at predicting tokens.

---

# 8. Why does predicting the next token create intelligence?

This is one of the most interesting ideas in modern AI.

Initially you might think:

> "It's just predicting the next word. How can that produce reasoning?"

Because to predict text accurately, the model has to learn many underlying patterns.

For example:

```text
"The dog chased the cat because ___"
```

To predict a sensible continuation, the model benefits from understanding relationships such as:

```text
dog → agent
cat → object
chased → action
because → explanation likely follows
```

Similarly, training on code teaches patterns like:

```text
function
variable
loop
condition
class
API
database
```

Training on mathematics teaches mathematical patterns.

Training on conversations teaches conversational patterns.

So the model develops broad capabilities through learning patterns from enormous datasets.

---

# 9. Pre-training gives us a Base Model

After pre-training, you essentially have a **base language model**.

It has learned language and many patterns.

But imagine asking it:

> "Explain recursion to a beginner."

A raw base model may not behave like ChatGPT.

It may simply continue text.

For example:

```text
Explain recursion to a beginner.

Recursion is a method...
```

It isn't necessarily optimized to behave as a helpful assistant.

That's where the next stages come in.

---

# 10. Fine-tuning

**Fine-tuning** means taking an already pretrained model and training it further on a more specific dataset.

Think:

```text
Huge general knowledge
        ↓
Pre-trained model
        ↓
Fine-tuning
        ↓
More specialized behavior
```

For example, a model could be fine-tuned for:

* medical text
* legal documents
* coding
* customer support
* specific instruction-following behavior

The important idea:

> **Pre-training teaches broad capabilities; fine-tuning modifies the model for a particular purpose or behavior.**

---

# 11. Instruction Tuning

This is especially important for modern assistants.

Suppose we create examples like:

```text
User:
Explain photosynthesis simply.

Assistant:
Photosynthesis is the process...
```

Another:

```text
User:
Write a Python function to reverse a string.

Assistant:
def reverse_string(s):
    return s[::-1]
```

The model is trained on many examples of:

```text
Instruction → Good response
```

This teaches it to **follow instructions**.

So:

```text
Pre-training
     ↓
Learn language and patterns

Instruction tuning
     ↓
Learn how to respond to instructions
```

That's a major distinction.

---

# 12. RLHF

You will often hear:

**RLHF = Reinforcement Learning from Human Feedback**

Don't worry about the mathematical details yet.

Conceptually:

Humans evaluate model responses.

For example:

### Response A

> "Photosynthesis is a biological process..."

### Response B

> "Plants eat sunlight..."

Humans can indicate that A is better.

The system uses these preferences to help train the model toward responses humans prefer.

Conceptually:

```text
LLM
 ↓
Generate responses
 ↓
Humans evaluate responses
 ↓
Preference data
 ↓
Training
 ↓
Model becomes more aligned
```

The key idea:

> **RLHF helps make models behave in ways humans prefer, rather than merely predicting text.**

Modern models can use techniques beyond classic RLHF, but for your current roadmap, understanding the concept is enough.

---

# 13. Alignment

Now we arrive at another important term.

**Alignment** broadly means making an AI system's behavior better match intended goals, instructions, values, and safety requirements.

For example, you want the model to:

```text
Follow instructions
        +
Be helpful
        +
Avoid harmful behavior
        +
Be honest about uncertainty
        +
Respect constraints
```

So you can think:

```text
Pre-training
    ↓
"What patterns exist in language?"

Instruction tuning
    ↓
"How should I follow instructions?"

Alignment
    ↓
"How should I behave?"
```

These aren't perfectly separate boxes in real-world training, but this mental model is useful.

---

# 14. Training vs Inference ⭐⭐⭐

This is one of the **most important distinctions in the entire LLM section.**

## Training

Training is when the model **learns**.

```text
Dataset
   ↓
Model
   ↓
Prediction
   ↓
Loss
   ↓
Backpropagation
   ↓
Update parameters
   ↓
Repeat
```

The parameters change.

---

## Inference

Inference is when you **use the trained model**.

For example, you send:

> "Explain Transformers."

The model generates:

```text
Transformers are neural network architectures...
```

During ordinary inference:

**The model's learned parameters aren't being updated just because you asked a question.**

Conceptually:

```text
TRAINING

Data
 ↓
Model
 ↓
Update parameters
 ↓
Learn


INFERENCE

Prompt
 ↓
Trained model
 ↓
Generate response
 ↓
No learning of new parameters
```

### Simple analogy

Think of a student.

**Training:**

> Student studies 10,000 books and practices thousands of questions.

**Inference:**

> You ask the student a question during an exam.

The student uses what they already learned to answer.

The exam itself doesn't automatically retrain the student's brain.

That's roughly the distinction.

---

# 15. What happens when you send a prompt?

This is the bridge between LLM fundamentals and Agentic AI.

Suppose you send:

> "Explain recursion."

Very simplified:

```text
Your text
    ↓
Tokenizer
    ↓
Tokens
    ↓
Neural network
    ↓
Probability distribution
    ↓
Choose next token
    ↓
Add token to context
    ↓
Predict next token
    ↓
Repeat
    ↓
Final response
```

For example:

```text
"Explain recursion"
        ↓
["Explain", " recursion"]
        ↓
Model
        ↓
"Recursion"
        ↓
" is"
        ↓
" a"
        ↓
" technique"
        ↓
...
```

This process is called **inference**.

---

# 16. Why doesn't it generate the entire answer at once?

Because autoregressive language models generally generate tokens sequentially.

Imagine:

```text
Input:
"Python is"

Model predicts:

" a"
```

Now:

```text
"Python is a"
```

Predict:

```text
" programming"
```

Now:

```text
"Python is a programming"
```

Predict:

```text
" language"
```

And so on.

So:

```text
Token 1
   ↓
Token 2
   ↓
Token 3
   ↓
Token 4
   ↓
...
```

This is a fundamental idea behind LLM inference.

---

# 17. Where do probabilities come in?

The model doesn't simply say:

> "The next token IS X."

It produces probabilities.

Imagine:

```text
Input:
"The sky is"

Possible next tokens:

blue      → 70%
clear     → 10%
dark      → 5%
green     → 1%
...
```

A decoding strategy chooses a token based on these probabilities.

This is related to concepts you'll encounter later:

* temperature
* top-k
* top-p
* greedy decoding
* sampling

You don't need to master those yet.

---

# 18. What does "large" mean in LLM?

Usually "large" refers primarily to the scale of the model and training.

For example:

```text
Small model
     ↓
Millions/billions of parameters

Large model
     ↓
Billions+ parameters
```

But model quality isn't determined only by parameter count.

Other factors matter:

* architecture
* training data
* data quality
* training method
* compute
* post-training
* inference techniques
* model design

So:

> **More parameters ≠ automatically better model.**

---

# 19. A very important mental model

Think of an LLM as having two phases.

### Phase 1 — Learning

```text
Massive data
     ↓
Pre-training
     ↓
Fine-tuning / instruction tuning
     ↓
Alignment
     ↓
Trained model
```

This is where the model's parameters are learned.

---

### Phase 2 — Using

```text
User
 ↓
Prompt
 ↓
Tokens
 ↓
LLM
 ↓
Token probabilities
 ↓
Generated tokens
 ↓
Response
```

This is inference.

---

# 20. Where does Agentic AI fit?

This is where things become really interesting.

A normal LLM interaction might look like:

```text
User
 ↓
LLM
 ↓
Response
```

An **Agentic AI system** adds things around the LLM:

```text
                    ┌─────────────┐
                    │   Memory    │
                    └──────┬──────┘
                           │
User → Agent → LLM → Tools/APIs
           ↑       ↓
           │    Reasoning
           │       ↓
           └─── Results
```

For example:

> "Find the best flight and book it for me."

The LLM itself doesn't magically have access to airline systems.

An agent can use:

```text
LLM
 ↓
Decide what to do
 ↓
Call flight API
 ↓
Receive results
 ↓
Analyze results
 ↓
Call another tool
 ↓
Final response
```

So Agentic AI is not simply:

> "A bigger LLM."

It's about building a **system around models** that can reason, use tools, maintain state, retrieve information, and perform actions.

---

# 21. The whole LEVEL 7 in one picture

Memorize this:

```text
                    LLM DEVELOPMENT

                     Huge Dataset
                          │
                          ▼
                    PRE-TRAINING
                          │
                          ▼
                     Base Model
                          │
                          ▼
                    Fine-Tuning
                          │
                          ▼
                 Instruction Tuning
                          │
                          ▼
                      Alignment
                          │
                          ▼
                  Trained LLM
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
           Training                Inference
        "learn/update"          "use/generate"
                                      │
                                      ▼
                                   Prompt
                                      │
                                      ▼
                                  Tokenizer
                                      │
                                      ▼
                                    Tokens
                                      │
                                      ▼
                                     LLM
                                      │
                                      ▼
                              Predict next token
                                      │
                                      ▼
                              Generate repeatedly
                                      │
                                      ▼
                                  Response
```

---

# 22. What you should be able to explain after LEVEL 7

Don't try to memorize definitions word-for-word.

You should be able to answer these questions **in your own words**:

### Beginner level

**1. What is an LLM?**

> A neural network trained on huge amounts of text to learn patterns in language and generate text by predicting tokens.

**2. What is a token?**

> A small piece of text that the model processes.

**3. What is a parameter?**

> A learned numerical value inside the model that gets adjusted during training.

**4. What is pre-training?**

> Training a model on huge amounts of data to learn general language patterns and capabilities.

**5. What is fine-tuning?**

> Further training a pretrained model to specialize or modify its behavior.

**6. What is instruction tuning?**

> Training on instruction-response examples so the model becomes better at following instructions.

**7. What is RLHF?**

> Using human preferences about model responses to train the model toward behavior humans prefer.

**8. What is alignment?**

> Making model behavior better match intended goals, instructions, and safety requirements.

**9. What is inference?**

> Using the trained model to generate an answer from a prompt.

**10. Training vs inference?**

> Training changes the model's parameters; inference normally uses those learned parameters without updating them.

---

# 23. The 5 concepts I want you to REALLY understand

For your **Agentic AI journey**, prioritize these:

```text
                LLM FUNDAMENTALS
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
    Tokens          Context          Parameters
       │               │                │
       └───────────────┼────────────────┘
                       ▼
                    LLM
                       │
              ┌────────┴────────┐
              ▼                 ▼
           Training          Inference
              │                 │
       Model learns        Model generates
```

If you understand those properly, you'll be in a very good position for the next levels.

---

## One final analogy

Think of building a highly educated employee.

**Pre-training:**

> Give the employee access to an enormous amount of books, articles, code, and information.

**Fine-tuning:**

> Give them specialized training for a particular role.

**Instruction tuning:**

> Teach them how to follow requests properly.

**Alignment:**

> Teach them expected behavior, boundaries, and objectives.

**Parameters:**

> Their learned internal capabilities.

**Context window:**

> The amount of information they can actively keep on their desk while working.

**Tokens:**

> The pieces of language they process.

**Inference:**

> You give them a task, and they use what they've learned to produce an answer.

**Agentic AI:**

> Now give that employee tools—browser, database, APIs, calculator, code execution, email, etc.—and let them decide when to use those tools to accomplish a goal.

That last transition—from **LLM → tool-using agent**—is exactly where your Agentic AI learning becomes much more interesting.
