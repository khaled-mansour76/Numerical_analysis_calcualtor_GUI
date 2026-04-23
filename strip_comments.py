import tokenize
import io
import os

def remove_comments_and_docstrings(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    try:
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
                
            if token_type == tokenize.COMMENT:
                pass
            elif token_type == tokenize.STRING:
                if prev_toktype not in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL, tokenize.ENCODING):
                    out += token_string
            else:
                out += token_string
                
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
    except tokenize.TokenError:
        pass
    
    # remove purely empty lines
    final_lines = []
    for line in out.splitlines():
        if not line.strip():
            continue
        final_lines.append(line)
        
    return "\n".join(final_lines) + "\n"

for f in os.listdir('.'):
    if f.endswith('.py') and f not in ('test_all.py', 'test_errors.py', 'strip_comments.py'):
        with open(f, 'r') as file:
            src = file.read()
        cleaned = remove_comments_and_docstrings(src)
        with open(f, 'w') as file:
            file.write(cleaned)
        print(f"Cleaned {f}")
