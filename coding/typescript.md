---
title: TypeScript 入门
description: TypeScript 基础类型系统和高级特性
---

# TypeScript 入门

TypeScript 是 JavaScript 的超集，添加了静态类型系统。

## 基础类型

```typescript
// 原始类型
let isDone: boolean = false
let decimal: number = 6
let color: string = 'blue'

// 数组
let list: number[] = [1, 2, 3]
let list2: Array<number> = [1, 2, 3]

// 元组
let tuple: [string, number] = ['hello', 10]

// 枚举
enum Color { Red, Green, Blue }
let c: Color = Color.Green

// any - 任意类型（谨慎使用）
let notSure: any = 4

// unknown - 安全版本的 any
let unknownValue: unknown
if (typeof unknownValue === 'string') {
  console.log(unknownValue.toUpperCase())
}

// void - 无返回值
function warnUser(): void {
  console.log('Warning')
}

// never - 永不返回的值
function error(message: string): never {
  throw new Error(message)
}
```

## 接口

```typescript
interface User {
  readonly id: number
  name: string
  email?: string  // 可选属性
  [key: string]: any  // 索引签名
}

const user: User = {
  id: 1,
  name: 'John'
}
```

## 泛型

```typescript
// 泛型函数
function identity<T>(arg: T): T {
  return arg
}

// 泛型接口
interface Box<T> {
  value: T
}

const stringBox: Box<string> = { value: 'hello' }
const numberBox: Box<number> = { value: 42 }

// 泛型约束
function printLength<T extends { length: number }>(arg: T): void {
  console.log(arg.length)
}
```

## 类型推断

```typescript
// TypeScript 会自动推断类型
let x = 3  // 推断为 number
x = 'hello'  // 错误：类型不匹配

// 最佳通用类型
let items = []  // 推断为 any[]
let items2: string[] = []  // 明确类型
```

## 实用工具类型

```typescript
type PartialUser = Partial<User>  // 所有属性可选
type RequiredUser = Required<User>  // 所有属性必填
type ReadonlyUser = Readonly<User>  // 所有属性只读
type UserKeys = keyof User  // 键的联合类型
type UserName = User['name']  // 索引访问类型
```

> 提示：使用 `tsc --noEmit` 可以快速检查类型错误。
