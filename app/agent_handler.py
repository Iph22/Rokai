# app/agent_handler.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from app.agents import get_agent, AGENTS

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_agent_response(agent_id: str, messages: list, context: dict = None):
    """
    Generate a response from a specific Eye agent
    
    Args:
        agent_id: ID of the agent (eye-1, eye-1.3, eye-2, eye-3)
        messages: Conversation history
        context: Optional additional context (memories, metadata)
    
    Returns:
        AI response string
    """
    
    # Get agent configuration
    agent = get_agent(agent_id)
    if not agent:
        return f"Error: Agent '{agent_id}' not found"
    
    # Build system prompt with context if provided
    system_prompt = agent["system_prompt"]
    
    if context and context.get("memories"):
        memory_context = "\n".join([
            f"- {mem['content']}" for mem in context["memories"]
        ])
        system_prompt += f"\n\n[Relevant context from Rokai memory:\n{memory_context}]"
    
    try:
        # Call Claude with agent-specific configuration
        response = client.messages.create(
            model=agent["model"],
            max_tokens=agent["max_tokens"],
            temperature=agent["temperature"],
            system=system_prompt,
            messages=messages
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"⚠️ {agent['name']} Error: {str(e)}"


def route_to_agent(query: str, context: dict = None) -> str:
    """
    Intelligently route query to appropriate agent based on content
    
    Args:
        query: User's question/request
        context: Optional context
    
    Returns:
        Agent ID to use
    """
    query_lower = query.lower()
    
    # Code/technical keywords → Eye-1.3
    code_keywords = ['code', 'function', 'api', 'debug', 'error', 'database', 
                     'implement', 'build', 'python', 'javascript', 'sql']
    if any(keyword in query_lower for keyword in code_keywords):
        return "eye-1.3"
    
    # Analytics/performance keywords → Eye-2
    analytics_keywords = ['analyze', 'performance', 'metrics', 'monitor', 
                          'optimize', 'statistics', 'data', 'usage']
    if any(keyword in query_lower for keyword in analytics_keywords):
        return "eye-2"
    
    # Design/creative keywords → Eye-3
    design_keywords = ['design', 'ui', 'ux', 'visual', 'layout', 'color', 
                       'brand', 'aesthetic', 'interface', 'component']
    if any(keyword in query_lower for keyword in design_keywords):
        return "eye-3"
    
    # Default → Eye-1
    return "eye-1"