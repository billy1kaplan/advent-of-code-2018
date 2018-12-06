import Data.List

frequencies :: (Eq a, Ord a) => [a] -> [Int]
frequencies = map length . group . sort

numberOfFreq :: Int -> [[Int]] -> Int
numberOfFreq freq = length . filter (elem freq)

computeCheckSum :: [[Char]] -> Int
computeCheckSum input = numberOfFreq 2 counts * numberOfFreq 3 counts
    where counts = map frequencies input

main = do
    file <- lines <$> readFile "input.txt"

    -- Part 1:
    print $ computeCheckSum file
    -- Part 2:
