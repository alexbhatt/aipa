import os
import json
import requests
from base64 import b64encode

class JiraTicketGenerator:
    def __init__(self, jira_url, email, api_token, project_key):
        """
        Initialize the JIRA ticket generator
        
        Args:
            jira_url: Your JIRA instance URL (e.g., 'https://your-domain.atlassian.net')
            email: Your JIRA account email
            api_token: Your JIRA API token
            project_key: The key of your JIRA project
        """
        self.jira_url = jira_url
        self.project_key = project_key
        self.auth_header = self._create_auth_header(email, api_token)
        
    def _create_auth_header(self, email, api_token):
        """Create the authentication header for JIRA API requests"""
        auth_str = f"{email}:{api_token}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = b64encode(auth_bytes).decode("utf-8")
        return {"Authorization": f"Basic {auth_b64}"}
    
    def create_epic(self, epic_name, epic_summary, epic_description):
        """
        Create an epic in JIRA
        
        Args:
            epic_name: The name of the epic
            epic_summary: A brief summary of the epic
            epic_description: Detailed description of the epic
            
        Returns:
            The key of the created epic
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_header
        }
        
        # The customfield ID for Epic Name varies per instance
        # You'll need to replace 'customfield_10011' with your actual Epic Name field ID
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": epic_summary,
                "description": epic_description,
                "issuetype": {"name": "Epic"},
                "customfield_10011": epic_name  # This is commonly the Epic Name field
            }
        }
        
        response = requests.post(
            f"{self.jira_url}/rest/api/2/issue/",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 201:
            return response.json()["key"]
        else:
            print(f"Failed to create epic: {response.text}")
            return None
    
    def create_story(self, epic_key, story_summary, story_description, components=None, labels=None):
        """
        Create a user story in JIRA and link it to an epic
        
        Args:
            epic_key: The key of the parent epic
            story_summary: A brief summary of the story
            story_description: Detailed description of the story
            components: List of component names to associate with the story
            labels: List of labels to add to the story
            
        Returns:
            The key of the created story
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_header
        }
        
        # Prepare components field if provided
        components_field = None
        if components:
            components_field = [{"name": comp} for comp in components]
        
        # The customfield ID for Epic Link varies per instance
        # You'll need to replace 'customfield_10014' with your actual Epic Link field ID
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": story_summary,
                "description": story_description,
                "issuetype": {"name": "Story"},
                "customfield_10014": epic_key,  # This is commonly the Epic Link field
            }
        }
        
        # Add components if provided
        if components_field:
            payload["fields"]["components"] = components_field
            
        # Add labels if provided
        if labels:
            payload["fields"]["labels"] = labels
        
        response = requests.post(
            f"{self.jira_url}/rest/api/2/issue/",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 201:
            return response.json()["key"]
        else:
            print(f"Failed to create story: {response.text}")
            return None
            
    def create_subtask(self, parent_key, subtask_summary, subtask_description):
        """
        Create a subtask in JIRA and link it to a parent issue
        
        Args:
            parent_key: The key of the parent issue
            subtask_summary: A brief summary of the subtask
            subtask_description: Detailed description of the subtask
            
        Returns:
            The key of the created subtask
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_header
        }
        
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": subtask_summary,
                "description": subtask_description,
                "issuetype": {"name": "Sub-task"},
                "parent": {"key": parent_key}
            }
        }
        
        response = requests.post(
            f"{self.jira_url}/rest/api/2/issue/",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 201:
            return response.json()["key"]
        else:
            print(f"Failed to create subtask: {response.text}")
            return None

def generate_project_tickets():
    # Replace these with your actual JIRA credentials and project information
    jira_url = "https://your-domain.atlassian.net"
    email = "your-email@example.com"
    api_token = "your-api-token"
    project_key = "APA"  # AI Personal Assistant
    
    jira = JiraTicketGenerator(jira_url, email, api_token, project_key)
    
    # Dictionary to store epic keys for reference
    epic_keys = {}
    
    # Create Epic 1: Core Infrastructure Setup
    epic1_desc = """
    This epic covers the setup of the core infrastructure for the AI Personal Assistant project.
    It includes database setup, backend API creation, and prototype UI development.
    
    **Epic Dependencies:** None - Starting point
    """
    epic_keys["epic1"] = jira.create_epic("Core Infrastructure Setup", "Epic 1: Core Infrastructure Setup", epic1_desc)
    
    # Create Story 1.1: Supabase Configuration
    story1_1_desc = """
    ## Supabase Configuration (Week 1)
    
    **Dependencies:** None
    
    **Tasks:**
    - Create Supabase account and project
    - Set up authentication system
    - Enable pgvector extension
    - Implement database schema
    
    **Technologies:** Supabase, PostgreSQL, SQL, pgvector
    
    **Documentation:**
    - [Supabase Documentation](https://supabase.com/docs)
    - [pgvector Documentation](https://github.com/pgvector/pgvector)
    - [Vector Embeddings with Supabase](https://supabase.com/docs/guides/database/extensions/pgvector)
    
    **Expected Outcome:** Functioning database with authentication and vector capabilities
    
    **Detailed Steps:**
    1. Create Supabase account at supabase.com
    2. Create new project with a descriptive name
    3. Navigate to SQL Editor and run: `create extension vector;`
    4. Execute database schema SQL from project plan
    5. Configure row-level security policies for tables
    6. Set up email authentication provider
    7. Test vector operations with sample embeddings
    
    **Learning Resources:**
    - [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
    - [Postgres Vector Cheatsheet](https://github.com/pgvector/pgvector/blob/master/README.md#usage)
    - [Authentication with Supabase](https://supabase.com/docs/guides/auth)
    """
    story1_1_key = jira.create_story(epic_keys["epic1"], "Story 1.1: Supabase Configuration", story1_1_desc, 
                                     components=["Database"], labels=["week-1"])
    
    # Create subtasks for Story 1.1
    jira.create_subtask(story1_1_key, "Create Supabase account and project", 
                       "Sign up for Supabase and create a new project for the AI Personal Assistant.")
    
    jira.create_subtask(story1_1_key, "Enable pgvector extension", 
                       "Run SQL command to enable the pgvector extension in the Supabase database.")
    
    jira.create_subtask(story1_1_key, "Implement database schema", 
                       "Create database tables according to the schema defined in the project plan.")
    
    jira.create_subtask(story1_1_key, "Configure row-level security", 
                       "Set up row-level security policies to ensure proper data access control.")
    
    jira.create_subtask(story1_1_key, "Set up authentication system", 
                       "Configure email authentication provider and test user signup/login flow.")
    
    # Create Story 1.2: FastAPI Backend
    story1_2_desc = """
    ## FastAPI Backend (Week 2)
    
    **Dependencies:** Story 1.1
    
    **Tasks:**
    - Set up FastAPI project structure
    - Configure Supabase client connection
    - Create basic API endpoints
    - Implement authentication middleware
    
    **Technologies:** Python, FastAPI, Pydantic, Supabase-py
    
    **Documentation:**
    - [FastAPI Documentation](https://fastapi.tiangolo.com/)
    - [Supabase Python Client](https://github.com/supabase-community/supabase-py)
    - [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
    
    **Expected Outcome:** Working API server with Supabase connection and authentication
    
    **Detailed Steps:**
    1. Set up virtual environment: `python -m venv venv`
    2. Install dependencies: `pip install fastapi uvicorn supabase pydantic python-dotenv`
    3. Create project structure
    4. Create Supabase client in config.py
    5. Implement JWT verification middleware
    6. Create basic health check endpoints
    7. Add user authentication routes
    
    **Learning Resources:**
    - [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
    - [Dependency Injection in FastAPI](https://fastapi.tiangolo.com/tutorial/dependencies/)
    - [JWT Authentication in FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
    """
    story1_2_key = jira.create_story(epic_keys["epic1"], "Story 1.2: FastAPI Backend", story1_2_desc, 
                                     components=["Backend"], labels=["week-2"])
    
    # Create subtasks for Story 1.2
    jira.create_subtask(story1_2_key, "Set up FastAPI project structure", 
                       "Create the directory structure and initial files for the FastAPI application.")
    
    jira.create_subtask(story1_2_key, "Configure Supabase client connection", 
                       "Set up the Supabase client in the FastAPI application with proper environment variables.")
    
    jira.create_subtask(story1_2_key, "Implement authentication middleware", 
                       "Create middleware to verify JWT tokens from Supabase auth.")
    
    jira.create_subtask(story1_2_key, "Create basic API endpoints", 
                       "Implement health check and initial API endpoints.")
    
    # Create Story 1.3: Streamlit Prototype
    story1_3_desc = """
    ## Streamlit Prototype (Week 3)
    
    **Dependencies:** Story 1.2
    
    **Tasks:**
    - Initialize Streamlit project
    - Create basic authentication flow
    - Implement simple UI components
    - Connect to FastAPI endpoints
    
    **Technologies:** Python, Streamlit, Requests
    
    **Documentation:**
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Streamlit Authentication](https://docs.streamlit.io/knowledge-base/deploy/authentication)
    
    **Expected Outcome:** Basic functional web interface for testing core features
    
    **Detailed Steps:**
    1. Install Streamlit: `pip install streamlit requests`
    2. Create project structure
    3. Implement Supabase authentication flow
    4. Create session management
    5. Build basic chat interface component
    6. Create API client to communicate with FastAPI backend
    
    **Learning Resources:**
    - [Streamlit Tutorial](https://docs.streamlit.io/get-started)
    - [Building Streamlit Apps](https://docs.streamlit.io/library/get-started/create-an-app)
    - [Session State in Streamlit](https://docs.streamlit.io/library/api-reference/session-state)
    """
    story1_3_key = jira.create_story(epic_keys["epic1"], "Story 1.3: Streamlit Prototype", story1_3_desc, 
                                     components=["Frontend"], labels=["week-3"])
    
    # Create subtasks for Story 1.3
    jira.create_subtask(story1_3_key, "Initialize Streamlit project", 
                       "Create the basic Streamlit application structure.")
    
    jira.create_subtask(story1_3_key, "Create authentication flow", 
                       "Implement login, logout, and session management in Streamlit.")
    
    jira.create_subtask(story1_3_key, "Build basic UI components", 
                       "Create the main UI components for the application.")
    
    jira.create_subtask(story1_3_key, "Connect to FastAPI endpoints", 
                       "Integrate the Streamlit frontend with the FastAPI backend.")
    
    # Create Epic 2: Calendar & Email Integration
    epic2_desc = """
    This epic focuses on integrating calendar and email functionality into the AI personal assistant.
    It includes connecting to Google Calendar and Gmail/Outlook APIs and implementing management features.
    
    **Epic Dependencies:** Epic 1
    """
    epic_keys["epic2"] = jira.create_epic("Calendar & Email Integration", "Epic 2: Calendar & Email Integration", epic2_desc)
    
    # Create stories for Epic 2 (simplified for brevity)
    story2_1_desc = """
    ## Google Calendar Integration (Week 4)
    
    **Dependencies:** Story 1.2
    
    **Tasks:**
    - Set up Google API credentials
    - Implement OAuth flow
    - Create calendar event management functions
    - Build calendar sync system
    
    **Technologies:** Google Calendar API, FastAPI
    
    **Documentation:**
    - [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
    - [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
    
    **Expected Outcome:** System that can read and manage Google Calendar events
    
    **Learning Resources:**
    - [Google API Python Client](https://github.com/googleapis/google-api-python-client)
    - [OAuth 2.0 Flow Tutorial](https://developers.google.com/identity/protocols/oauth2/web-server#python)
    """
    story2_1_key = jira.create_story(epic_keys["epic2"], "Story 2.1: Google Calendar Integration", story2_1_desc, 
                                     components=["API Integration"], labels=["week-4"])
    
    # Create Epic 3: LLM & Agent Integration
    epic3_desc = """
    This epic covers the integration of large language models and the agent architecture.
    It includes setting up LangChain, creating basic and advanced agent systems, and implementing NLP features.
    
    **Epic Dependencies:** Epic 1
    """
    epic_keys["epic3"] = jira.create_epic("LLM & Agent Integration", "Epic 3: LLM & Agent Integration", epic3_desc)
    
    # Create stories for Epic 3 (add more details for these as needed)
    story3_1_desc = """
    ## LangChain Setup (Week 3)
    
    **Dependencies:** Story 1.2
    
    **Tasks:**
    - Set up LangChain environment
    - Configure LLM providers (OpenAI/Anthropic)
    - Create basic prompt templates
    - Implement conversation history storage
    
    **Technologies:** Python, LangChain, OpenAI API, Anthropic API
    
    **Documentation:**
    - [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
    - [LangChain with OpenAI](https://python.langchain.com/docs/integrations/llms/openai)
    - [LangChain with Anthropic](https://python.langchain.com/docs/integrations/llms/anthropic)
    
    **Expected Outcome:** Working LLM integration with basic conversation abilities
    
    **Learning Resources:**
    - [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)
    - [Working with LLMs](https://python.langchain.com/docs/modules/model_io/)
    - [Chat Models in LangChain](https://python.langchain.com/docs/modules/model_io/chat/)
    """
    story3_1_key = jira.create_story(epic_keys["epic3"], "Story 3.1: LangChain Setup", story3_1_desc, 
                                     components=["AI Integration"], labels=["week-3"])
    
    # Continue with all epics and stories in the project plan...
    # For brevity, I've included only a few examples, but you would continue adding all epics and stories
    
    # Create Epic 4: Job Application Support
    epic4_desc = """
    This epic focuses on developing job application support features.
    It includes experience management, Google Drive integration, job application agent system, and interview preparation.
    
    **Epic Dependencies:** Epic 1, Epic 3
    """
    epic_keys["epic4"] = jira.create_epic("Job Application Support", "Epic 4: Job Application Support", epic4_desc)
    
    # Create Epic 5: London Activity Planning
    epic5_desc = """
    This epic covers the development of London activity planning features.
    It includes event discovery, activity recommendation, and activity planning functionality.
    
    **Epic Dependencies:** Epic 1, Epic 3
    """
    epic_keys["epic5"] = jira.create_epic("London Activity Planning", "Epic 5: London Activity Planning", epic5_desc)
    
    # Create Epic 6: Production Interface
    epic6_desc = """
    This epic focuses on creating the production-ready interface.
    It includes React setup, agent visualization, user interface development, and mobile experience.
    
    **Epic Dependencies:** All previous Epics
    """
    epic_keys["epic6"] = jira.create_epic("Production Interface", "Epic 6: Production Interface", epic6_desc)
    
    # Create Epic 7: Deployment & Productization
    epic7_desc = """
    This epic covers the deployment and productization of the application.
    It includes CI/CD setup, cloud deployment, self-improvement mechanism, and user testing preparation.
    
    **Epic Dependencies:** All previous Epics
    """
    epic_keys["epic7"] = jira.create_epic("Deployment & Productization", "Epic 7: Deployment & Productization", epic7_desc)
    
    return "Successfully generated project tickets!"

if __name__ == "__main__":
    generate_project_tickets()