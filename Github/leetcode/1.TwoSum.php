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
