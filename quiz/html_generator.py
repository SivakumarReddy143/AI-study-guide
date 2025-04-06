from quiz.template import _format_quiz_with_reveal

def generate_html(quiz):
    """
    Generate the HTML content for the quiz using the custom template.
    
    Args:
        quiz (list): List of dictionaries with question, options, correct answer, and explanation.
    
    Returns:
        str: Rendered HTML string.
    """
    return _format_quiz_with_reveal(quiz)
