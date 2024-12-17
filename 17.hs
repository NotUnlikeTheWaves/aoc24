import Data.Bits

main = do
    -- -- Example instructions
    -- let regs = [729, 0, 0]
    -- let program = [0,1,5,4,3,0]
    -- -- Example instructions
    -- let regs = [10, 0, 0]
    -- let program = [5,0,5,1,5,4]
    -- Part 1 instructions
    let regs = [30553366, 0, 0]
    let program = [2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0]

    print "Hi"
    print $ execProgram regs program 0
    -- print $ execInstr regs program 0


--  Registers, program, instruction counter -> return output of the program
execProgram :: [Int] -> [Int] -> Int -> [Int]
execProgram registers program ic
    | ic > maxIC = [] -- nothing to add to the output
    | otherwise =   let (new_regs, new_ic, output) = execInstr registers program ic
                    in output ++ execProgram new_regs program new_ic
    where maxIC = (length program) - 2

-- Input: Registers, program, ic -> return output ([register state], new ic, [output])
execInstr :: [Int] -> [Int] -> Int -> ([Int], Int, [Int])
execInstr registers program ic
    | op == 0 = (setAR (advInstr rA combo)      , inc2                  , [])
    | op == 1 = (setBR (bxlInstr rB literal)    , inc2                  , [])
    | op == 2 = (setBR (bstInstr combo)         , inc2                  , [])
    | op == 3 = (registers                      , jnzInstr rA ic literal, [])
    | op == 4 = (setBR (bxcInstr rB rC)         , inc2                  , [])
    | op == 5 = (registers                      , inc2                  , [outInstr combo])
    | op == 6 = (setBR (advInstr rA combo)      , inc2                  , [])
    | op == 7 = (setCR (advInstr rA combo)      , inc2                  , [])
    where   rA = registers !! 0
            rB = registers !! 1
            rC = registers !! 2
            setAR = setA registers
            setBR = setB registers
            setCR = setC registers
            inc2 = incIC ic
            (op:literal:[]) = fetchIC program ic
            combo = decombo literal registers


-- Actual opcode execution

--0:adv
advInstr :: Int -> Int -> Int
advInstr a b = div a $ 2 ^ b

--1:bxl
bxlInstr :: Int -> Int -> Int
bxlInstr a b = xor a b

--2:bst
bstInstr :: Int -> Int
bstInstr a = mod a 8

--3:jnz     regA   ic     literal
jnzInstr :: Int -> Int -> Int -> Int
jnzInstr 0 ic _ = incIC ic
jnzInstr _ _ literal = literal

--4:bxc
bxcInstr :: Int -> Int -> Int
bxcInstr b c = xor b c

--5:out -- basically bstInstr?
outInstr :: Int -> Int
outInstr a = bstInstr a

--6:bdv == cdv


-- Go from combo op to regular op
-- 0-3 == literal value
-- 4-6 == register a/b/c
decombo :: Int -> [Int] -> Int
decombo op registers
    | op < 4    = op
    | op > 6    = 0 -- Fallback to make my life easier
    | otherwise = registers !! (op - 4)

--  Increase IC by 2
incIC :: Int -> Int
incIC ic = (ic + 2)

--  Retrieve the operator and operand in a list of size 2
fetchIC :: [Int] -> Int -> [Int]
fetchIC program ic = take 2 (drop ic program)

-- Setting the registers
setA :: [Int] -> Int -> [Int]
setA (_:b:c:[]) a = [a, b, c]

setB :: [Int] -> Int -> [Int]
setB (a:_:c:[]) b = [a, b, c]

setC :: [Int] -> Int -> [Int]
setC (a:b:_:[]) c = [a, b, c]
