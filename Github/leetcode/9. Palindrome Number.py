# [:] Crea una copia de la lista.
# [start:end:step], si se fija un "end" este no es considerado al recorrer todo. step  es el paso en el que lo recorre.
# [::-1] recorre toda la lista a un paso de "-1", es decir, en reversa. Por lo que copia la lista al revés.
# runtime y memoria son random en leetcode, pero es la mejor versión que conozco. 
# https://leetcode.com/problems/palindrome-number/submissions/1220572500/

class Solution:
    def isPalindrome(self, x: int) -> bool:
        ret = str(x)
        return ret[::-1] == ret
