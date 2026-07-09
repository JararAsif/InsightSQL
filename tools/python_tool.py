import io
import contextlib
import traceback

def execute_python(code: str) -> str:
    """
    Executes a string of Python code and returns any standard output, 
    or the error traceback if it fails.
    """
    output_buffer = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            with contextlib.redirect_stderr(output_buffer):
                exec(code, globals())
                
        return output_buffer.getvalue()
    except Exception as e:
        return f"Python Execution Error: {str(e)}\n{traceback.format_exc()}"
