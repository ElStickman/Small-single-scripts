class Solution:
    def numberToWords(self, s: int) -> str:
        finalString = ''
        dic = {
            "Trillion" : 1000000000000,
            "Billion" : 1000000000,
            "Million" : 1000000,
            "Thousand" : 1000,
            "Hundred" : 100,
            "Ninety" : 90,
            "Eighty" : 80,
            "Seventy" : 70,
            "Sixty" : 60,
            "Fifty" : 50,
            "Forty" : 40,
            "Thirty" : 30,
            "Twenty" : 20,
            "Nineteen" : 19,
            "Eighteen" : 18,
            "Seventeen" : 17,
            "Sixteen" : 16,
            "Fifteen" : 15,
            "Fourteen" : 14,
            "Thirteen" : 13,
            "Twelve" : 12,
            "Eleven" : 11,
            "Ten" : 10,
            "Nine" : 9,
            "Eight" : 8,
            "Seven" : 7,
            "Six" : 6,
            "Five" : 5,
            "Four" : 4,
            "Three" : 3,
            "Two" : 2,
            "One" : 1
                     }
        
        if(s == 0):
            return "Zero"
        key_list = list(dic.keys())
        for name, number in dic.items(): 
            if(total := floor(s / number)):
                s = s % number
                if(number > 99) :
                    key = ''
                    try:
                        key = key_list.index(total)
                    except:
                        key = ''
                    if(key == ''):
                        key = Solution().numberToWords(total)
                    
                    key += ' '
                else :
                    key = ''
                
                if(number > 10):
                    name += ' '
                finalString += key+name;
            
        finalString = finalString.replace("  ", " ").strip()
        return finalString;
    