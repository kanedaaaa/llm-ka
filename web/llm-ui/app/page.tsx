"use client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send } from "lucide-react"
import { useState } from "react"

export default function Home() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<{ role: "user" | "assistant", content: string }[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = () => {
    if (!input.trim()) return

    const userMessage = { role: "user" as const, content: input }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    setTimeout(() => {
      const aiResponse = {
        role: "assistant" as const,
        content: "This is a dummy response. In a real implementation, this would be the LLM's response to your message: " + input
      }
      setMessages(prev => [...prev, aiResponse])
      setIsLoading(false)
    }, 1000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-screen">
      {messages.length === 0 ? (
        <div className="flex-1 flex items-center justify-center p-5">
          <div className="w-full max-w-3xl">
            <h1 className="text-4xl font-bold mb-4">Welcome to the LLM chat</h1>
            <p className="text-muted-foreground mb-6">
              Ask me anything! I'm here to help you with your questions and concerns.
            </p>
            <div className="relative">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your message..."
                className="rounded-2xl pr-12 py-6"
              />
              <Button
                size="icon"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 mr-[4px] flex justify-center items-center"
                onClick={handleSend}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-y-auto p-4">
            <div className="max-w-3xl mx-auto space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-2xl ${message.role === "user"
                    ? "bg-primary text-primary-foreground ml-auto"
                    : "bg-muted"
                    } max-w-[80%] ${message.role === "user" ? "ml-auto" : "mr-auto"}`}
                >
                  {message.content}
                </div>
              ))}
              {isLoading && (
                <div className="p-4 rounded-2xl bg-muted max-w-[80%] mr-auto">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-muted-foreground/20 animate-bounce [animation-delay:-0.3s]"></div>
                    <div className="w-2 h-2 rounded-full bg-muted-foreground/20 animate-bounce [animation-delay:-0.15s]"></div>
                    <div className="w-2 h-2 rounded-full bg-muted-foreground/20 animate-bounce"></div>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="bg-background p-5">
            <div className="max-w-3xl mx-auto">
              <div className="relative">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder="Type your message..."
                  className="rounded-2xl pr-12 py-6"
                />
                <Button
                  size="icon"
                  className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 mr-[4px] flex justify-center items-center"
                  onClick={handleSend}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )

}
