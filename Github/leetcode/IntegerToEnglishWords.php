<?php
/**
 * This solution is bugged on leetcode as recursion is not working properly on PHP for high value numbers.
 * 
 * 273. Integer to English Words
 * https://leetcode.com/problems/integer-to-english-words/
 */

class Solution {

/**
 * @param Integer $num
 * @return String
 */
function numberToWords($s) {
    $finalString = '';
    $dic = array(
        "One" => 1,
        "Two" => 2,
        "Three" => 3,
        "Four" => 4,
        "Five" => 5,
        "Six" => 6,
        "Seven" => 7,
        "Eight" => 8,
        "Nine" => 9,
        "Ten" => 10,
        "Eleven" => 11,
        "Twelve" => 12,
        "Thirteen" => 13,
        "Fourteen" => 14,
        "Fifteen" => 15,
        "Sixteen" => 16,
        "Seventeen" => 17,
        "Eighteen" => 18,
        "Nineteen" => 19,
        "Twenty" => 20,
        "Thirty" => 30,
        "Forty" => 40,
        "Fifty" => 50,
        "Sixty" => 60,
        "Seventy" => 70,
        "Eighty" => 80,
        "Ninety" => 90,
        "Hundred" => 100,
        "Thousand" => 1000,
        "Million" => 1000000,
        "Billion" => 1000000000,
        "Trillion" => 1000000000000
    );
    $dic = array_reverse($dic, true);
    if($s == 0)
        return "Zero";
    foreach ($dic as $name => $int) {
        if($total = floor($s / $int)) {
            $s = $s % $int;
            if($int > 99) { 
                $key = array_search ($total, $dic);
                if($key == '') {
                    $key = numberToWords($total);
                }
                $key .= ' ';
            } else {
                $key = '';
            }
            if($int > 10)
                $name .= ' ';
            $finalString .= $key.$name;
        }
    }
    return $finalString;
}
}