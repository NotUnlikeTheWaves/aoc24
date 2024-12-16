use std::{cell::RefCell, fs::File, io::Read, path::Path, rc::Rc};

struct Node {
    outgoing: Vec<Rc<RefCell<Node>>>,
    value: i8,
}

fn main() {
    use std::time::Instant;
    let now = Instant::now();
    let path = Path::new("10.txt");
    let mut file = match File::open(path) {
        Ok(file) => file,
        Err(err) => panic!("Couldn't open {}: {}", path.display(), err),
    };

    let mut buffer = String::new();
    let _ = file.read_to_string(&mut buffer);

    // let array: Vec<&str> = buffer.split('\n').map(|a: char| a).collect();
    let raw_array: Vec<&str> = buffer.split('\n').collect();
    let mut array: Vec<Vec<Rc<RefCell<Node>>>> = raw_array
        .iter()
        .map(|line| {
            line.chars()
                .map(|c| {
                    Rc::new(RefCell::new(Node {
                        outgoing: vec![],
                        value: i8::try_from(c.to_digit(10).unwrap()).unwrap(),
                    }))
                })
                .collect()
        })
        .collect();

    // Due to split shenanigans including an empty final element
    array.pop();

    let height = array.len();
    let width = array[0].len();

    let mut trail_starts: Vec<Rc<RefCell<Node>>> = vec![];

    for y in 0..height {
        for x in 0..width {
            let mut this = array[y][x].borrow_mut();
            let my_value = this.value;
            // Add neighbours if they are exactly one more than us, i.e. visitable
            if x != 0 && ((*array[y][x - 1].borrow()).value - my_value) == 1 {
                this.outgoing.push(Rc::clone(&array[y][x - 1]));
            }
            if y != 0 && ((*array[y - 1][x].borrow()).value - my_value) == 1 {
                this.outgoing.push(Rc::clone(&array[y - 1][x]));
            }
            if (x + 1) != width && ((*array[y][x + 1].borrow()).value - my_value) == 1 {
                this.outgoing.push(Rc::clone(&array[y][x + 1]));
            }
            if (y + 1) != height && ((*array[y + 1][x].borrow()).value - my_value) == 1 {
                this.outgoing.push(Rc::clone(&array[y + 1][x]));
            }

            // If we are at a start of a trailhead, add
            if my_value == 0 {
                trail_starts.push(Rc::clone(&array[y][x]));
            }
        }
    }

    let (unique_trail_options, total_trail_options) =
        trail_starts.iter().fold((0, 0), |(unique, total), start| {
            let mut unique_visited_ends: Vec<Rc<RefCell<Node>>> = vec![];
            let count = find_trail_end(start, &mut unique_visited_ends);
            if count > 0 {
                return (unique + unique_visited_ends.len(), total + count);
            }
            return (unique, total);
        });

    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);
    println!("If you see this, the program terminates. This is good.");
    println!("Unique 0-9 trails: {}", unique_trail_options);
    println!("Total 0-9 trails: {}", total_trail_options);
}

fn find_trail_end(node: &Rc<RefCell<Node>>, ends: &mut Vec<Rc<RefCell<Node>>>) -> u32 {
    let n = node.borrow();
    if n.value == 9 {
        if !(ends.iter().any(|x| Rc::ptr_eq(&x, node))) {
            ends.push(Rc::clone(node));
        }
        return 1;
    }

    return n
        .outgoing
        .iter()
        .map(|neighbour| find_trail_end(neighbour, ends))
        .sum();
}
