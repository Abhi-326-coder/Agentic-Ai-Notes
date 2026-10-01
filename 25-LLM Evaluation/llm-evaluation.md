# LEVEL 31 — LLM EVALUATION

This is the level that turns you from someone who can **build an AI agent** into someone who can **engineer and improve an AI system**.

You have already learned:

```text
LangChain
   ↓
LangGraph
   ↓
RAG
   ↓
Multi-Agent
   ↓
Deep Agents
   ↓
MCP
   ↓
Guardrails
   ↓
🔥 LLM EVALUATION
```

And this is the correct point to learn evaluation because you now have something complicated enough to evaluate.

---

# 1. The fundamental problem

Imagine you build an agent.

User asks:

> "Find the cheapest flight from Bangalore to Delhi next Friday."

Your agent responds:

> "The cheapest flight is ₹4,850."

Looks good.

But...

**How do you know it's actually correct?**

You can't manually ask:

```text
"Did my agent work?"
```

for every request.

Production systems may process:

```text
10,000
100,000
1,000,000+
```

interactions.

You need a systematic way to answer:

> **Is my AI system behaving correctly, and did the latest change make it better or worse?**

That's **LLM evaluation**.

---

# 2. The most important mental model

Memorize this:

```text
             AI SYSTEM
                 ↓
              OUTPUT
                 ↓
             EVALUATE
                 ↓
          ┌──────┴──────┐
          ↓             ↓
       GOOD           BAD
          ↓             ↓
       Keep         Analyze
                        ↓
                     Improve
                        ↓
                     Test
                        ↓
                     Repeat
```

So production AI isn't:

```text
Prompt → Response
```

It is:

```text
Input
  ↓
LLM / Agent
  ↓
Output
  ↓
Evaluation
  ↓
Analysis
  ↓
Improvement
  ↓
Regression Tests
  ↓
Deploy
  ↓
Monitor
  ↓
Evaluate again
```

This is the **AI engineering mindset**.

---

# 3. What exactly are we evaluating?

A beginner often thinks:

> "Evaluation means checking whether the final answer is correct."

That's only one part.

For Agentic AI, you can evaluate:

```text
                    AGENT
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      Input         Process        Output
        │             │             │
        ↓             ↓             ↓
    Quality       Trajectory      Answer
```

And inside the process:

```text
Planning
Tool selection
Tool arguments
Tool execution
Retrieval
Reasoning trajectory
Agent routing
Final response
```

You might therefore evaluate:

* correctness
* relevance
* groundedness
* faithfulness
* hallucination
* tool selection
* tool arguments
* task completion
* agent trajectory
* retrieval quality
* safety
* latency
* cost
* reliability

This is where **Agent Evaluation** becomes more complicated than simple LLM evaluation.

---

# 4. The evaluation vocabulary

You need to understand these terms clearly:

```text
Dataset
Test Case
Input
Expected Output
Ground Truth
Prediction
Evaluator
Metric
Experiment
Regression Test
```

Let's understand them one by one.

---

# 5. Dataset

A dataset is a collection of examples used to evaluate your AI system.

Example:

```python
dataset = [
    {
        "question": "What is TCP?",
        "expected": "TCP is a connection-oriented transport protocol."
    },
    {
        "question": "What is DNS?",
        "expected": "DNS translates domain names to IP addresses."
    },
]
```

Think:

```text
Dataset
│
├── Test Case 1
├── Test Case 2
├── Test Case 3
├── Test Case 4
└── ...
```

---

# 6. Test case

A single evaluation example.

For an Agentic AI system:

```python
{
    "input": "Find the README and explain the project",
    "expected": "The project is a task manager"
}
```

Could also contain more information:

```python
{
    "input": "...",
    "expected_output": "...",
    "expected_tools": [
        "list_files",
        "read_file"
    ],
    "metadata": {
        "category": "code_analysis"
    }
}
```

This becomes very powerful for agent evaluation.

---

# 7. Ground truth

This is another extremely important concept.

**Ground truth = the reference answer or expected behavior against which you evaluate the system.**

Example:

Question:

```text
What is 2 + 2?
```

Ground truth:

```text
4
```

Agent:

```text
4
```

Correct.

---

But for many LLM tasks there isn't one exact answer.

Question:

> Explain TCP.

Possible valid answers:

```text
TCP is a reliable connection-oriented transport protocol...
```

or:

```text
TCP provides reliable, ordered delivery of data between applications...
```

Both can be correct.

Therefore LLM evaluation often can't simply do:

```python
prediction == expected
```

---

# 8. Exact match evaluation

For deterministic tasks, exact matching is excellent.

```python
def exact_match(
    prediction,
    expected
):
    return prediction == expected
```

Example:

```python
prediction = "4"
expected = "4"

print(
    exact_match(
        prediction,
        expected
    )
)
```

Output:

```text
True
```

Use this for things like:

* classification labels
* boolean decisions
* IDs
* exact structured values
* deterministic transformations

---

# 9. Why exact matching doesn't work well for LLMs

