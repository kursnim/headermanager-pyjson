import json
import re

def define_replacer(text):
    def is_cstyle_num(text):
        m = re.match(r'\d', text)
        if m:
            return True
        else:
            return False

    def replacer(match):
        def_key = match.group(2)
        if def_key in option_dict:
            def_val = option_dict[def_key]
            if is_cstyle_num(def_val):
                print(match.group(4))
                def_val = '({0})'.format(def_val)
            elif match.group(4).startswith('"'):
                def_val = '"{0}"'.format(def_val)
                
            return match.group(1) + match.group(2) + match.group(3) + def_val
        else:
            return match.group(0)
    return re.sub(r'(#\s*define\s+)(\w+)(\s+)([-+]?\d*\.\d+F?|\w+|\".+\")', replacer, text)

def parentheses_remover(text):
    def replacer(match):
        return match.group(1)
    text = re.sub(r'\((.*)\)', replacer, text)    
    if '(' in text:
        return parentheses_remover(text)
    else:
        return text

if __name__=='__main__':
    with open('option.json') as f:
        text = f.read()
        option_dict = json.loads(text)

    with open('option.h', 'r') as f:
        text = f.read()
    
    text = parentheses_remover(text)    
    text = define_replacer(text)

    print(text)

    # with open('option.h', 'w') as f:
    #     f.write(text)
