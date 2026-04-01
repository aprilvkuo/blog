// GET /api/analyze/:taskId - 查询任务状态
// 返回：{ "task_id": "xxx", "status": "completed", "result": {...} }

import type { PagesFunction } from '@cloudflare/workers-types'

interface Env {
  TASKS_KV: KVNamespace
}

interface Task {
  id: string
  symbol: string
  stock_code?: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: number
  updated_at: number
  result?: {
    report_path?: string
    error?: string
  }
}

export const onRequest: PagesFunction<Env> = async ({ request, env, params }) => {
  // CORS 预检请求处理
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '86400',
      },
    })
  }

  if (request.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  const taskId = params.taskId

  if (!taskId) {
    return new Response(JSON.stringify({ error: 'Missing task_id' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  try {
    // 从 KV 获取任务
    const taskData = await env.TASKS_KV.get(`task:${taskId}`)

    if (!taskData) {
      return new Response(JSON.stringify({ error: 'Task not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' },
      })
    }

    const task: Task = JSON.parse(taskData)

    // 检查是否有结果文件
    let result = task.result
    if (task.status === 'completed' && task.result?.report_path) {
      // 可以尝试读取结果内容（如果存储在 KV 中）
      const resultData = await env.TASKS_KV.get(`result:${taskId}`)
      if (resultData) {
        result = JSON.parse(resultData)
      }
    }

    return new Response(JSON.stringify({
      task_id: task.id,
      symbol: task.symbol,
      stock_code: task.stock_code,
      status: task.status,
      created_at: task.created_at,
      updated_at: task.updated_at,
      result: result,
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    })
  } catch (error) {
    console.error('Error fetching task:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}