Suppose:

```text
Expected:

Paris is the capital of France.
```

Model:

```text
The capital city of France is Paris.
```

Exact match:

```text
False
```

But semantically:

```text
Correct.
```

Therefore we need better evaluators.

---

# 10. Evaluation metrics

A metric is a measurable signal representing system quality.

Examples:

```text
Accuracy
Precision
Recall
F1
Correctness
Relevance
Faithfulness
Groundedness
Toxicity
Latency
Cost
Task success rate
Tool-call accuracy
```

The appropriate metric depends on the system.

---

# 11. Accuracy

Suppose you have:

```text
100 test cases
90 correct
```

Then:

```text
Accuracy = 90 / 100
         = 90%
```

Simple.

For classification tasks, accuracy can be useful.

But for open-ended LLM outputs, accuracy is often insufficient.

---

# 12. Precision and recall

These come from classical machine learning and are useful when your AI system performs classification/detection.

For example, a prompt-injection detector.

```text
Actual attack?
Predicted attack?
```

You have:

```text
TP = correctly detected attack
FP = normal input incorrectly flagged
TN = correctly accepted normal input
FN = attack missed
```

genui{"learning_viz":{"type_id":"CLASSIFICATION_THRESHOLD","initial_values":{"threshold":0.5}}}

### Precision

> Of everything we flagged as an attack, how many really were attacks?

```text
Precision = TP / (TP + FP)
```

### Recall

> Of all actual attacks, how many did we detect?

```text
Recall = TP / (TP + FN)
```

This matters when evaluating things like:

* prompt injection detectors
* PII detectors
* safety classifiers
* spam detection

---

# 13. F1 score

F1 combines precision and recall.

```text
F1 = 2 × Precision × Recall
     ────────────────────────
       Precision + Recall
```

You don't need to use F1 for every LLM evaluation.

But you should understand it because AI systems often contain traditional classifiers.

---

# 14. LLM evaluation is different

Now imagine:

```text
Question:
Explain recursion.
```

Expected:

```text
Recursion is when a function calls itself...
```

Agent:

```text
Recursion is a programming technique where
a function solves a problem by calling itself
on smaller versions of the same problem...
```

How do we automatically score this?

This is where:

# LLM-as-a-Judge

comes in.

---

# 15. LLM-as-a-Judge

We use another model as an evaluator.

```text
              Question
                  │
          ┌───────┴────────┐
          ↓                ↓
       Agent            Ground Truth
          │                │
          └───────┬────────┘
                  ↓
             Judge LLM
                  ↓
             Score / Reason
```

Example evaluator prompt:

```python
judge_prompt = """
You are evaluating an AI assistant.

Question:
{question}

Expected answer:
{expected}

Actual answer:
{actual}

Evaluate whether the actual answer is correct.

Return:
score: 0 or 1
reason: explanation
"""
```

Then:

```text
Judge:

score: 1

reason:
The answer correctly explains recursion
and describes the base case concept.
```

---

# 16. Why LLM-as-a-Judge is powerful

It can evaluate things difficult to express with exact rules:

* correctness
* relevance
* helpfulness
* style
* coherence
* groundedness
* completeness

But it isn't perfect.

---

# 17. LLM-as-a-Judge problems

Very important for interviews.

### Problem 1 — Judge bias

The judge may prefer certain styles.

### Problem 2 — Position bias

Depending on how alternatives are presented, it may favor one.

### Problem 3 — Model bias

A weak judge can make bad evaluations.

### Problem 4 — Judge agrees with itself

If generator and judge are the same model, correlated errors can occur.

### Problem 5 — Cost

Every evaluation requires another model call.

### Problem 6 — Non-determinism

LLM judgments can vary.

Therefore:

> **LLM-as-a-judge is useful, but should not automatically be treated as ground truth.**

---

# 18. Human evaluation

Sometimes humans need to evaluate outputs.

Example:

You build a medical research assistant.

You might ask experts to rate:

```text
Correctness: 1–5
Relevance: 1–5
Clarity: 1–5
Safety: 1–5
```

Human evaluation provides high-quality judgments but is:

* expensive
* slow
* difficult to scale
* sometimes subjective

Therefore production systems often combine:

```text
Automated evaluation
+
LLM-as-judge
+
Human evaluation
```

---

# 19. Three major evaluation approaches

Memorize:

```text
                    EVALUATION
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
    Deterministic    LLM Judge      Human
```

### Deterministic

```text
Fast
Cheap
Reproducible
```

### LLM Judge

```text
Flexible
Semantic
Scalable
```

### Human

```text
High-quality
Expensive
Slow
```

A strong production system uses the appropriate combination.

---

# 20. Evaluating RAG

You've already learned RAG, so this is extremely important.

RAG has multiple stages:

```text
Question
 ↓
Retriever
 ↓
Documents
 ↓
Context
 ↓
LLM
 ↓
Answer
```

You shouldn't only evaluate the final answer.

Evaluate:

