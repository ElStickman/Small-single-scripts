/**
*
*
* Runtime 11ms Beats 94.47%of users with PHP
* Memory 19.76MB Beats 99.39% of users with PHP
**/
class Solution {

    /**
     * @param Integer[] $nums
     * @param Integer $target
     * @return Integer[]
     */
    function twoSum($nums, $target) {
        $hash = array();
        foreach ($nums as $key => $num) {
            $search = $target - $num;
            if(isset($hash[$search]))
                return [$hash[$search], $key];
            $hash[$num] = $key;
        }
    }
}
