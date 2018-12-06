import qualified Data.Set as Set

readLineAsInt :: [Char] -> Int
readLineAsInt ('+': rest) = read rest
readLineAsInt line = read line

cyclicalFreqSum :: [Int] -> [Int]
cyclicalFreqSum original = scanl (+) 0 (cycle original)

findFirstDuplicate :: Ord a => [a] -> Set.Set a -> Either a (Set.Set a)
findFirstDuplicate [] set = Right set
findFirstDuplicate (first:rest) set
    | Set.member first set = Left first
    | otherwise = findFirstDuplicate rest (Set.insert first set)

main = do
    file <- lines <$> readFile "input.txt"

    -- Part 1:
    print $ sum $ fmap readLineAsInt file

    -- Part 2:
    print $ findFirstDuplicate (cyclicalFreqSum $ map readLineAsInt file) Set.empty