```text
Retriever
    ↓
Generation
```

---

# 21. Retrieval evaluation

Suppose the correct document is:

```text
document_42
```

Retriever returns:

```text
document_1
document_8
document_42
document_73
```

Good.

You can measure retrieval metrics such as:

* Recall@K
* Precision@K
* MRR
* NDCG

---

# 22. Recall@K

Question:

> Did the correct document appear within the top K results?

Example:

```text
Top 5:

1. doc1
2. doc4
3. doc7
4. doc42 ← correct
5. doc9
```

Then:

```text
Recall@5 = 1
```

If correct document isn't present:

```text
Recall@5 = 0
```

Across many queries:

```text
Recall@5 =
queries where relevant document appeared
────────────────────────────────────────
             total queries
```

This is very useful for RAG.

---

# 23. Generation evaluation in RAG

Suppose retrieved context is:

```text
"TCP is connection-oriented."
```

Model says:

```text
"TCP is connectionless."
```

The retrieval was correct.

Generation was wrong.

Therefore evaluate separately:

```text
Retrieval quality
+
Answer quality
```

This helps identify **where the system failed**.

---

# 24. Faithfulness / groundedness

Question:

> Is the answer supported by the provided context?

Context:

```text
Python was created by Guido van Rossum.
```

Answer:

```text
Python was created by Guido van Rossum.
```

Faithful.

But:

```text
Python was created by Dennis Ritchie.
```

Not faithful.

A common conceptual metric:

```text
Faithfulness =
claims supported by evidence
─────────────────────────────
       total claims
```

In practice, implementations vary.

---

# 25. Relevance

Question:

```text
What is Docker?
```

Answer:

```text
Docker is a platform for packaging
applications into containers...
```

Relevant.

But:

```text
Docker was founded in...
The history of containerization...
Linux namespaces...
```

could be technically related but not directly answer the question.

So:

```text
Correct ≠ Relevant
```

A response can be factually correct but poorly targeted.

---

# 26. RAG evaluation architecture

A useful mental model:

```text
                  RAG SYSTEM
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     RETRIEVAL              GENERATION
          │                     │
          ↓                     ↓
    Recall@K              Correctness
    Precision@K           Relevance
    MRR                   Faithfulness
    NDCG                  Groundedness
```

This distinction is important.

---

# 27. Agent evaluation

Now the most important part for **you**.

Traditional LLM:

```text
Input
 ↓
LLM
 ↓
Output
```

Agent:

```text
Input
 ↓
Agent
 ↓
Plan
 ↓
Tool
 ↓
Observation
 ↓
Tool
 ↓
Observation
 ↓
Final answer
```

Therefore:

> Evaluating only the final answer is insufficient.

You should evaluate the **trajectory**.

---

# 28. What is an agent trajectory?

Trajectory = the sequence of actions/steps an agent took to accomplish a task.

Example:

```text
User:
"Find the bug in auth.py."

Trajectory:

1. list_files()
2. read_file("auth.py")
3. search_code("token")
4. read_file("config.py")
5. final answer
```

That entire sequence is the agent's trajectory.

---

# 29. Agent trajectory evaluation

We can evaluate:

### Tool selection

Did the agent choose the correct tool?

### Tool arguments

Did it provide correct parameters?

### Ordering

Did it call tools in a sensible order?

### Efficiency

Did it make unnecessary calls?

### Task completion

Did it accomplish the task?

### Final answer

Was the final response correct?

---

# 30. Deterministic trajectory evaluation

Suppose expected:

```python
expected_tools = [
    "search_code",
    "read_file"
]
```

Agent:

```python
actual_tools = [
    "search_code",
    "read_file"
]
```

We can compare directly.

```python
def trajectory_match(
    actual,
    expected
):
    return actual == expected
```

This is excellent when there is a **known correct trajectory**.

But sometimes multiple trajectories can be valid.

---

# 31. Example of multiple valid trajectories

Task:

> Find where authentication is implemented.

Agent A:

```text
search_code("auth")
→ read_file("auth.py")
```

Agent B:

```text
list_files()
→ read_file("auth.py")
```

Agent C:

```text
search_code("login")
→ search_code("token")
→ read_file("security.py")
```

All could potentially be valid.

Therefore exact trajectory matching can be too strict.

This is where semantic/LLM-based trajectory evaluation becomes useful.

---

# 32. LLM judge for agent trajectory

Give the evaluator:

```text
Task
+
Agent trajectory
+
Tool outputs
+
Final answer
```

Then ask:

```text
Was the agent's behavior appropriate?

Did it select appropriate tools?

Did it use correct arguments?

Did it accomplish the task?

Did it take unnecessary actions?

Score 0–1.
```

Conceptually:

```text
Task
 │
 ↓
Agent
 │
 ├── Tool A
 │
 ├── Tool B
 │
 └── Final answer
       │
       ▼
    Judge LLM
       │
       ▼
Evaluation
```

This is exactly the type of agent-trajectory evaluation covered in modern LangChain/LangSmith evaluation workflows.

