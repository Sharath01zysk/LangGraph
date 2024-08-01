from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from functions import handle_question,handle_eval,handle_response,handle_result, check_conv_length


class GraphState(TypedDict):
    history: Optional[str] = None
    result: Optional[str] = None
    total_questions: Optional[int] = None
    interviewer: Optional[str] = None
    candidate: Optional[str] = None
    current_question: Optional[str] = None
    current_answer: Optional[str] = None

workflow = StateGraph(GraphState)

workflow.add_node("handle_question",handle_question)
workflow.add_node("handle_evaluation",handle_eval)
workflow.add_node("handle_response",handle_response)
workflow.add_node("handle_result",handle_result)

workflow.add_conditional_edges(
    'handle_evaluation',
    check_conv_length,
    {
        'handle_question':'handle_question',
        'handle_result':'handle_result'
    }
)

workflow.set_entry_point('handle_question')
workflow.add_edge('handle_question','handle_response')
workflow.add_edge('handle_response','handle_evaluation')
workflow.add_edge('handle_evaluation',END)

app = workflow.compile()

conversation = app.invoke({'total_questions':0,'candidate':'junior web dev','interviewer':'senior web developer','history':'nothing',})

