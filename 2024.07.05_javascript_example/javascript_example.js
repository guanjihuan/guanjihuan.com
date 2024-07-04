// 输出到控制台
console.log("Hello, World!"); 


// 变量声明
var name = "Alice";  // 不推荐，因为它有作用域问题
let age = 25;  // 推荐
const pi = 3.14159; // 用于常量


// 数据类型
let number = 42; // 数字
let text = "Hello"; // 字符串
let isTrue = true; // 布尔值
let items = [1, 2, 3]; // 数组
let person = { name: "John", age: 30 }; // 对象


// 基本运算
let sum = 10 + 5; // 加法
let difference = 10 - 5; // 减法
let product = 10 * 5; // 乘法
let quotient = 10 / 5; // 除法
let a = 0.1;
let b = 0.2;
let c = a + b; // 浮点加法


// 条件语句
let abc = 10;
if (abc > 0) {
    console.log("abc is positive.");
} else if (abc < 0) {
    console.log("abc is negative.");
} else {
    console.log("abc is zero.");
}
console.log('');


// for 循环
for (let i = 0; i < 5; i++) {
    console.log(i);
}
console.log('')


// while 循环
let i = 0;
while (i < 5) {
console.log(i);
i++;
}
console.log('');


// 函数定义和调用
function greet(name) {
    return "Hello, " + name;
}
console.log(greet("Guan"));