---

# 33. Task success

One of the most useful agent metrics.

Suppose:

```text
100 tasks
83 successfully completed
```

Then:

```text
Task Success Rate = 83%
```

For agents, this can be more meaningful than judging writing quality.

Example:

```text
Task:
Create a GitHub issue with the bug description.
```

Agent:

```text
Creates issue correctly
```

Success.

Even if its final sentence is not beautifully written.

---

# 34. Tool-call accuracy

Suppose agent needs:

```text
search_code()
```

but calls:

```text
delete_file()
```

That's a serious failure.

You can evaluate:

```text
Expected tool
vs
Actual tool
```

Example:

```python
expected = "search_code"
actual = "delete_file"

score = int(
    expected == actual
)
```

For some tasks, deterministic tool evaluation is extremely valuable.

---

# 35. Tool argument evaluation

Correct tool isn't enough.

Suppose:

```text
Tool:
get_weather(city)
```

Agent calls:

```python
get_weather("Mumbai")
```

when user asked:

```text
Bangalore
```

Tool selection:

```text
CORRECT
```

Tool arguments:

```text
WRONG
```

So evaluate both.

---

# 36. Agent efficiency

Suppose:

### Agent A

```text
search → read → answer
```

3 calls.

### Agent B

```text
search → search → search → list → read → read → read → answer
```

8 calls.

Both eventually succeed.

Which is more efficient?

You can measure:

```text
tool calls
latency
tokens
cost
retries
```

This is important in production.

---

# 37. Cost evaluation

Suppose:

```text
Agent A:
$0.02 / task

Agent B:
$0.40 / task
```

If both achieve similar quality, cost matters.

You can track:

```text
Input tokens
Output tokens
Model calls
Tool calls
API cost
```

So production evaluation isn't only:

```text
"Is the answer good?"
```

It is:

```text
Quality
+
Reliability
+
Latency
+
Cost
+
Safety
```

---

# 38. Latency evaluation

Imagine:

```text
Agent A → 2 seconds
Agent B → 45 seconds
```

Both have 95% task success.

For an interactive application, latency matters enormously.

Track:

```text
Average latency
P50
P95
P99
```

You should know these from system design already.

### P95

95% of requests finish within that latency.

The remaining 5% take longer.

This is a production engineering metric.

---

# 39. Regression testing

This is one of the **most important concepts in this entire level**.

Suppose your agent currently achieves:

```text
Accuracy = 92%
```

You modify the prompt.

Now:

```text
Accuracy = 84%
```

You accidentally made the system worse.

How do you detect this?

**Regression testing.**

---

# 40. Regression test mental model

```text
Old version
    ↓
Evaluation dataset
    ↓
92%

New version
    ↓
Same evaluation dataset
    ↓
84%

        ↓
REGRESSION DETECTED
```

So:

> **A regression test checks whether a change causes previously working behavior to break.**

---

# 41. Golden dataset

A very common concept.

Create a trusted set of important examples:

```text
golden_dataset.json
```

Example:

```json
[
  {
    "input": "What is TCP?",
    "expected": "TCP is connection-oriented..."
  },
  {
    "input": "What is DNS?",
    "expected": "DNS resolves domain names..."
  }
]
```

Whenever you change:

* prompt
* model
* retrieval
* tools
* agent logic
* guardrails

run the dataset again.

---

# 42. Regression pipeline

A production workflow might be:

```text
Developer changes agent
        ↓
Run tests
        ↓
Run evaluation dataset
        ↓
Calculate metrics
        ↓
Compare previous version
        ↓
Did quality drop?
     /       \
   YES        NO
   ↓           ↓
 BLOCK       DEPLOY
```

This is essentially **CI/CD for AI behavior**.

---

# 43. Traditional tests vs LLM evaluations

Very important distinction.

Traditional software:

```python
assert add(2, 2) == 4
```

Deterministic.

LLM:

```text
"Explain recursion."
```

Many answers can be correct.

Therefore:

```text
Traditional software
→ exact assertions

LLM systems
→ statistical/semantic evaluation
```

But deterministic tests are still extremely useful wherever possible.

---

# 44. Unit tests + evaluation tests

Don't replace traditional tests.

Use both.

```text
AI APPLICATION
│
├── Unit Tests
│   ├── Tool functions
│   ├── Validators
│   ├── Authorization
│   └── Business logic
│
├── Integration Tests
│   ├── MCP
│   ├── Database
│   └── APIs
│
└── AI Evaluations
    ├── Answer quality
    ├── Agent trajectory
    ├── RAG quality
    └── Task success
```

This is a very strong production architecture.

---

# 45. Build your own tiny evaluation framework

Before learning LangSmith or another platform, I want you to understand what is happening underneath.

Create:

```text
llm-evaluation/
│
├── dataset.json
├── agent.py
├── evaluators/
│   ├── exact_match.py
│   ├── llm_judge.py
│   └── trajectory.py
│
├── runner.py
└── results.json
```

---

# 46. Dataset

