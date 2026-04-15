import subprocess
import sys
from rag import retrieve

# ── Tool 1: Search Python docs using RAG ─────────────
def search_python_docs(question: str) -> str:
    """
    Search the Python knowledge base using RAG retrieval.
    Use this when the user asks about Python concepts,
    syntax, functions, errors, OOP, or best practices.
    Always use this tool first before answering any
    Python related question.
    """
    context = retrieve(question)

    if context:
        return f"Found in knowledge base:\n\n{context}"
    else:
        return (
            f"No relevant documents found for: '{question}'. "
            f"Answer from your general Python knowledge."
        )


# ── Tool 2: Run Python code ───────────────────────────
def run_python_code(code: str) -> str:
    """
    Execute Python code and return the output or error.
    Use this when the user wants to test code, debug,
    verify output, or when they share code and ask
    if it works correctly.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            return (
                f"Code ran successfully!\nOutput: {output}"
                if output else
                "Code ran successfully! No output produced."
            )
        else:
            return f"Error:\n{result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Code timed out — possible infinite loop."
    except Exception as e:
        return f"Could not run code: {str(e)}"


# ── Tool 3: Explain Python error ─────────────────────
def explain_error(error_message: str) -> str:
    """
    Explain what a Python error means and how to fix it.
    Use this when the user has an error message or when
    running code produces an error output.
    """
    explanations = {
        "NameError":        "Variable used before being defined. Check spelling or define it first.",
        "TypeError":        "Wrong data type. Example: adding int and string without converting.",
        "ValueError":       "Right type but wrong value. Example: int('hello') fails.",
        "IndexError":       "List index out of range. List has fewer items than expected.",
        "KeyError":         "Dictionary key does not exist. Use .get() for safe access.",
        "IndentationError": "Wrong indentation. Python uses spaces to define code blocks.",
        "SyntaxError":      "Invalid Python syntax. Check for missing colons, brackets, or quotes.",
        "ZeroDivisionError":"Division by zero. Add check: if b != 0: result = a / b",
        "AttributeError":   "Object does not have that method. Check the object type.",
        "ImportError":      "Module not found. Install with: pip install <module_name>",
    }

    for error_type, explanation in explanations.items():
        if error_type.lower() in error_message.lower():
            return f"{error_type}: {explanation}"

    return (
        f"Error: {error_message}\n"
        f"Share the full traceback for a more specific explanation."
    )


# ── Tool 4: Generate practice exercise ───────────────
def generate_exercise(topic: str, difficulty: str = "beginner") -> str:
    """
    Generate a Python practice exercise for a given topic.
    Use this when the user wants to practice, asks for an
    exercise, or wants to test their understanding of a topic.
    """
    exercises = {
        "list": {
            "beginner":     "Create a list of 5 fruits. Print the first and last item. Add 'grape' to the end.",
            "intermediate": "Write a function that takes a list of numbers and returns only even ones using list comprehension.",
        },
        "dictionary": {
            "beginner":     "Create a dictionary with your name, age, and city. Print each value using a for loop.",
            "intermediate": "Write a function that counts word frequency in a sentence and returns a dictionary.",
        },
        "function": {
            "beginner":     "Write a function called greet that takes a name and returns 'Hello, <name>!'",
            "intermediate": "Write a function using *args that returns the sum of all numbers passed to it.",
        },
        "loop": {
            "beginner":     "Print numbers 1 to 10 using a for loop. Then print only even numbers.",
            "intermediate": "Write a while loop that keeps asking for input until user types 'quit'.",
        },
        "class": {
            "beginner":     "Create a class called Dog with name and age attributes. Add a bark() method.",
            "intermediate": "Create a class called BankAccount with deposit, withdraw, and balance methods.",
        },
        "error": {
            "beginner":     "Write a program that asks for a number and handles ValueError if user types letters.",
            "intermediate": "Write a function that opens a file and handles both FileNotFoundError and PermissionError.",
        },
        "string": {
            "beginner":     "Take a sentence as input. Print it in uppercase, count vowels, and reverse it.",
            "intermediate": "Write a function that checks if a string is a palindrome ignoring spaces and case.",
        },
    }

    topic_lower = topic.lower()
    for key, levels in exercises.items():
        if key in topic_lower:
            level = difficulty.lower()
            exercise = levels.get(level) or levels.get("beginner")
            return f"Exercise ({difficulty}): {exercise}"

    return f"Exercise: Write a Python program demonstrating {topic}. Test it with at least 3 examples."