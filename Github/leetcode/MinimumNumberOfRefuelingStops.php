<?php
/**
 * 871. Minimum Number of Refueling Stops
 * https://leetcode.com/problems/minimum-number-of-refueling-stops/
 * 
 * A car travels from a starting position to a destination which is target miles east of the starting position.
 *
 * There are gas stations along the way. The gas stations are represented as an array stations where stations[i] = [positioni, fueli] indicates that the ith gas station is positioni miles east of the starting position and has fueli liters of gas.
 *
 * The car starts with an infinite tank of gas, which initially has startFuel liters of fuel in it. It uses one liter of gas per one mile that it drives. When the car reaches a gas station, it may stop and refuel, transferring all the gas from the station into the car.
 *
 * Return the minimum number of refueling stops the car must make in order to reach its destination. If it cannot reach the destination, return -1.
 *
 * Note that if the car reaches a gas station with 0 fuel left, the car can still refuel there. If the car reaches the destination with 0 fuel left, it is still considered to have arrived.
 */
class Solution {

    /**
    * @param Integer $target
    * @param Integer $startFuel
    * @param Integer[][] $stations
    * @return Integer
    * We asume stations are from closest to furthest
    */
    function minRefuelStops($target, $fuel, $stations) {
        //We keep driving until we arrive.
        $totalStations = 0;
        $distanceFromStart = 0;
        $missedStationsFuel = [];
        $stations[] = [$target, 0];
        //If no stations on the way.
        if(count($stations) == 0 && $fuel < $target)
            return -1;
        //We can get there with no statiosn.
        if($target <= $fuel)
            return 0;
        //We go through every station
        foreach ($stations as $station) {
            //Distance from last station.
                $distance = $station[0] - $distanceFromStart;
                //We substract the distance we traveled.
                $fuel -= ($distance);
                $distanceFromStart += $distance;
                //If we got no fuel and can't refill GG
                while($fuel < 0) {
                    //If we can't refill anymore, return -1.
                    if(count($missedStationsFuel) == 0) {
                        return -1;
                    }
                    //We should always refill the greatest ammount.
                    $fuel += max($missedStationsFuel);
                    //We add 1 station to the count.
                    $totalStations+=1;
                    //We unset the fuel we just refilled
                    unset($missedStationsFuel[array_search (max($missedStationsFuel), $missedStationsFuel)]);
                }
                //We can only refill if we reached the station.
                $missedStationsFuel[] = $station[1];
            }
        //We arrived
        return $totalStations;
    }
}