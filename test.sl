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
    return fib(a - 1) + fib(a - 2);
}
def factorial(a) {
    if (a == 0) {
        return 1;
    }
    if (a == 1) {
        return 1;
    }
    return a * factorial(a - 1);
}
let arr = [1, 2, 3, 4, 5]
print(arr[2])
print(fib(5))
print(factorial(5))
