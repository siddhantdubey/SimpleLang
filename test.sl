let x = 15;
print(x);
while (x < 100) {
    print(x);
    let x = x * 2;
}
def fib(a) {
    if (a == 0) {
        return 0;
    }
    if (a == 1) {
        return 1;
    }
    let secondlast = 0;
    let out = 1;
    for i = 1 to a {
        let temp = out;
        let out = temp + secondlast;
        let secondlast = temp;
    }
    return out;
}
print("Final x is:");
print(x);
print(fib(6));