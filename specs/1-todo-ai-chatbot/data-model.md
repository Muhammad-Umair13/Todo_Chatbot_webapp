# Data Model

**Conversation**:
- id: int PK
- user_id: str FK(User.id)
- title: str
- created_at: datetime

**Message**:
- id: int PK
- conversation_id: int FK
- role: str (user/assistant/tool)
- content: text
- metadata: JSONB
- created_at: datetime