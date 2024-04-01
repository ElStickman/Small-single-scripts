/***
*Siguiendo la misma lógica del .py
* en caso de PHP existe una función para dar vuelta un str.
* Al no necesitar pasar 2 veces esto a texto, y por que PHP toma el número como texto, el código se simplifica.
*/
class Solution {

    /**
     * @param Integer $x
     * @return Boolean
     */
    function isPalindrome($x) {
        return $t == strrev($x);
    }
}
