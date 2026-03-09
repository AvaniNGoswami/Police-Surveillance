# Police Surveillance Intelligence System


## Demo Video
[▶ https://youtube.com/your-demo-link](https://drive.google.com/file/d/1hjuIEq302YSvRojcGvyoOfd03Lrd60XD/view?usp=drivesdk)

Short demonstration of the system performing:

detect → event creation → alert → hourly summary generation



Problem Statement

Urban monitoring requires automated detection of situational risks such as:
- Loitering behavior
- Unattended objects
- Sudden crowd density spikes

The objective is to assist law enforcement with structured situational awareness while preserving human oversight and minimizing false positives.

## System Architecture

![Architecture Diagram](https://github.com/user-attachments/assets/0c0d1a28-bf38-486e-9b4b-1319cbdab829)

Layer Responsibilities
Layer                                                                    	Responsibility
Detection	                                                                Detect persons / objects in frame
Event Engine	                                                            Apply temporal + spatial rules to detect events
Database	                                                                Store structured event records
Vector Store	                                                            Store embeddings of event descriptions
RAG Layer	                                                                Retrieve semantically similar past events
LLM                                                                      	Generate grounded operational summaries
Dashboard	                                                                Display alerts and reports


Important architectural principle:

The database is the source of truth.
The vector store augments it with semantic retrieval.

## Event Reasoning Logic

The system does not trigger events on single frames.

Each event type has reasoning rules:

### Loitering
- Same person remains in defined zone
- Duration exceeds time threshold
- Confidence above threshold

### Unattended Object
- Object present
- No associated person nearby
- Duration threshold satisfied

### Crowd Surge
- Person density exceeds zone threshold
- Sustained for defined time window

Events are created only when temporal continuity is satisfied.

This reduces noisy frame-level alerts.

## Data Flow
![Data Flow Diagram](https://github.com/user-attachments/assets/4b012321-9dfb-4277-a40a-43e5b8debf83)

The vector store sits between the database and the LLM.

It is used only during contextual retrieval.

## Retrieval-Augmented Generation (RAG)

The system uses:

SentenceTransformer: all-MiniLM-L6-v2

FAISS (IndexFlatL2) for similarity search

Each stored event is converted into structured text:

"{event_type} occurred at zone {zone} 
 confidence {confidence} 
 time {timestamp}"

Embeddings are stored in FAISS.

When generating summaries:
- The query is embedded
- Top-k similar events are retrieved
- Retrieved events are injected into the LLM prompt

This ensures summaries are:
- Grounded in past incidents
- Context-aware
- Non-generic
- Not chatbot-style responses

## Event Lifecycle

![Event Lifecycle Diagram](https://github.com/user-attachments/assets/ac5026b9-7017-498c-b741-40a6cdcf2e55)

Human review is part of the loop.

The LLM does not trigger actions.
It only produces summaries.

Operational decisions remain human-controlled.

## Safety & False Positive Mitigation

Events require sustained conditions over time.

- 2. Spatial Constraints

Zones must be predefined.

- 3. Human Verification

All alerts are reviewable before resolution.

- 5. LLM Safety

The LLM:

  - Does not automate decisions
  - Does not control actions
  - Only generates contextual summaries

This prevents automation bias.

8. Sample Outputs
   
  Detection Logs
<img width="1396" height="370" alt="detection_logs" src="https://github.com/user-attachments/assets/c03835a3-b45b-4d3c-9cef-8a22543c22b5" />



Event Record Stored in Database
<img width="1517" height="343" alt="event_record" src="https://github.com/user-attachments/assets/4c0dab45-3f96-4b38-ad5c-9839a07eb4ba" />



Generated Event Summary

<img width="804" height="822" alt="summary" src="https://github.com/user-attachments/assets/380f9de5-7215-4759-8988-15cd8eae3efb" />

Grounded. Operational. Not conversational.

## Why This System Is Not a Chatbot
- The LLM is not used for detection.
- The LLM is not used for decision-making.
- The LLM is not used for conversation.
- It is used for structured summarization grounded in retrieved events.
- That is meaningful LLM usage.

## Design Principles
- Event reasoning over frame detection
- Database as single source of truth
- Vector store as semantic layer
- Retrieval before generation
- Human in the loop
- Safety over automation

## What This Demonstrates
- System thinking
- Event lifecycle modeling
- RAG integration beyond chatbots
- Operational awareness
- Safety-first AI design
