# LangChain

## 1. Chat Models
LangChain provides chat-model implementations for popular LLM providers with a common interface.

### Features Covered:
- **OpenAI Integration**: Using `ChatOpenAI` with specific models like `gpt-4o-mini`
- **Google Gemini Integration**: Using `ChatGoogleGenerativeAI` with models like `gemini-2.0-flash`
- **Generic Provider Support**: Using `init_chat_model` for flexible provider selection
- **Message Formats**: Working with `SystemMessage`, `HumanMessage`, and `AIMessage`
- **Chat History**: Managing conversation context across multiple exchanges

## 2. Prompt Templates
Dynamic prompt creation and management for structured LLM interactions.

### Features Covered:
- **Simple Prompt Templates**: Using `PromptTemplate.from_template()` for basic variable substitution
- **Chat Prompt Templates**: Supporting both OpenAI format (`system`, `user`, `assistant`) and LangChain format (`system`, `human`, `ai`)
- **Message Placeholders**: Using `MessagesPlaceholder` and placeholder syntax for dynamic message insertion
- **Template Formatting**: Variable injection and prompt composition

## 3. Tools
External tool integration allowing LLMs to perform actions and access real-world data.

### Features Covered:
- **Simple Tool Creation**: Using `@tool` decorator for basic function-to-tool conversion
- **Injected Tool Arguments**: Runtime argument allocation with `InjectedToolArg`
- **Tools with Artifacts**: Using `response_format='content_and_artifact'` for enhanced tool responses
- **Tool Binding**: Connecting tools to LLMs with `bind_tools()`
- **Tool Invocation**: Direct tool execution and LLM-triggered tool calls

## 4. Structured Output
Generating structured, validated responses from LLMs.

### Features Covered:
- **JSON Mode**: Simple structured output using `with_structured_output(method='json_mode')`
- **Pydantic Schema Integration**: Type-safe responses using Pydantic models with field validation
- **Response Validation**: Automatic parsing and validation of LLM outputs

## 5. Runnables (Chains)
Composable workflow building blocks for creating complex LLM pipelines.

### Features Covered:
- **Sequential Runnables**: Chaining operations with `RunnableSequence`
- **Parallel Runnables**: Concurrent execution with `RunnableParallel`
- **Lambda Runnables**: Custom functions as runnable components with `RunnableLambda`
- **Passthrough Runnables**: Input forwarding with `RunnablePassthrough`
- **Conditional Runnables**: Branching logic with `RunnableBranch`
- **Output Parsing**: Response formatting with `StrOutputParser`

## 6. Streaming
Real-time response generation for better user experience.

### Features Covered:
- **LLM Streaming**: Direct model streaming with `.stream()` method
- **Chain Streaming**: Streaming through runnable sequences
- **Chunk Processing**: Real-time content processing as responses are generated

## 7. Batch Processing
Efficient processing of multiple requests simultaneously.

### Features Covered:
- **Sequential Batch Processing**: Processing multiple inputs with `.batch()` 
- **Async Batch Processing**: Non-blocking batch execution with `.batch_as_completed()`
- **Result Ordering**: Both ordered and completion-order result handling