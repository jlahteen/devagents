# Microsoft Agent Framework Migration Plan

**Date**: January 28, 2026  
**Goal**: Replace AutoGen with Microsoft Agent Framework (MAF) in `agent_platform/` while preserving public API  
**Scope**: Internal implementation changes only - zero impact on `workflows/`, `agents/`, `tests/`, `utils/`

---

## Executive Summary

**Strategy**: Keep platform-agnostic abstraction layer unchanged, swap AutoGen implementation for MAF implementation.

**Files Modified**: Only 4 files in `agent_platform/`:
- `agent_base.py` - Agent creation and tool wrapping
- `agent_team.py` - Team orchestration with speaker selection
- `inner_team_agent_base.py` - Nested team agents
- `termination.py` - Termination conditions

**Estimated Effort**: 7-10 days (reduced from initial 12-17 days due to focused scope)

---

## Current AutoGen API Usage

### 1. Agent Creation (`agent_base.py`)

#### Current AutoGen Implementation:
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import FunctionTool

class AgentBase(AssistantAgent):
    def __init__(self, name, system_message, config, tools):
        super().__init__(
            name=name,
            system_message=system_message,
            model_client=ChatCompletionClient.load_component(config.model_client),
            tools=self._to_autogen_tools()
        )
    
    async def run(self, prompt):
        response = await self.on_messages(
            [TextMessage(content=prompt, source="user")], 
            CancellationToken()
        )
        return response.chat_message.content
    
    def _to_autogen_tools(self):
        return [FunctionTool(func=tool, description=tool.__doc__) for tool in self._tools]
```

#### MAF Target Implementation:
```python
from agent_framework import ChatAgent, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function

class AgentBase:  # No longer inherits from framework class
    def __init__(self, name, system_message, config, tools):
        self._name = name
        self._system_message = system_message
        self._config = config
        self._tools = tools or []
        
        # Create MAF chat client
        chat_client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            # Additional config from self._config
        )
        
        # Create MAF ChatAgent
        self._agent = ChatAgent(
            name=name,
            instructions=system_message,
            chat_client=chat_client,
            tools=self._to_maf_tools()
        )
    
    async def run(self, prompt):
        response = await self._agent.run(prompt)
        return response.text  # MAF AgentResponse.text
    
    def _to_maf_tools(self):
        # MAF uses @ai_function decorator or AIFunction objects
        # Tools are already callable, wrap them as AIFunction
        maf_tools = []
        for tool in self._tools:
            # Create AIFunction wrapper
            func = ai_function(
                func=tool,
                name=tool.__name__,
                description=tool.__doc__ or f"Tool: {tool.__name__}"
            )
            maf_tools.append(func)
        return maf_tools
```

**Key Changes**:
- ❌ Remove inheritance from `AssistantAgent`
- ✅ Composition: Create internal `ChatAgent` instance
- ✅ Replace `ChatCompletionClient.load_component()` → `AzureOpenAIChatClient()`
- ✅ Replace `FunctionTool` → `@ai_function` or `AIFunction`
- ✅ Replace `on_messages()` → `agent.run()`
- ✅ Replace `TextMessage` → plain string prompt
- ✅ Replace `response.chat_message.content` → `response.text`

---

### 2. Team Orchestration (`agent_team.py`)

#### Current AutoGen Implementation:
```python
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.ui import Console

