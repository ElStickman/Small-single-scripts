<?php
/**
 * https://leetcode.com/problems/roman-to-integer/
 * 13. Roman to Integer
 */

class Solution {

    /**
     * @param String $s
     * @return Integer
     */
    function romanToInt($s) {
        $total = 0;

        $s = str_replace('IV', 'IIII', $s);
        $s = str_replace('IX', 'VIIII', $s);
        $s = str_replace('XL', 'XXXX', $s);
        $s = str_replace('XC', 'LXXXX', $s);
        $s = str_replace('CD', 'CCCC', $s);
        $s = str_replace('CM', 'DCCCC', $s);
        $dic = array( 
                      'I' => 1,
                      'V' => 5,
                      'X' => 10,
                      'L' => 50,
                      'C' => 100,
                      'D' => 500,
                      'M' => 1000);
        foreach ($dic as $roman => $int) {
            $total += substr_count($s, $roman)*$int;
            $s = str_replace($roman, '', $s);
        }
        

        return $total;
    }
    
}