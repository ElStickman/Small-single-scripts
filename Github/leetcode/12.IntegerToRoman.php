<?php
/**
 * 12. Integer to Roman
 * https://leetcode.com/problems/integer-to-roman/
 * 
 */
class Solution {

    /**
     * @param Integer $num
     * @return String
     */
    function intToRoman($s) {
    $finalString = '';
    $dic = array( 
                'M' => 1000,
                'CM' => 900,
                'D' => 500,
                'CD' => 400,
                'C' => 100,
                'XC' => 90,
                'L' => 50,
                'XL' => 40,
                'X' => 10,
                'IX' => 9, 
                'V' => 5,
                'IV' => 4, 
                'I' => 1
    );
        foreach ($dic as $roman => $int) {
            //Vemos cuantas veces se puede dividir. (Si es 0, no  imprimirá nada)           
            if($total = floor($s / $int)) {
                //Restamos los multiplos de $int
                $s   = $s % $int;
                //Agregamos los números romanos equivalentes.
                $finalString .= str_repeat($roman, $total); 
            }
        }
    return $finalString;
    }
}