class AgentTeam:
    def __init__(self, agents, config, selector_func, termination_condition):
        model_client = ChatCompletionClient.load_component(config.model_client)
        self._team = SelectorGroupChat(
            participants=agents,
            model_client=model_client,
            selector_func=self._select_next_speaker,
            termination_condition=termination_condition,
            max_turns=999
        )
    
    def _select_next_speaker(self, messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
        # Adapter: converts AutoGen messages to platform-agnostic Message
        message_count = len(messages)
        last_message = None
        if message_count > 0:
            msg = messages[-1]
            last_message = Message(source=msg.source, content=getattr(msg, "content", ""))
        return self._selector_func(message_count, last_message)
    
    async def run(self, prompt):
        await Console(self._team.run_stream(task=prompt))
```

#### MAF Target Implementation:
```python
from agent_framework import GroupChatBuilder, GroupChatState
from agent_framework import WorkflowOutputEvent

class AgentTeam:
    def __init__(self, agents, config, selector_func, termination_condition):
        self._selector_func = selector_func
        
        # Convert our AgentBase instances to MAF ChatAgent instances
        maf_agents = [agent._agent for agent in agents]
        
        # Build MAF group chat workflow
        self._workflow = (
            GroupChatBuilder()
            .with_select_speaker_func(self._maf_selector_func)
            .participants(maf_agents)
            .with_termination_condition(termination_condition)
            .with_max_rounds(999)
            .build()
        )
    
    def _maf_selector_func(self, state: GroupChatState) -> str:
        # Adapter: converts MAF GroupChatState to platform-agnostic Message
        message_count = state.current_round
        last_message = None
        if state.conversation:
            msg = state.conversation[-1]
            last_message = Message(
                source=msg.author_name or msg.role.value,
                content=msg.text
            )
        return self._selector_func(message_count, last_message)
    
    async def run(self, prompt):
        async for event in self._workflow.run_stream(prompt):
            if isinstance(event, WorkflowOutputEvent):
                # Handle final output
                pass
            # MAF has different event types - may need to adapt Console output
```

**Key Changes**:
- ✅ Replace `SelectorGroupChat` → `GroupChatBuilder().build()`
- ✅ Replace `model_client` parameter → chat client embedded in agents
- ✅ Adapter: `Sequence[AgentEvent | ChatMessage]` → `GroupChatState`
- ✅ Extract MAF internal agents: `agent._agent` from our wrapper
- ✅ Replace `Console(team.run_stream())` → custom event handling
- ✅ Replace `max_turns` → `with_max_rounds()`

---

### 3. Nested Team Agents (`inner_team_agent_base.py`)

#### Current AutoGen Implementation:
```python
from autogen_agentchat.agents import SocietyOfMindAgent
from autogen_agentchat.teams import SelectorGroupChat

class InnerTeamAgentBase(SocietyOfMindAgent):
    def __init__(self, name, config, agents, speaker_selector, 
                 termination_condition, system_message, response_prompt):
        model_client = ChatCompletionClient.load_component(config.model_client)
        team = SelectorGroupChat(
            agents,
            model_client=model_client,
            selector_func=self._select_next_speaker,
            termination_condition=termination_condition
        )
        
        super().__init__(
            name=name,
            team=team,
            model_client=model_client,
            instruction=system_message,
            response_prompt=response_prompt
        )
    
    async def run_inner_team(self, prompt):
        await Console(self.run_stream(task=prompt))
```

#### MAF Target Implementation:
```python
from agent_framework import GroupChatBuilder

class InnerTeamAgentBase:
    def __init__(self, name, config, agents, speaker_selector,
                 termination_condition, system_message, response_prompt):
        self._name = name
        self._config = config
        self._system_message = system_message
        self._response_prompt = response_prompt
        
        # Extract MAF agents
        maf_agents = [agent._agent for agent in agents]
        
        # Build inner team workflow
        self._workflow = (
            GroupChatBuilder()
            .with_select_speaker_func(self._maf_selector_func)
            .participants(maf_agents)
            .with_termination_condition(termination_condition)
            .build()
        )
        
        # MAF: Workflows can be converted to agents
        # This is the key to nested teams!
        self._agent = self._workflow.as_agent()
    
    def _maf_selector_func(self, state: GroupChatState) -> str:
        # Same adapter as AgentTeam
        message_count = state.current_round
        last_message = None
        if state.conversation:
            msg = state.conversation[-1]
            last_message = Message(
                source=msg.author_name or msg.role.value,
                content=msg.text
            )
        return self._speaker_selector(message_count, last_message)
    
    async def run_inner_team(self, prompt):
        # Use the workflow-as-agent
        response = await self._agent.run(prompt)
        # Handle streaming if needed
```

**Key Changes**:
- ❌ Remove inheritance from `SocietyOfMindAgent`
- ✅ Replace `SelectorGroupChat` → `GroupChatBuilder().build()`
- ✅ **Critical**: Use `workflow.as_agent()` for nested teams
- ✅ Replace `super().__init__()` with workflow creation
- ⚠️ **Investigation needed**: MAF's `workflow.as_agent()` behavior vs AutoGen's `SocietyOfMindAgent`

---

### 4. Termination Conditions (`termination.py`)

#### Current AutoGen Implementation:
```python
from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import StopMessage

class MessageTermination(TextMentionTermination):
    pass

class SuccessOrFailureTermination(TerminationCondition):
    async def __call__(self, messages):
        for message in reversed(messages):
            if self._success_phrase in message.content:
                return StopMessage(...)
            if self._failure_phrase in message.content:
                if self._on_failure_callback:
                    await self._on_failure_callback(message.content)
                return StopMessage(...)
        return None
```

#### MAF Target Implementation:
```python
# MAF uses TerminationCondition = Callable[[list[ChatMessage]], bool | Awaitable[bool]]

class MessageTermination:
    """Terminates when specific text is mentioned."""
    
    def __init__(self, text: str):
        self._text = text
    
    def __call__(self, conversation: list) -> bool:
        # MAF expects bool, not StopMessage
        for message in reversed(conversation):
            if hasattr(message, 'text') and self._text in message.text:
                return True
        return False

class SuccessOrFailureTermination:
    """Terminates on success or failure phrase."""
    
    def __init__(self, success_phrase, failure_phrase, on_failure_callback=None):
        self._success_phrase = success_phrase
        self._failure_phrase = failure_phrase
        self._on_failure_callback = on_failure_callback
    
    async def __call__(self, conversation: list) -> bool:
        # MAF: Returns bool instead of StopMessage
        for message in reversed(conversation):
            if not hasattr(message, 'text'):
                continue
            
            if self._success_phrase in message.text:
                return True
            
            if self._failure_phrase in message.text:
                # Callback handling
                if self._on_failure_callback:
                    if asyncio.iscoroutinefunction(self._on_failure_callback):
                        await self._on_failure_callback(message.text)
                    else:
                        self._on_failure_callback(message.text)
                return True
        
        return False
```

**Key Changes**:
- ✅ Replace `StopMessage` → `bool` return type
- ✅ MAF termination signature: `Callable[[list[ChatMessage]], bool | Awaitable[bool]]`
- ✅ No need to inherit from `TerminationCondition` base class
- ✅ Callback support maintained
- ✅ Message iteration logic similar

---

## API Mapping Summary

| AutoGen API | MAF API | Change Type |
|-------------|---------|-------------|
| `AssistantAgent` | `ChatAgent` | Replace + Composition |
| `ChatCompletionClient.load_component()` | `AzureOpenAIChatClient(credential=...)` | Config change |
| `FunctionTool(func=...)` | `@ai_function` or `AIFunction(...)` | Wrapper change |
| `agent.on_messages([TextMessage(...)])` | `agent.run(prompt_str)` | API simplification |
| `response.chat_message.content` | `response.text` | Property change |
| `SelectorGroupChat(...)` | `GroupChatBuilder().build()` | Builder pattern |
| `Sequence[AgentEvent \| ChatMessage]` | `GroupChatState` | State object |
| `msg.source`, `msg.content` | `msg.author_name`, `msg.text` | Property names |
| `SocietyOfMindAgent` | `workflow.as_agent()` | Nested team pattern |
| `TerminationCondition → StopMessage` | `TerminationCondition → bool` | Return type |
| `Console(team.run_stream())` | `async for event in workflow.run_stream()` | Event handling |
| `max_turns` | `with_max_rounds()` | Builder method |

---

## New Abstractions Needed

### 1. MAF Chat Client Factory
```python
# New utility in agent_platform/
def create_maf_chat_client(config: Config):
    """Creates MAF chat client from our Config."""
    from agent_framework.azure import AzureOpenAIChatClient
    from azure.identity import DefaultAzureCredential
    
    return AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        # Map config.model_client to MAF parameters
    )
