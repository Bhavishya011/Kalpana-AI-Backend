# Frontend Integration Guide

## Integrating Chatbot API into Support Center

This guide shows how to integrate the chatbot API into your `support-center.tsx` component.

---

## Step 1: Update Environment Variables

Create `.env.local` in your project root:
```env
NEXT_PUBLIC_CHATBOT_API_URL=https://support-chatbot-api-XXXXX.run.app
```

Or for development:
```env
NEXT_PUBLIC_CHATBOT_API_URL=http://localhost:8083
```

---

## Step 2: Create Chatbot Hook

Create `src/hooks/useChatbot.ts`:

```typescript
import { useState, useCallback } from 'react';

interface ChatMessage {
  role: 'user' | 'bot';
  content: string;
  timestamp: string;
}

interface ChatResponse {
  response: string;
  session_id: string;
  timestamp: string;
  language: string;
}

const CHATBOT_API_URL = process.env.NEXT_PUBLIC_CHATBOT_API_URL || 'http://localhost:8083';

export const useChatbot = (language: string = 'en-US') => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>(`session_${Date.now()}`);

  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch(`${CHATBOT_API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          language,
          history: messages.slice(-5) // Last 5 messages for context
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      // Add bot response
      const botMessage: ChatMessage = {
        role: 'bot',
        content: data.response,
        timestamp: data.timestamp
      };
      setMessages(prev => [...prev, botMessage]);
      setSessionId(data.session_id);

    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      const errorMessage: ChatMessage = {
        role: 'bot',
        content: language === 'hi-IN' 
          ? 'क्षमा करें, मुझे जवाब देने में परेशानी हो रही है। कृपया पुनः प्रयास करें।'
          : 'Sorry, I\'m having trouble responding. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [language, sessionId, messages]);

  const getQuickHelp = useCallback(async (category: string) => {
    setIsLoading(true);

    try {
      const response = await fetch(`${CHATBOT_API_URL}/quick-help?category=${category}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      // Add quick help response
      const botMessage: ChatMessage = {
        role: 'bot',
        content: data.response,
        timestamp: data.timestamp
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Quick help error:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const resetChat = useCallback(async () => {
    try {
      await fetch(`${CHATBOT_API_URL}/chat/reset?session_id=${sessionId}`, {
        method: 'POST',
      });
      
      setMessages([]);
      setSessionId(`session_${Date.now()}`);
    } catch (error) {
      console.error('Reset error:', error);
    }
  }, [sessionId]);

  return {
    messages,
    isLoading,
    sendMessage,
    getQuickHelp,
    resetChat
  };
};
```

---

## Step 3: Update Support Center Component

Update `src/components/dashboard/support-center.tsx`:

```typescript
"use client"

import { useState, useEffect, useRef } from "react"
import { Search, MessageCircle, Send, X, RotateCcw } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { useChatbot } from "@/hooks/useChatbot"
import { useLanguage } from "@/contexts/LanguageContext"

export function SupportCenter() {
  const { language } = useLanguage()
  const { messages, isLoading, sendMessage, getQuickHelp, resetChat } = useChatbot(language)
  
  const [searchQuery, setSearchQuery] = useState("")
  const [chatMessage, setChatMessage] = useState("")
  const [isChatOpen, setIsChatOpen] = useState(false)
  
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!chatMessage.trim()) return

    await sendMessage(chatMessage)
    setChatMessage("")
  }

  const handleQuickHelp = async (category: string) => {
    setIsChatOpen(true)
    await getQuickHelp(category)
  }

  const quickHelpButtons = [
    { category: "getting-started", label: "Getting Started" },
    { category: "product-creation", label: "Create Product" },
    { category: "market-pulse", label: "Market Pulse" },
    { category: "the-muse", label: "The Muse" },
    { category: "artisan-mentor", label: "Artisan Mentor" },
    { category: "pricing", label: "Pricing" },
    { category: "languages", label: "Languages" },
    { category: "support", label: "Contact Support" }
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Support Center</h1>
        <p className="text-muted-foreground mt-2">
          Get help and answers to your questions
        </p>
      </div>

      {/* Search Bar */}
      <Card>
        <CardContent className="p-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search for help articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Quick Help Buttons */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Quick Help</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickHelpButtons.map((btn) => (
            <Button
              key={btn.category}
              variant="outline"
              onClick={() => handleQuickHelp(btn.category)}
              className="h-auto py-4 flex flex-col items-center gap-2"
            >
              <MessageCircle className="h-5 w-5" />
              <span className="text-sm">{btn.label}</span>
            </Button>
          ))}
        </div>
      </div>

      {/* Chat Widget */}
      {isChatOpen && (
        <Card className="fixed bottom-6 right-6 w-96 h-[600px] flex flex-col shadow-2xl z-50">
          {/* Chat Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <div className="flex items-center gap-2">
              <MessageCircle className="h-5 w-5 text-primary" />
              <h3 className="font-semibold">AI Support Assistant</h3>
              <Badge variant="secondary" className="text-xs">Online</Badge>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="icon"
                onClick={resetChat}
                title="Reset Chat"
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsChatOpen(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Chat Messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.length === 0 && (
                <div className="text-center text-muted-foreground text-sm py-8">
                  <MessageCircle className="h-12 w-12 mx-auto mb-2 opacity-50" />
                  <p>Hello! How can I help you today?</p>
                  <p className="text-xs mt-2">
                    Ask me anything about KalpanaAI features!
                  </p>
                </div>
              )}

              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      msg.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-muted rounded-lg p-3">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>
          </ScrollArea>

          {/* Chat Input */}
          <div className="p-4 border-t">
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <Input
                placeholder="Type your message..."
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                disabled={isLoading}
              />
              <Button type="submit" size="icon" disabled={isLoading}>
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </Card>
      )}

      {/* Floating Chat Button (when chat closed) */}
      {!isChatOpen && (
        <Button
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg z-50"
          onClick={() => setIsChatOpen(true)}
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      )}

      {/* Existing support articles, FAQs, etc. */}
      {/* ... rest of your component ... */}
    </div>
  )
}
```

---

## Step 4: Update Tailwind Config (Optional)

Add animation delays in `tailwind.config.ts`:

```typescript
export default {
  theme: {
    extend: {
      animation: {
        'bounce': 'bounce 1s infinite',
      },
      keyframes: {
        bounce: {
          '0%, 100%': {
            transform: 'translateY(0)',
            animationTimingFunction: 'cubic-bezier(0.8, 0, 1, 1)',
          },
          '50%': {
            transform: 'translateY(-25%)',
            animationTimingFunction: 'cubic-bezier(0, 0, 0.2, 1)',
          },
        },
      },
    },
  },
}
```

---

## Step 5: Testing

### Test the Integration

1. **Start API locally** (optional):
   ```bash
   cd support-chatbot-api
   uvicorn main:app --reload --port 8083
   ```

2. **Start frontend**:
   ```bash
   npm run dev
   ```

3. **Test chat**:
   - Click chat button (bottom-right)
   - Try quick help buttons
   - Send messages
   - Change language in header
   - Test multilingual responses

### Test Multilingual

```typescript
// In your component
const testMessages = {
  'en-US': "How do I create a product?",
  'hi-IN': "मुझे उत्पाद कैसे बनाना है?",
  'bn-IN': "আমি কীভাবে পণ্য তৈরি করব?",
  'ta-IN': "நான் எப்படி தயாரிப்பு உருவாக்குவது?"
}
```

---

## Step 6: Production Deployment

### Update Environment Variable

After deploying API to Cloud Run:

```env
NEXT_PUBLIC_CHATBOT_API_URL=https://support-chatbot-api-YOUR_ID.run.app
```

### Rebuild and Deploy Frontend

```bash
npm run build
npm run deploy
```

---

## Features Implemented

✅ Real-time chat interface  
✅ Quick help buttons  
✅ Multilingual support (auto-switches with header language)  
✅ Session management  
✅ Conversation context  
✅ Loading states  
✅ Error handling  
✅ Reset chat functionality  
✅ Auto-scroll to bottom  
✅ Typing indicator  
✅ Responsive design  
✅ Floating chat button  

---

## Advanced Features (Optional)

### 1. Message Persistence

Store messages in localStorage:

```typescript
useEffect(() => {
  localStorage.setItem('chat_messages', JSON.stringify(messages))
}, [messages])

useEffect(() => {
  const saved = localStorage.getItem('chat_messages')
  if (saved) setMessages(JSON.parse(saved))
}, [])
```

### 2. Typing Indicator

Show when bot is typing:

```typescript
const [isTyping, setIsTyping] = useState(false)

// Before API call
setIsTyping(true)

// After response
setIsTyping(false)
```

### 3. Message Reactions

Allow users to rate responses:

```typescript
const [messageRatings, setMessageRatings] = useState<Record<number, boolean>>({})

const rateMessage = (idx: number, helpful: boolean) => {
  setMessageRatings(prev => ({ ...prev, [idx]: helpful }))
  // Send feedback to analytics
}
```

### 4. Suggested Questions

Show suggested follow-up questions:

```typescript
const suggestions = [
  "How does pricing work?",
  "Tell me about Market Pulse",
  "How do I use The Muse?"
]
```

---

## Troubleshooting

### Chat not working

1. Check API URL:
   ```typescript
   console.log('API URL:', process.env.NEXT_PUBLIC_CHATBOT_API_URL)
   ```

2. Check CORS (add to `main.py` if needed):
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Change in production
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. Check network tab in browser dev tools

### Messages not translating

Ensure language is passed correctly:
```typescript
const { language } = useLanguage()
const { sendMessage } = useChatbot(language)  // Pass language here
```

### Session issues

Reset session if needed:
```typescript
const resetSession = () => {
  setSessionId(`session_${Date.now()}`)
  setMessages([])
}
```

---

## Performance Optimization

### 1. Debounce Typing

```typescript
import { debounce } from 'lodash'

const debouncedSend = debounce(sendMessage, 500)
```

### 2. Lazy Load Chat

```typescript
const ChatWidget = lazy(() => import('./ChatWidget'))

<Suspense fallback={<LoadingSpinner />}>
  {isChatOpen && <ChatWidget />}
</Suspense>
```

### 3. Virtualize Long Chats

For very long conversations, use `react-virtual`:

```typescript
import { useVirtual } from 'react-virtual'

const { virtualItems } = useVirtual({
  size: messages.length,
  parentRef: scrollRef
})
```

---

## Next Steps

1. ✅ Deploy chatbot API to Cloud Run
2. ✅ Update `NEXT_PUBLIC_CHATBOT_API_URL` in `.env.local`
3. ✅ Create `useChatbot` hook
4. ✅ Update `support-center.tsx` with chat UI
5. ✅ Test locally
6. ✅ Deploy frontend
7. ✅ Monitor usage and feedback

---

## Support

For integration help:
- API Documentation: `API_DOCUMENTATION.md`
- Quick Start: `QUICKSTART.md`
- Contact: dev@kalpana-ai.com
