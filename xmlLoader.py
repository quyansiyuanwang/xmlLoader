import json
import os


def json_io(filename: str, 
            mode: str = 'r', 
            info: dict = None,
            indent: int = 2) -> bool | dict:
    mode = mode.lower()
    if mode not in 'ra':
        raise IOError(f'unknown mode: {mode}')
    
    with open(filename, mode) as f:
        user_infos = json.load(f)
        match mode:
            case 'r':
                return user_infos
            case 'a':
                if info is None:
                    raise ValueError('No info!')
                user_infos.update(info)
                json.dump(user_infos, f, indent=indent)
                return True
    return False

def to_list(dic):
    return [v for k, v in dic.items() if v != '=']
        
def indents_string(string: str, indents: str):
    return string.replace('\n', '\n' + indents)

def tree(tree_stru, indents: int = 2):
    # if indents > 16: return  # 临时的限制，不然他不崩溃我要崩溃
    match tree_stru:
        case {'name':name, 'equals': '=', 'value': value}:
            if isinstance(value, dict):
                tree(value, indents + 2)
            else:
                value = str(value)
                if '\n' in value:
                    value = indents_string(value, '>' * (indents + len(name) + 6))
                print('-' * indents + f'{name}: {value}')
        case dict():
            if 'equals' in tree_stru:
                # print(tree_stru.keys())
                tree(to_list(tree_stru), indents)

            else:
                for k, v in tree_stru.items():
                    print('-' * indents + k)
                    tree(v, indents + 2)

        case list():
            for elem in tree_stru:
                    tree(elem, indents + 2)
        
        case _:    
            print('-' * indents + repr(tree_stru))




#print(__file__)
#print('the path:', os.path.abspath(__file__))


json_path = '/'.join(__file__.split('/')[:-1])
infos = json_io(json_path + '/amiya.json', 'r')

tree(infos)