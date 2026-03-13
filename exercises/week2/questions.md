# Week 2 题目清单（模块化 + 异常处理 + 文件处理）

> 命名建议：`w2_eXX_name.py`。  
> 完成策略：先跑通主流程，再优化异常处理与结构。

---

## Day 1：模块化

### W2-E01 单文件拆分

- 把一个脚本拆成 `main.py / services.py / utils.py`

### W2-E02 函数职责拆分

- 实现：
  - `load_users(path)`
  - `build_user_index(users)`
  - `render_summary(users)`

### W2-E03 入口规范

- 用 `main()` + `if __name__ == "__main__":`

---

## Day 2：异常处理

### W2-E04 安全数字转换

- 实现 `safe_int(value, default=0)`、`safe_float(value, default=0.0)`

### W2-E05 文件异常处理

- 读取文件时处理 `FileNotFoundError`、`PermissionError`

### W2-E06 业务异常

- 自定义异常 `InvalidUserError`
- 当年龄 < 0 或邮箱缺失时抛出异常

---

## Day 3：JSON 处理

### W2-E07 加载脏数据 JSON

- 输入包含缺失字段、错误类型

### W2-E08 数据清洗

- 保证输出字段：`id/name/department/role/age`

### W2-E09 双维度统计

- 统计：
  - 按部门人数
  - 按角色人数

### W2-E10 导出统计结果

- 输出到 `summary.json`

---

## Day 4：CSV 报表

### W2-E11 读取 orders.csv

- 字段：`order_id,user_id,amount,created_at`

### W2-E12 用户消费统计

- 每个用户：总消费、订单数、客单价

### W2-E13 导出报表

- 输出 `order_report.csv`

---

## Day 5：mini project

### W2-E14 参数化运行

- 支持 `--input --output --format`

### W2-E15 多格式输入

- 可读取 JSON 或 CSV

### W2-E16 汇总输出

- 控制台打印 summary
- 同时落盘到目标目录

---

## 完成打卡

- [ ] W2-E01
- [ ] W2-E02
- [ ] W2-E03
- [ ] W2-E04
- [ ] W2-E05
- [ ] W2-E06
- [ ] W2-E07
- [ ] W2-E08
- [ ] W2-E09
- [ ] W2-E10
- [ ] W2-E11
- [ ] W2-E12
- [ ] W2-E13
- [ ] W2-E14
- [ ] W2-E15
- [ ] W2-E16

