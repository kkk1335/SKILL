# E2E Test Case Design Patterns

## Analysis Workflow

When analyzing a requirements document, follow this systematic approach:

### 1. Identify Functional Modules
- Scan for distinct features, user flows, or subsystems
- Each major feature area becomes a top-level module in the test plan
- Group related sub-features under the same module

### 2. Extract Test Points Per Module
For each module, derive test points from:
- **Explicit requirements**: Directly stated behaviors ("用户可以...")
- **Implicit requirements**: Obvious necessities (error handling, edge cases)
- **Business rules**: Validation rules, constraints, calculations
- **User flows**: Happy path + alternative paths
- **Data scenarios**: Different data states (empty, normal, boundary, invalid)
- **Permission scenarios**: Different user roles and access levels

### 3. Apply Test Design Techniques

| Technique | When to Use | Example |
|-----------|-------------|---------|
| Equivalence Partitioning | Input ranges, categories | Age: <0, 0-17, 18-60, >60 |
| Boundary Value Analysis | Numeric/date limits | Min-1, Min, Min+1, Max-1, Max, Max+1 |
| Decision Table | Complex business rules | Discount based on member_level × order_amount |
| State Transition | Multi-step flows | Order: created → paid → shipped → completed |
| Error Guessing | Based on experience | Null input, concurrent operations, network timeout |
| Scenario Testing | End-to-end user stories | Complete checkout flow |

### 4. Test Case Structure

Each test case MUST include:
- **测试点 (Test Point)**: What specific behavior/condition is being verified
- **前置条件 (Precondition)**: System state, data setup, user state before test
- **测试步骤 (Steps)**: Sequential, numbered, unambiguous actions
- **预期结果 (Expected Result)**: Observable, verifiable outcome for each step or final state

## Common E2E Test Dimensions

For any module, consider these cross-cutting dimensions:

### Functional
- Happy path (normal usage)
- Alternative paths (different valid inputs/approaches)
- Error handling (invalid inputs, failures)
- Boundary conditions

### Data
- No data / empty state
- Single item
- Multiple items (pagination if applicable)
- Maximum capacity
- Special characters in text fields

### User Roles & Permissions
- Admin / regular user / guest
- Owner vs. non-owner actions
- Cross-account scenarios

### Environment
- Different browsers / devices (if applicable)
- Network conditions (offline, slow)
- Concurrent users

### Integration
- Dependencies on other systems
- Data sync scenarios
- Webhook / notification triggers

## XMind Mind Map Structure

```
Root: 项目名称 - E2E测试用例
├── 模块A: 用户登录
│   ├── TC-001: 正常登录 - 有效账号密码
│   │   ├── 前置条件: 用户已注册且账号状态正常
│   │   ├── 测试步骤
│   │   │   ├── 1. 打开登录页面
│   │   │   ├── 2. 输入有效用户名和密码
│   │   │   └── 3. 点击登录按钮
│   │   └── 预期结果: 登录成功，跳转至首页
│   ├── TC-002: 密码错误
│   │   ├── 前置条件: ...
│   │   ├── 测试步骤
│   │   └── 预期结果: ...
│   └── TC-003: 账号被锁定
├── 模块B: 商品搜索
│   ├── TC-001: ...
│   └── TC-002: ...
└── 模块C: 订单管理
    └── TC-001: ...
```

## JSON Specification Format

The intermediate JSON passed to generate_xmind.py:

```json
{
    "title": "项目名称 - E2E测试用例",
    "modules": [
        {
            "name": "模块名称",
            "test_cases": [
                {
                    "id": "TC-001",
                    "test_point": "测试点描述",
                    "precondition": "前置条件",
                    "steps": ["步骤1", "步骤2"],
                    "expected": "预期结果"
                }
            ]
        }
    ]
}
```

### ID Convention
- Format: `TC-XXX` (3-digit sequential number)
- Per-module sequential, e.g., TC-001 ~ TC-015 for Module A, TC-001 ~ TC-010 for Module B
- Or global sequential if user prefers
