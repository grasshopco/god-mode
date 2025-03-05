"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { AlertTriangle, Copy, Check, Send, Loader, FileText, ArrowRight, RefreshCw } from 'lucide-react';
import { useAdaptedTheme } from '@/lib/theme-adapter';
import { cn } from '@/lib/utils';

// Add types for our API responses
interface EnhanceResponse {
  enhancedPrompt: string;
  error?: string;
  details?: string;
}

interface AIResponse {
  success: boolean;
  message: string;
  aiResponse: string | null;
  integrationStatus: 'available' | 'unavailable';
  error?: string;
}

interface ProcessResponse {
  success: boolean;
  message: string;
  details: string;
  logs: string[];
  memoryUpdates: string[];
  filesToCommit: string[];
  error?: string;
}

export default function Home() {
  const adaptedTheme = useAdaptedTheme();
  const [prompt, setPrompt] = useState('');
  const [enhancedPrompt, setEnhancedPrompt] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSendingToAI, setIsSendingToAI] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'info' | 'success' | 'error'>('info');
  const [showManualInput, setShowManualInput] = useState(false);
  const [copied, setCopied] = useState(false);
  const [apiIntegrationAvailable, setApiIntegrationAvailable] = useState(false);
  const [processing, setProcessing] = useState({
    logs: [] as string[],
    memoryUpdates: [] as string[],
    filesToCommit: [] as string[]
  });

  // Check if API integration is available on component mount
  useEffect(() => {
    // Check if MCP integration is available
    const checkMcpAvailability = async () => {
      try {
        const response = await fetch('/api/mcp/status');
        const data = await response.json();
        
        setApiIntegrationAvailable(data.available);
        
        if (data.available) {
          setMessage('MCP integration detected! Direct integration is available.');
          setMessageType('success');
        } else {
          console.log('MCP not available:', data.message);
        }
      } catch (error) {
        console.error('Error checking MCP status:', error);
        setApiIntegrationAvailable(false);
      }
    };
    
    checkMcpAvailability();
  }, []);

  // Enhanced prompt handling with better error handling
  const enhancePrompt = async () => {
    if (!prompt.trim()) {
      setMessage('Please enter a prompt');
      setMessageType('error');
      return;
    }

    setIsEnhancing(true);
    setMessage('Enhancing prompt with God Mode...');
    setMessageType('info');
    
    try {
      let enhancedPromptText;
      
      // Try MCP first if available
      if (apiIntegrationAvailable) {
        const mcpResponse = await fetch('/api/mcp', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tool: 'god_mode.enhance',
            parameters: { prompt }
          })
        });
        
        const mcpData = await mcpResponse.json();
        
        if (mcpResponse.ok && mcpData.success) {
          enhancedPromptText = mcpData.result;
        } else {
          // Fallback to regular API if MCP failed
          console.warn('MCP enhancement failed, falling back to regular API:', mcpData.error || mcpData.message);
          throw new Error(mcpData.error || mcpData.message || 'MCP enhancement failed');
        }
      } else {
        // Use regular API if MCP is not available
        const response = await fetch('/api/enhance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt })
        });
        
        const data: EnhanceResponse = await response.json();
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to enhance prompt');
        }
        
        enhancedPromptText = data.enhancedPrompt;
      }
      
      setEnhancedPrompt(enhancedPromptText);
      setMessage('Prompt enhanced successfully! Attempting to send to AI...');
      setMessageType('success');
      
      // Automatically try to send to AI if direct integration is available
      if (apiIntegrationAvailable) {
        await sendToAI(enhancedPromptText);
      } else {
        setMessage('Prompt enhanced successfully! Copy it to use with Cursor AI.');
        setMessageType('success');
      }
      
    } catch (error) {
      console.error('Error enhancing prompt:', error);
      setMessage(`Error: ${error instanceof Error ? error.message : 'Failed to enhance prompt'}`);
      setMessageType('error');
    } finally {
      setIsEnhancing(false);
    }
  };

  // Send to AI directly (when API integration becomes available)
  const sendToAI = async (textToSend: string) => {
    setIsSendingToAI(true);
    setMessage('Sending to AI...');
    setMessageType('info');
    
    try {
      const response = await fetch('/api/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enhancedPrompt: textToSend })
      });
      
      const data: AIResponse = await response.json();
      
      if (data.integrationStatus === 'available' && data.aiResponse) {
        setAiResponse(data.aiResponse);
        setMessage('Received response from AI! Processing...');
        setMessageType('success');
        
        // Automatically process the response
        await processResponse(data.aiResponse);
      } else {
        setMessage('Direct AI integration not available. Please use manual input.');
        setMessageType('info');
        setShowManualInput(true);
      }
    } catch (error) {
      console.error('Error communicating with AI:', error);
      setMessage('Could not connect to AI. Please use manual input.');
      setMessageType('error');
      setShowManualInput(true);
    } finally {
      setIsSendingToAI(false);
    }
  };

  // Process the AI response
  const processResponse = async (responseToProcess?: string) => {
    const textToProcess = responseToProcess || aiResponse;
    
    if (!textToProcess.trim()) {
      setMessage('Please paste the AI response');
      setMessageType('error');
      return;
    }

    setIsProcessing(true);
    setMessage('Processing AI response...');
    setMessageType('info');
    
    try {
      let processResult;
      
      // Try MCP first if available
      if (apiIntegrationAvailable) {
        const mcpResponse = await fetch('/api/mcp', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tool: 'god_mode.process',
            parameters: { 
              response: textToProcess,
              prompt: prompt 
            }
          })
        });
        
        const mcpData = await mcpResponse.json();
        
        if (mcpResponse.ok && mcpData.success) {
          processResult = mcpData.result;
        } else {
          // Fallback to regular API if MCP failed
          console.warn('MCP processing failed, falling back to regular API:', mcpData.error || mcpData.message);
          throw new Error(mcpData.error || mcpData.message || 'MCP processing failed');
        }
      } else {
        // Use regular API if MCP is not available
        const response = await fetch('/api/process', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ aiResponse: textToProcess, prompt })
        });
        
        const data: ProcessResponse = await response.json();
        
        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Failed to process response');
        }
        
        processResult = data;
      }
      
      // Extract logs, memory updates, etc.
      setProcessing({
        logs: processResult.logs || [],
        memoryUpdates: processResult.memory_updates || processResult.memoryUpdates || [],
        filesToCommit: processResult.committed_files || processResult.filesToCommit || []
      });
      
      setMessage('Response processed successfully!');
      setMessageType('success');
    } catch (error) {
      console.error('Error processing response:', error);
      setMessage('Error processing response. Please try again.');
      setMessageType('error');
    } finally {
      setIsProcessing(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setMessage('Copied to clipboard!');
    setMessageType('success');
    
    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  const resetState = () => {
    setPrompt('');
    setEnhancedPrompt('');
    setAiResponse('');
    setMessage('');
    setShowManualInput(false);
    setProcessing({
      logs: [],
      memoryUpdates: [],
      filesToCommit: []
    });
  };

  // Style constants using theme tokens
  const containerStyle = {
    backgroundColor: adaptedTheme.colors.background,
    color: adaptedTheme.colors.foreground,
    fontFamily: adaptedTheme.typography.fonts.primary,
  };
  
  const cardStyle = {
    backgroundColor: adaptedTheme.colors.card,
    borderColor: adaptedTheme.colors.border,
    borderRadius: adaptedTheme.borderRadius.lg,
    boxShadow: adaptedTheme.shadows.md,
  };

  const buttonStyle = {
    backgroundColor: adaptedTheme.colors.primary.DEFAULT,
    color: adaptedTheme.colors.primary.foreground,
    padding: `${adaptedTheme.spacing.unit * 2}px ${adaptedTheme.spacing.unit * 4}px`,
    borderRadius: adaptedTheme.borderRadius.md,
    fontWeight: adaptedTheme.typography.fontWeights.medium,
    cursor: 'pointer',
  };
  
  const successButtonStyle = {
    ...buttonStyle,
    backgroundColor: adaptedTheme.colors.success.DEFAULT,
    color: adaptedTheme.colors.success.foreground,
  };

  const textareaStyle = {
    backgroundColor: adaptedTheme.colors.input,
    borderColor: adaptedTheme.colors.border,
    borderRadius: adaptedTheme.borderRadius.md,
    padding: adaptedTheme.spacing.unit * 3,
    fontFamily: adaptedTheme.typography.fonts.mono,
  };

  return (
    <main style={containerStyle} className="flex min-h-screen flex-col p-4 sm:p-6 md:p-12">
      <div className="w-full max-w-4xl mx-auto space-y-6">
        <header className="flex flex-col items-center justify-center mb-8">
          <h1 className="text-3xl font-bold mb-2">God Mode Web UI</h1>
          <p className="text-center opacity-70">Enhance your prompts and process AI responses</p>
        </header>

        {message && (
          <div 
            className={cn(
              "p-4 my-4 rounded-md flex items-center gap-2",
              messageType === 'error' ? 'bg-red-100 text-red-800 border border-red-200' : 
              messageType === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 
              'bg-blue-100 text-blue-800 border border-blue-200'
            )}
          >
            {messageType === 'error' && <AlertTriangle size={18} />}
            {messageType === 'success' && <Check size={18} />}
            {message}
          </div>
        )}

        <div className="space-y-6 border border-gray-200 rounded-lg shadow-sm" style={cardStyle}>
          <div className="p-6 space-y-4">
            <h2 className="text-xl font-semibold flex items-center">
              <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center mr-2">1</span>
              Enter your prompt
            </h2>
            <textarea
              style={textareaStyle}
              className="w-full h-32 resize-y"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              disabled={isEnhancing}
            />
            <button
              style={buttonStyle}
              className="w-full p-3 flex items-center justify-center gap-2 disabled:opacity-50"
              onClick={enhancePrompt}
              disabled={isEnhancing || !prompt.trim()}
            >
              {isEnhancing ? (
                <>
                  <Loader size={18} className="animate-spin" />
                  Enhancing...
                </>
              ) : (
                <>
                  <Send size={18} />
                  Enhance with God Mode
                </>
              )}
            </button>
          </div>
        </div>

        {enhancedPrompt && (
          <div className="space-y-6 border border-gray-200 rounded-lg shadow-sm" style={cardStyle}>
            <div className="p-6 space-y-4">
              <h2 className="text-xl font-semibold flex items-center">
                <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center mr-2">2</span>
                Enhanced prompt {isSendingToAI && "(Sending to AI...)"}
              </h2>
              <div className="relative">
                <textarea
                  style={textareaStyle}
                  className="w-full h-64 resize-y"
                  value={enhancedPrompt}
                  readOnly
                />
                <button
                  className="absolute right-2 top-2 p-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 flex items-center gap-1"
                  onClick={() => copyToClipboard(enhancedPrompt)}
                >
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
              
              {!apiIntegrationAvailable && (
                <div className="p-4 bg-yellow-100 border border-yellow-200 rounded-md text-yellow-800">
                  <p>While we work on direct API integration:</p>
                  <ol className="list-decimal pl-5 space-y-1 mt-2">
                    <li>Copy the enhanced prompt (button above)</li>
                    <li>Paste it into Cursor AI</li>
                    <li>Get the AI's response</li>
                    <li>Click "Manual input" below to paste the response</li>
                  </ol>
                </div>
              )}
              
              {apiIntegrationAvailable && (
                <button
                  style={buttonStyle}
                  className="w-full p-3 flex items-center justify-center gap-2 disabled:opacity-50"
                  onClick={() => sendToAI(enhancedPrompt)}
                  disabled={isSendingToAI}
                >
                  {isSendingToAI ? (
                    <>
                      <Loader size={18} className="animate-spin" />
                      Sending to AI...
                    </>
                  ) : (
                    <>
                      <ArrowRight size={18} />
                      Send to AI
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        )}

        {enhancedPrompt && (
          <div className="space-y-6 border border-gray-200 rounded-lg shadow-sm" style={cardStyle}>
            <div className="p-6 space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold flex items-center">
                  <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center mr-2">3</span>
                  {showManualInput ? "Paste AI response" : "AI response"}
                </h2>
                {!showManualInput && (
                  <button
                    onClick={() => setShowManualInput(true)}
                    className="flex items-center text-sm gap-1 text-orange-600"
                  >
                    <AlertTriangle size={14} />
                    Manual input
                  </button>
                )}
              </div>
              
              {showManualInput ? (
                <>
                  <textarea
                    style={textareaStyle}
                    className="w-full h-64 resize-y"
                    value={aiResponse}
                    onChange={(e) => setAiResponse(e.target.value)}
                    placeholder="Paste the AI's response here..."
                    disabled={isProcessing}
                  />
                  <button
                    style={successButtonStyle}
                    className="w-full p-3 flex items-center justify-center gap-2 disabled:opacity-50"
                    onClick={() => processResponse()}
                    disabled={isProcessing || !aiResponse.trim()}
                  >
                    {isProcessing ? (
                      <>
                        <Loader size={18} className="animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Check size={18} />
                        Process Response
                      </>
                    )}
                  </button>
                </>
              ) : (
                <div className="p-6 bg-gray-100 rounded-md text-center opacity-70 h-32 flex items-center justify-center">
                  <p>
                    {isSendingToAI ? 
                      "Waiting for response from AI..." : 
                      "Direct API integration coming soon! Use manual input for now."}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Results section - shown after processing */}
        {(processing.logs.length > 0 || processing.memoryUpdates.length > 0 || processing.filesToCommit.length > 0) && (
          <div className="space-y-6 border border-gray-200 rounded-lg shadow-sm" style={cardStyle}>
            <div className="p-6 space-y-4">
              <h2 className="text-xl font-semibold flex items-center">
                <span className="bg-green-100 text-green-800 w-6 h-6 rounded-full flex items-center justify-center mr-2">✓</span>
                Processing Results
              </h2>
              
              {processing.logs.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-medium">Logs Updated:</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {processing.logs.map((log, index) => (
                      <li key={index} className="text-sm font-mono">{log}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {processing.memoryUpdates.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-medium">Memory Files Updated:</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {processing.memoryUpdates.map((file, index) => (
                      <li key={index} className="text-sm font-mono">{file}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {processing.filesToCommit.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-medium">Files Committed:</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {processing.filesToCommit.map((file, index) => (
                      <li key={index} className="text-sm font-mono">{file}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <button
                style={{...buttonStyle, backgroundColor: adaptedTheme.colors.secondary.DEFAULT}}
                className="w-full p-3 flex items-center justify-center gap-2 mt-4"
                onClick={resetState}
              >
                <RefreshCw size={18} />
                New Prompt
              </button>
            </div>
          </div>
        )}

        <footer className="mt-8 pt-6 border-t border-gray-200 flex justify-between items-center text-sm opacity-70">
          <Link href="/history" className="text-blue-600 hover:underline">
            View History
          </Link>
          <span>
            God Mode Web UI v0.1.0
          </span>
        </footer>
      </div>
    </main>
  );
} 