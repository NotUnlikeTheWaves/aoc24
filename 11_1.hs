main = do
    let init = [112, 1110, 163902, 0, 7656027, 83039, 9, 74]
    let f x = concat $ map changeStone x
    let result = iterate f init
    print (length (result !! 25))

changeStone :: Int -> [Int]
changeStone 0 = [1]
changeStone n =
    let nod = numberOfDigits n
    in case (even nod) of
        True -> [div n (10 ^ (div nod 2)), mod n (10 ^ (div nod 2))]
        False -> [n * 2024]

numberOfDigits :: Int -> Int
numberOfDigits 0 = 0
numberOfDigits n = 1 + numberOfDigits (div n 10)