`dataset.json`

```json
[
  {
    "id": "tc1",
    "input": "What is 2 + 2?",
    "expected": "4"
  },
  {
    "id": "tc2",
    "input": "What is 3 + 5?",
    "expected": "8"
  }
]
```

---

# 47. Exact-match evaluator

```python
def exact_match(
    actual: str,
    expected: str
) -> bool:

    return (
        actual.strip().lower()
        ==
        expected.strip().lower()
    )
```

---

# 48. Evaluation runner

```python
import json


def run_evaluation(
    agent,
    dataset
):

    results = []

    for test_case in dataset:

        actual = agent.invoke(
            test_case["input"]
        )

        passed = exact_match(
            actual,
            test_case["expected"]
        )

        results.append({
            "id": test_case["id"],
            "input": test_case["input"],
            "expected": test_case["expected"],
            "actual": actual,
            "passed": passed
        })

    return results
```

Then calculate:

```python
def accuracy(results):

    correct = sum(
        result["passed"]
        for result in results
    )

    return correct / len(results)
```

You've just built the skeleton of an evaluation framework.

---

# 49. Now make it Agentic AI-specific

Instead of only storing:

```json
{
    "input": "...",
    "expected": "..."
}
```

store:

```json
{
    "id": "code_001",
    "input": "Find where authentication is implemented",
    "expected_tools": [
        "search_code",
        "read_file"
    ],
    "expected_behavior": "Identify authentication implementation",
    "category": "code_analysis"
}
```

Now you can evaluate:

```text
Final answer
+
Tool selection
+
Tool arguments
+
Task completion
```

This is much closer to real Agent Evaluation.

---

# 50. Evaluator architecture

I recommend thinking of an evaluator as:

```text
             Test Case
                 │
                 ↓
              Agent
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Output   Trajectory  Metrics
       │         │         │
       └─────────┼─────────┘
                 ↓
              Evaluator
                 ↓
              Score
```

---

# 51. Score-based evaluation

Instead of:

```text
PASS / FAIL
```

you can use:

```text
0 → Completely wrong
1 → Poor
2 → Partially correct
3 → Mostly correct
4 → Excellent
```

Example:

```python
{
    "correctness": 4,
    "relevance": 5,
    "faithfulness": 4
}
```

Then aggregate.

But be careful with arbitrary scoring systems; define what each score means.

---

# 52. Evaluation rubric

For an LLM judge, don't just say:

```text
"Rate this answer."
```

Give explicit criteria.

Example:

```text
Score correctness from 0 to 4.

0 = completely incorrect
1 = mostly incorrect
2 = partially correct
3 = mostly correct
4 = fully correct

Evaluate only factual correctness.
Do not reward verbosity.
```

This improves consistency.

---

# 53. Better LLM-as-a-Judge

Instead of asking:

```text
Is this good?
```

ask:

```text
Evaluate the answer against these criteria:

1. Correctness
2. Relevance
3. Completeness

Return JSON:

{
  "correctness": 0-4,
  "relevance": 0-4,
  "completeness": 0-4,
  "reason": "..."
}
```

Then validate the judge output with Pydantic.

Notice how your **Guardrails knowledge** comes back here.

```text
LLM Judge
   ↓
Structured Output
   ↓
Pydantic
   ↓
Evaluation Result
```

---

# 54. Pairwise evaluation

Another technique.

Instead of:

```text
"Is answer A good?"
```

compare:

```text
Answer A
vs
Answer B
```

Judge:

```text
Which answer better satisfies the criteria?
```

Useful when comparing:

```text
Prompt v1
vs
Prompt v2
```

or:

```text
Model A
vs
Model B
```

or:

```text
Retriever A
vs
Retriever B
```

But pairwise judges can also have biases, so don't treat the result as absolute truth.

---

# 55. Evaluation experiment

Suppose you change your system prompt.

You have:

```text
Version A
```

and:

```text
Version B
```

Run both against:

```text
100 test cases
```

Results:

```text
              Version A    Version B

Correctness      88%          92%
Relevance        91%          93%
Latency          1.8s         2.2s
Cost             $0.02        $0.05
```

Now you have an **experiment**.

This is much more meaningful than:

> "Version B feels better."

---

# 56. Evaluation matrix

For Agentic AI, I'd track something like:

| Dimension      | What you're measuring               |
| -------------- | ----------------------------------- |
| Correctness    | Is answer factually/task correct?   |
| Relevance      | Does it answer the actual question? |
| Faithfulness   | Is it supported by evidence?        |
| Task success   | Did agent accomplish task?          |
| Tool accuracy  | Did it choose correct tools?        |
| Tool arguments | Were parameters correct?            |
| Efficiency     | How many steps/tools?               |
| Safety         | Did it violate policy?              |
| Latency        | How quickly did it respond?         |
| Cost           | How expensive was execution?        |

This is much closer to real AI engineering.

---

# 57. Online vs offline evaluation

Another interview topic.

## Offline evaluation

Run against a fixed dataset.

```text
dataset
 ↓
agent
 ↓
evaluate
```

Useful before deployment.

---

## Online evaluation

Evaluate real production traffic.

```text
Real user
 ↓
Production agent
 ↓
Trace
 ↓
Evaluation
```

Useful after deployment.

For example:

```text
Production traffic
        ↓
sample 5%
        ↓
LLM evaluator
        ↓
quality metrics
```

This allows continuous monitoring.

---

# 58. Offline + Online

A mature system uses both:

```text
                 AI SYSTEM
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
       OFFLINE                ONLINE
       EVALS                  EVALS
          │                     │
      Before deploy         After deploy
          │                     │
          └──────────┬──────────┘
                     ↓
                 Monitoring
```

---

# 59. Evaluation dataset design

This is often overlooked.

A bad dataset gives misleading evaluation.

Your dataset should contain:

### Normal cases

```text
"What is Docker?"
```

### Edge cases

```text
""
Very long input
Ambiguous questions
```

### Difficult cases

```text
Complex reasoning
Multi-step tasks
```

### Adversarial cases

```text
Prompt injection
Malformed input
Tool abuse
```

### Regression cases

Previous failures.

---

# 60. Your dataset should grow from failures

This is a very important engineering practice.

Suppose production failure:

```text
User asks:
"Find refund policy."

Agent retrieves:
wrong document.
```

Add that exact scenario to your evaluation dataset.

Now:

```text
Production failure
       ↓
Add test case
       ↓
Fix system
       ↓
Run regression suite
       ↓
Deploy
```

This creates a continuously improving system.

---

# 61. Evaluation flywheel

This is one of the best mental models from this entire level.

```text
             ┌───────────────┐
             │   Production  │
             │    Traffic    │
             └───────┬───────┘
                     ↓
                  Failures
                     ↓
              Evaluation Set
                     ↓
                  Testing
                     ↓
                  Improve
                     ↓
                  Deploy
                     ↓
                Production
                     │
                     └─────────→
```

Your evaluation dataset becomes increasingly valuable over time.

---

# 62. Agent trajectory example

Suppose user asks:

> "Find the bug in authentication and explain how to fix it."

Agent trajectory:

```text
1. list_files()
2. search_code("auth")
3. read_file("auth.py")
4. read_file("config.py")
5. search_code("JWT")
6. final_answer
```

We could record:

```python
trajectory = {
    "tools": [
        {
            "name": "list_files",
            "arguments": {}
        },
        {
            "name": "search_code",
            "arguments": {
                "query": "auth"
            }
        },
        {
            "name": "read_file",
            "arguments": {
                "path": "auth.py"
            }
        }
    ]
}
```

Now the evaluator can inspect the **whole process**.

---

# 63. Evaluating agent trajectory

Possible metrics:

```text
Tool correctness
Tool argument correctness
Unnecessary calls
Number of calls
Task completion
Final answer correctness
```

For example:

```python
def tool_accuracy(
    actual_tools,
    expected_tools
):

    correct = 0

    for tool in actual_tools:

        if tool in expected_tools:
            correct += 1

    return correct / len(
        actual_tools
    )
```

This is simplistic, but demonstrates the idea.

---

# 64. Why trajectory evaluation matters

Imagine two agents both produce:

```text
"Authentication bug is caused by an expired JWT."
```

Final answer appears correct.

But:

### Agent A

```text
read_file("auth.py")
→ identifies JWT expiration
```

### Agent B

```text
read_file("database.py")
→ delete_file("auth.py")
→ random web search
→ guesses JWT
```

Same final answer.

Completely different behavior.

Therefore:

> **Final-answer evaluation alone cannot fully evaluate an agent.**

This is one of the most important things I want you to remember from Level 31.

---

# 65. Safety evaluation

Because you just learned Guardrails, connect them.

Evaluate whether:

```text
Agent
 ↓
Tool request
```

violated policy.

Examples:

```text
Unauthorized database access
Unauthorized file access
Unsafe tool invocation
PII leakage
Prompt injection success
```

So your evaluation framework can measure:

```text
Safety violation rate
```

For example:

```text
100 adversarial tests
3 violations

Violation Rate = 3%
```

---

# 66. Evaluation of your Guardrails

This is a beautiful connection between Level 29 and 31.

You shouldn't just build:

```text
Prompt injection detector
```

You should test it.

Dataset:

```text
100 legitimate inputs
100 injection attempts
```

Then calculate:

```text
Precision
Recall
False positive rate
False negative rate
```

Now you're actually **evaluating the guardrail**.

---

# 67. Evaluation hierarchy

You can think of your entire Agentic AI stack as:

```text
                 AI SYSTEM
                     │
      ┌──────────────┼──────────────┐
      ↓              ↓              ↓
    MODEL          AGENT         TOOLS
      │              │              │
      └──────────────┼──────────────┘
                     ↓
                EVALUATION
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    Output       Trajectory      Safety
       │             │             │
       └─────────────┼─────────────┘
                     ↓
                  Metrics
```