```

### 2. Message Adapter Utilities
```python
# agent_platform/adapters.py (new file)
from agent_framework import ChatMessage as MAFChatMessage
from agent_platform.agent_base import Message

def maf_to_platform_message(maf_msg: MAFChatMessage) -> Message:
    """Converts MAF ChatMessage to platform-agnostic Message."""
    return Message(
        source=maf_msg.author_name or maf_msg.role.value,
        content=maf_msg.text
    )

def platform_to_maf_message(msg: Message) -> MAFChatMessage:
    """Converts platform-agnostic Message to MAF ChatMessage."""
    # May not be needed, MAF accepts string prompts
    pass
```

### 3. GroupChatState Adapter
```python
def extract_platform_message_from_state(state: GroupChatState) -> tuple[int, Message | None]:
    """Extracts message info from MAF GroupChatState."""
    message_count = state.current_round
    last_message = None
    if state.conversation:
        last_msg = state.conversation[-1]
        last_message = Message(
            source=last_msg.author_name or last_msg.role.value,
            content=last_msg.text
        )
    return message_count, last_message
```

---

## Implementation Phases

### Phase 0: Preparation (0.5 days)
**Goal**: Setup dependencies and research

- [ ] Add `agent-framework` to requirements.txt
- [ ] Install MAF: `pip install agent-framework[azure] --pre`
- [ ] Research MAF authentication patterns
- [ ] Review MAF examples for best practices
- [ ] Create `agent_platform/adapters.py` for message conversion

### Phase 1: AgentBase Migration (1.5 days)
**Goal**: Single agent works with tools

- [ ] Create MAF chat client factory
- [ ] Remove inheritance from `AssistantAgent`
- [ ] Replace with composition: internal `ChatAgent`
- [ ] Implement `_to_maf_tools()` using `@ai_function`
- [ ] Update `run()` method to use MAF API
- [ ] **Test**: `test_developer_agent.py` should pass

### Phase 2: Termination Migration (1 day)
**Goal**: Termination conditions work with MAF

- [ ] Update `MessageTermination` to return `bool`
- [ ] Update `SuccessOrFailureTermination` to return `bool`
- [ ] Remove `StopMessage` references
- [ ] Test callback invocation
- [ ] **Test**: Termination logic validated

### Phase 3: AgentTeam Migration (2 days)
**Goal**: Team orchestration works

- [ ] Replace `SelectorGroupChat` with `GroupChatBuilder`
- [ ] Implement MAF selector adapter (`GroupChatState` → `Message`)
- [ ] Update `run()` to handle MAF workflow events
- [ ] Handle MAF streaming output properly
- [ ] **Test**: Simple team workflows pass

### Phase 4: InnerTeamAgentBase Migration (2.5 days)
**Goal**: Nested teams work (most complex)

- [ ] Replace `SocietyOfMindAgent` with workflow composition
- [ ] Use `workflow.as_agent()` pattern
- [ ] Verify nested team execution
- [ ] Verify `run_inner_team()` behavior
- [ ] **Test**: `test_build_agent.py` passes (complex nested teams)

### Phase 5: Integration Testing (2 days)
**Goal**: All workflows pass

- [ ] Run all workflow tests: `python tests/run_tests.py`
- [ ] Fix any integration issues
- [ ] Verify keyword-based transitions still work
- [ ] Test error handling and callbacks
- [ ] **Validate**: All tests green

### Phase 6: Cleanup & Documentation (0.5 days)
**Goal**: Finalize migration

- [ ] Remove all AutoGen imports
- [ ] Update requirements.txt (remove autogen)
- [ ] Update copilot-instructions.md
- [ ] Document MAF-specific behaviors
- [ ] Update README if needed

**Total Estimated Time**: 10 days (conservative with buffer)

---

## Risk Assessment

### High Risk ⚠️
1. **Nested team behavior** - MAF's `workflow.as_agent()` may behave differently than AutoGen's `SocietyOfMindAgent`
   - **Mitigation**: Test early in Phase 4, be ready to adapt pattern
   
2. **Tool result propagation** - MAF may handle tool results differently
   - **Mitigation**: Validate in Phase 1 with simple tool tests

### Medium Risk ⚠️
3. **Streaming output** - MAF event types differ from AutoGen
   - **Mitigation**: May need custom event handler instead of `Console`
   
4. **Configuration mapping** - Our `Config` may not map 1:1 to MAF client params
   - **Mitigation**: Create flexible client factory in Phase 0

### Low Risk ✅
5. **Message adaptation** - Well-defined pattern
6. **Termination conditions** - Clear API mapping
7. **Tool wrapping** - MAF `@ai_function` is straightforward

---

## Success Criteria

✅ **All existing tests pass without modification**  
✅ **Zero changes to `workflows/`, `agents/`, `tests/`, `utils/`**  
✅ **All keyword-based transitions work correctly**  
✅ **Tool execution and results propagate correctly**  
✅ **Nested teams function as before**  
✅ **Error callbacks still trigger**  

---

## Open Questions for MAF Research

1. ❓ Does `workflow.as_agent()` support the same `run()` interface as `ChatAgent`?
2. ❓ How does MAF handle tool execution failures?
3. ❓ Can MAF workflows be nested multiple levels deep?
4. ❓ What's the exact event sequence from `workflow.run_stream()`?
5. ❓ Does MAF support custom authentication beyond `DefaultAzureCredential()`?

---

## Decision Points

### Decision 1: Keep AutoGen as fallback?
**Option A**: Delete AutoGen entirely after migration  
**Option B**: Keep AutoGen code in branch for comparison  
**Recommendation**: Option B - keep AutoGen branch for reference

### Decision 2: Event handling
**Option A**: Keep `Console` wrapper if MAF supports it  
**Option B**: Custom event handler for our needs  
**Recommendation**: Option B - gives more control

### Decision 3: Testing strategy
**Option A**: Migrate all at once, then test  
**Option B**: Phase-by-phase testing  
**Recommendation**: Option B - catch issues early

---

## Next Steps

1. **Review this plan** - Validate approach and estimates
2. **Phase 0 prep** - Install MAF, create adapters
3. **Quick POC** - Test single agent with tool (30 min validation)
4. **Begin Phase 1** - Migrate `AgentBase`

---

**Ready to proceed?** Let me know if you want to:
- Adjust any phases
- Clarify specific mappings
- Start with Phase 0 preparation
