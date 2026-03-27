from langgraph.graph import StateGraph, START, END

from swarm.state import AgentState
from swarm.agents import scout_node, extractor_node, analyst_node

def build_intelligence_swarm():
    """Builds and compiles the Multi-Agent Swarm graph."""
    
    # Initialize the state machine graph
    workflow = StateGraph(AgentState)
    
    # Add our autonomous agents as nodes
    workflow.add_node("scout", scout_node)
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("analyst", analyst_node)
    
    # Define the execution flow (Edges)
    workflow.add_edge(START, "scout")
    workflow.add_edge("scout", "extractor")
    workflow.add_edge("extractor", "analyst")
    workflow.add_edge("analyst", END)
    
    # Compile the graph into an executable application
    return workflow.compile()

# Global singleton instance of the swarm
swarm_app = build_intelligence_swarm()

if __name__ == "__main__":
    print("🚀 AACIE V6 Swarm Initialized.")
    # Test run
    initial_state = {
        "topic": "الذكاء الاصطناعي في الشرق الأوسط",
        "target_count": 2,
        "raw_urls": [],
        "scraped_content": [],
        "final_reports": [],
        "errors": []
    }
    
    final_state = swarm_app.invoke(initial_state)
    
    print("\n--- FINAL INTELLIGENCE REPORTS ---")
    for r in final_state.get("final_reports", []):
        print(f"\n📰 {r['title']}")
        print(f"🔗 {r['url']}")
        print(f"🧠 Analysis: {r['analysis']}")