---

# 68. Observability vs Evaluation

Another important distinction.

### Observability

> What happened?

Example:

```text
Agent called search_code()
Agent called read_file()
Latency = 2.4 sec
Tokens = 4,200
```

### Evaluation

> Was what happened good?

Example:

```text
Tool selection = correct
Final answer = correct
Task success = true
```

So:

```text
Observability → collect what happened
Evaluation → judge what happened
```

You need both.

---

# 69. Traces

A trace records an execution.

Example:

```text
TRACE
│
├── User input
│
├── Agent decision
│
├── Tool call
│
├── Tool result
│
├── LLM call
│
├── Tool call
│
└── Final answer
```

This is incredibly useful for Agentic AI.

Without traces:

```text
"Why did the agent do that?"
```

Hard to answer.

With traces:

```text
"Oh, it retrieved document X,
then selected tool Y,
because the previous result contained Z."
```

---

# 70. Evaluation + tracing

This gives you:

```text
                    TRACE
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
   Tool Calls      LLM Calls      Output
       │              │              │
       └──────────────┼──────────────┘
                      ↓
                  EVALUATORS
                      ↓
                   METRICS
```

This is the foundation of AI observability platforms such as LangSmith.

---

# 71. What I expect you to know about LangSmith

Don't memorize every API.

Understand the concepts:

```text
Dataset
Experiment
Run
Trace
Evaluator
Feedback
Comparison
Regression
```

A typical workflow:

```text
Create dataset
      ↓
Run agent
      ↓
Collect traces
      ↓
Run evaluators
      ↓
Calculate metrics
      ↓
Compare versions
```

That is what matters.

---

# 72. Production evaluation architecture

Now let's combine everything you've learned.

```text
                       USER
                         │
                         ▼
                  ┌─────────────┐
                  │   AGENT     │
                  └──────┬──────┘
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
             LLM       Tools       RAG
              │          │          │
              └──────────┼──────────┘
                         ↓
                      TRACE
                         ↓
               ┌──────────────────┐
               │   EVALUATION     │
               ├──────────────────┤
               │ Correctness      │
               │ Relevance        │
               │ Faithfulness     │
               │ Tool accuracy    │
               │ Task success     │
               │ Safety           │
               │ Latency          │
               │ Cost             │
               └────────┬─────────┘
                        ↓
                    DASHBOARD
                        ↓
                  IMPROVEMENT
                        ↓
                  REGRESSION TEST
                        ↓
                     DEPLOY
```

---

# 73. The complete AI engineering loop

This is probably the most important diagram of Level 31:

```text
             ┌───────────────────┐
             │   Build Agent     │
             └─────────┬─────────┘
                       ↓
                  Create Dataset
                       ↓
                  Run Evaluation
                       ↓
                  Analyze Failures
                       ↓
                     Improve
                       ↓
                 Run Regression
                       ↓
                 Deploy Version
                       ↓
                Monitor Production
                       ↓
                Collect Failures
                       │
                       └─────────────┐
                                     ↓
                              Update Dataset
                                     ↓
                               Evaluate Again
```

**This is how production AI systems evolve.**

---

# 74. Interview question: How would you evaluate an AI agent?

A strong answer:

> "I would evaluate the agent at multiple levels rather than only checking the final response. I'd create a representative evaluation dataset containing normal, edge, adversarial, and historical failure cases. I'd use deterministic evaluators wherever possible, LLM-as-a-judge for semantic criteria, and human evaluation for high-value or ambiguous cases. For agents I'd evaluate tool selection, tool arguments, trajectory, task completion, final-answer correctness, safety, latency and cost. I'd maintain regression tests so changes to prompts, models, retrieval, or tools don't silently degrade existing behavior."

That's a **very good interview answer**.

---

# 75. Interview: What is LLM-as-a-Judge?

> An LLM-as-a-Judge uses an evaluator model to assess another model's output against specified criteria such as correctness, relevance, faithfulness, or task completion.

Then immediately mention limitations:

> It can introduce evaluator bias, inconsistency, correlated model errors, and additional cost, so I wouldn't rely on it as the only evaluation mechanism.

That second sentence makes your answer much stronger.

---

# 76. Interview: How do you evaluate an agent differently from a chatbot?

Answer:

```text
Chatbot:
Input → Output

Agent:
Input
 ↓
Planning
 ↓
Tool selection
 ↓
Tool arguments
 ↓
Tool execution
 ↓
Observations
 ↓
Iteration
 ↓
Final output
```

Therefore:

> "For an agent I evaluate both the final result and the execution trajectory."

---

# 77. Interview: What is regression testing for LLMs?

> "Regression testing means running a stable evaluation dataset against every meaningful system change and comparing the new results with a previous baseline to detect quality or behavior degradation."

Changes could include:

```text
Prompt
Model
RAG
Retriever
Embedding model
Tool
Agent graph
Guardrails
MCP server
```

---

# 78. Interview: How do you evaluate RAG?

Say:

> "I separate retrieval evaluation from generation evaluation."

Then:

```text
Retrieval:
Recall@K
Precision@K
MRR
NDCG

Generation:
Correctness
Relevance
Faithfulness
Groundedness
Citation accuracy
```

That's an excellent interview answer.

---

# 79. Interview: How do you evaluate tool usage?

Evaluate:

```text
1. Was the correct tool selected?
2. Were arguments correct?
3. Was the tool called at the right time?
4. Were unnecessary calls made?
5. Was the tool result interpreted correctly?
6. Was the task successfully completed?
```

This is exactly the mindset companies want for Agentic AI systems.

---

# 80. Interview: What makes a good evaluation dataset?

A strong dataset should be:

```text
Representative
Diverse
Difficult
Adversarial
Versioned
Grounded in real failures
```

Include:

```text
Normal cases
Edge cases
Ambiguous cases
Adversarial cases
Historical production failures
Regression cases
```

---

# 81. Your Level 31 mini-project

Again, **don't build a huge application**.

Build:

# 🧪 Agent Evaluation Framework

Architecture:

```text
                         DATASET
                            │
                            ▼
                     ┌────────────┐
                     │   Agent    │
                     └─────┬──────┘
                           │
                    ┌──────┼──────┐
                    ↓      ↓      ↓
                  Output  Tools  Trace
                    │      │      │
                    └──────┼──────┘
                           ↓
                     EVALUATORS
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
        Deterministic   LLM Judge    Human
              │            │            │
              └────────────┼────────────┘
                           ↓
                        METRICS
                           ↓
                    REGRESSION TEST
```

Implement:

```text
dataset.json
     ↓
run_agent()
     ↓
collect trace
     ↓
exact-match evaluator
     ↓
tool evaluator
     ↓
LLM judge
     ↓
calculate metrics
     ↓
save results
```

Then add:

```text
baseline.json
```

and compare:

```text
Version 1
vs
Version 2
```

---

# 82. What your project should evaluate

For your first version:

### Level 1 — Deterministic

```text
Exact match
Tool selection
Tool arguments
Task success
```

### Level 2 — Semantic

```text
Correctness
Relevance
Faithfulness
```

using an LLM judge.

### Level 3 — Engineering

```text
Latency
Token usage
Number of tool calls
Cost
```

### Level 4 — Regression

```text
Version A
vs
Version B
```

This is enough to make the project educational without becoming another giant project.

---

# 83. The biggest mistakes I don't want you to make

### ❌ Mistake 1

Only evaluate final answers.

### ❌ Mistake 2

Use only an LLM judge.

### ❌ Mistake 3

Use only exact matching.

### ❌ Mistake 4

Have a tiny, unrealistic dataset.

### ❌ Mistake 5

Never test adversarial cases.

### ❌ Mistake 6

Don't preserve previous failures.

### ❌ Mistake 7

Ignore latency and cost.

### ❌ Mistake 8

Don't compare versions.

### ❌ Mistake 9

Assume a high average score means the system is reliable.

---

# 84. The complete Agentic AI evaluation stack

You have now reached an important point.

```text
                    AGENT
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      INPUT         PROCESS       OUTPUT
        │             │             │
        ↓             ↓             ↓
    Validation    Trajectory     Quality
    Safety        Tool calls     Correctness
    PII           Planning       Relevance
    Injection     Routing        Faithfulness
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                  EVALUATION
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
    Deterministic   LLM Judge   Human
          │           │           │
          └───────────┼───────────┘
                      ↓
                   METRICS
                      ↓
                REGRESSION
                      ↓
                 IMPROVEMENT
```

---

# 85. Your Agentic AI roadmap is now almost complete

You have:

```text
LEVEL 24 ── LangChain
     ↓
LEVEL 25 ── LangGraph
     ↓
LEVEL 26 ── Multi-Agent
     ↓
LEVEL 27 ── Deep Agents
     ↓
LEVEL 28 ── MCP
     ↓
LEVEL 29 ── Guardrails
     ↓
LEVEL 31 ── LLM Evaluation  ← YOU ARE HERE
```

At this point, you have learned the **core architecture concepts** needed to build serious agentic systems.

The next phase shouldn't be another 20 levels of theory.

It should be:

```text
                    YOUR KNOWLEDGE
                          │
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
    Build               Evaluate           Secure
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ↓
                 RESUME-WORTHY PROJECT
                          ↓
                 Production Architecture
                          ↓
                   GitHub + README
                          ↓
                     Resume
```

And importantly, your final resume project can now combine **Deep Agents + LangGraph + MCP + Guardrails + Evaluation + RAG + Multi-Agent architecture** rather than being just another "chatbot with an LLM."

### The one sentence to remember from Level 31

> **LLM evaluation is the systematic process of measuring an AI system's quality, reliability, safety, and behavior against representative test cases, using deterministic checks, model-based evaluators, and human judgment, then using those results to improve the system and prevent regressions.**

That is the mindset I want you to carry into your project phase.
