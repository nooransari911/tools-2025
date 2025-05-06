def caesar_cipher (a: str, k: int):
    if not a.isalpha ():
        return chr (0)
    base_position: int = 0
    
    if a.islower ():
        base_position = ord ("a")
    else:
        base_position = ord ("A")


    char_position: int = ord (a) - base_position
    shifted_position: int = ((char_position + k) % 26) + base_position 
    
    return chr (shifted_position)
    


s = input ("enter string: ")
k = int (input ("enter key: "))

shifted_char_list: list = [caesar_cipher (a, k) for a in s]

encstr = "".join (shifted_char_list)

print (encstr)





