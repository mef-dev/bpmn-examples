# Incident Management TMF724
The Incident Co-Pilot leverages a sophisticated multi-agent architecture designed to enhance the efficiency and effectiveness of NOC engineers. This architecture seamlessly integrates advanced AI technologies, including LLMs and real-time data processing, to deliver comprehensive incident management and resolution capabilities.

The process begins with the NOC Engineer, who initiates the workflow by providing prompts to the Incident Co-Pilot. These prompts, ranging from simple queries to complex commands, are the starting point for the incident management process. The Incident Co-Pilot serves as the central orchestrator. It interprets the NOC Engineer’s prompts, sets goals, and provides context for the tasks at hand. Acting as the hub of the system, the Incident Co-Pilot determines which specialized agents to instantiate from the Agent Repository based on the nature of the incident.

Once the appropriate agent is selected, the Network Incident Agent is instantiated. This agent refines the engineer’s prompt by adding necessary context and querying a comprehensive Vectorized Knowledge Base and Real-Time Data sources. This allows the agent to gather all relevant information needed to address the incident thoroughly. The system utilizes various Foundation Models such as LLaMa3, Google Gemma, OpenAI GPT-4, and Mistral. These models are integrated to enhance the response capabilities of the Network Incident Agent, ensuring that the information and solutions provided are both sophisticated and relevant.

The Agent Knowledge component is crucial to the operation. It comprises two main parts:
1. **Vectorized Knowledge Base**. This includes unstructured text, Q&A pairs, rules, constraints, and knowledge graphs. It provides a deep well of contextual information that the agents draw upon to perform their tasks.
2. **Real-Time Data**. This component includes current network data such as alarms and topology, ensuring that the agents’ actions are based on the latest available information.

In short, the overall workflow follows a clear and systematic process:
* The NOC Engineer issues a prompt.
* The Incident Co-Pilot receives the prompt, sets the goal, and adds context.
* The Incident Co-Pilot instantiates the Network Incident Agent.
* The Network Incident Agent queries the Vectorized Knowledge Base and Real-Time Data sources.
* The Agent refines the prompt and sends it to the LLM for a response.
* The LLM processes the refined prompt and generates a response.
The Network Incident Agent uses this response to address the incident.
The results are returned back to the Incident Co-Pilot and presented to the NOC Engineer.

## The Workflow
![Incident Diagnosis Flow](https://github.com/mef-dev/bpmn-examples/blob/dev/tmforum-apis/TMF724_Incident_Management/1.%20Incident%20Diagnosis%20Flow.png)
|:--:|

The BPMN workflow above demonstrates what is happening underneath the hood of Incident Co-Pilot Catalyst on the multi-vendor incident diagnosis orchestration level.

Orchestration begins with receiving an API request from the NOC engineer’s software to diagnose the incident. At stage 1, MEF.DEV Platform validates the request, checks if Qvantel’s trouble ticketing API is available, and creates the corresponding trouble ticket using TM Forum’s standardized TMF621 Trouble Ticket API.

Next, the platform has to check which vendor will perform incident diagnosis, selecting between 3 options depending on the incident category:
1. For device-based incidents, the gateway forwards further incident diagnosis to Infosys (stage 2.2);
2. For network-based incidents, MEF.DEV Platform performs Root Cause Analysis (RCA) to diagnose the incident (stage 2.3);
3. For all the remaining incident categories, the gateway forwards further incident diagnosis to Huawei (stage 2.1).
4. If the incident is network-based, the platform calls another BPMN flow (presented below) that generates a suggested resolution according to the TMF724 Incident Management API model.

![Root Cause Analysis Flow](https://github.com/mef-dev/bpmn-examples/blob/dev/tmforum-apis/TMF724_Incident_Management/2.%20Root%20Cause%20Analysis%20Flow.png)
|:--:|

The RCA begins with checking the list of alarms. If the list of alarms is present, the platform prepares a request to a corresponding LLM model by building embeddings, referring to a database of manuals and a history of alarms from other vendors (stages 1 & 2). The goal is to identify the alarm that initially caused the incident and define how to resolve it using vendors’ documentation. At this step, MEF.DEV Platform also adds information about network topology (stage 2).

Next, the platform performs prompt engineering based on either “One Shot” or “Chain of Thoughts” technologies. It uses the unified SuggestResolution Prompting to access RAG, forming the suggested incident resolution (stage 3, SuggestResolution prompt example).

Next, the suggested resolution is packed into the incident diagnosis object following the TMF724 API and returned back to the main incident diagnosis BPMN flow presented in the first workflow picture (stage 4). Finally, depending on the incident diagnosis feasibility, the platform returns a successful response in a TMF724 Incident Management API model or an error.
