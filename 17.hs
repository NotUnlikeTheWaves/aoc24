import Data.Bits

main = do
    -- Example instructions
    let regs = [729, 0, 0]
    let program = [0,1,5,4,3,0]
    print "Hi"


--  Registers, program, instruction counter -> return output of the program
execProgram :: [Int] -> [Int] -> Int -> [Int]
execProgram registers program ic
    | instr == [] = [] -- nothing to add to the output
    | otherwise = 
    where instr = fetchIC program ic 

-- Input: Registers, program, ic -> return output ([register state], new ic, [output])
execInstr :: [Int] -> [Int] -> Int -> ([Int], Int, [Int])
execInstr registers program ic
    | op == 0 = (setA (advInstr rA $ decombo rhs), incIC)
    where   rA = registers !! 0
            rB = registers !! 1
            rC = registers !! 2
            (op, rhs) = fetchIC program ic


-- Actual opcode execution

--0:adv
advInstr :: Int -> Int -> Int
adv a b = div a $ 2 ^ 5

--1:bxl
bxlInstr :: Int -> Int -> Int
bxlInstr a b = xor a b

--2:bst
bstInstr :: Int -> Int
bstInstr a = mod a 8

-- --3:jnz
-- jnzInstr :: 


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
setA :: Int -> [Int] -> [Int]
setA a (_, b, c) = [a, b, c]

setB :: Int -> [Int] -> [Int]
setB b (a, _, c) = [a, b, c]

setC :: Int -> [Int] -> [Int]
setC c (a, b, _) = [a, b, c]
