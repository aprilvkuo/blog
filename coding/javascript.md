---
title: JavaScript 核心概念
description: JavaScript 语言的核心特性和最佳实践
---

# JavaScript 核心概念

JavaScript 是一门多范式、动态类型的脚本语言。

## 变量声明

```javascript
// var - 函数作用域（不推荐）
var name = 'John'

// let - 块级作用域，可重新赋值
let count = 0

// const - 块级作用域，不可重新赋值
const PI = 3.14159
```

## 箭头函数

```javascript
// 传统函数
function add(a, b) {
  return a + b
}

// 箭头函数
const add = (a, b) => a + b

// 多行箭头函数
const multiply = (a, b) => {
  const result = a * b
  return result
}
```

## 异步编程

### Promise

```javascript
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error))
```

### Async/Await

```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/data')
    const data = await response.json()
    return data
  } catch (error) {
    console.error(error)
  }
}
```

## 解构赋值

```javascript
// 数组解构
const [first, second, ...rest] = [1, 2, 3, 4, 5]

// 对象解构
const { name, age, city = 'Unknown' } = user

// 嵌套解构
const { user: { name } } = response
```

## 模块系统

```javascript
// ES Modules - 导出
export const name = 'value'
export default function fn() {}

// ES Modules - 导入
import fn, { name } from './module.js'
```
