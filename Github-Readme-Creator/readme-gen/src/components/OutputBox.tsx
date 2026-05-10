import { useState } from 'react'

interface OutputBoxProps {
  output: string
  onClear: () => void
}

export default function OutputBox({ output, onClear }: OutputBoxProps) {
  const [copied, setCopied] = useState(false)

  const copy = async () => {
    await navigator.clipboard.writeText(output)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <section className="output-area" aria-label="Generated README output">
      <div className="output-label-row">
        <span className="output-label">output</span>
        {output && (
          <div className="output-actions">
            {/* Top-right actions: only Clear button here for the clean look */}
            <button className="icon-btn" onClick={onClear} aria-label="Clear output">
              <XIcon />
              <span>clear</span>
            </button>
          </div>
        )}
      </div>

      <div className="output-box" aria-live="polite">
        {output ? (
          <div className="output-inner-container">
            {/* Rendered Markdown Area */}
            <div 
              className="markdown-content"
              dangerouslySetInnerHTML={{ __html: renderMarkdown(output) }}
            />
            
            {/* Dedicated Copy Button at the bottom (Icon only) */}
            <div className="copy-footer">
              <button 
                className={`copy-btn-icon-only ${copied ? 'copied' : ''}`} 
                onClick={copy} 
                title="Copy Markdown"
              >
                {copied ? <CheckIcon /> : <CopyIcon />}
              </button>
            </div>
          </div>
        ) : (
          <div className="output-placeholder">
            <FileIcon />
            <span>your readme will appear here</span>
          </div>
        )}
      </div>
    </section>
  )
}

function renderMarkdown(markdown: string): string {
  // Handle code blocks - fixed regex escaping
  let html = markdown.replace(/```(?:\w+)?([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

  html = html
    // Headers
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    
    // Bold and Inline Code
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    
    // Links
    .replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    
    // Unordered lists
    .replace(/^\*\s+(.*)$/gim, '<li>$1</li>')
    .replace(/^-\s+(.*)$/gim, '<li>$1</li>')
    
    // Numbered lists
    .replace(/^(\d+\.)\s+(.*)$/gim, '<li>$1 $2</li>');

  // Wrap list items in ul tags
  html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');

  // Handle paragraphs
  return html.split(/\n\n+/).map((para: string): string => {
    const trimmed = para.trim();
    if (!trimmed) return '';
    
    // Skip wrapping for HTML elements
    if (/^<(h\d|ul|pre|code)/i.test(trimmed)) {
      return trimmed;
    }
    
    return `<p>${trimmed.replace(/\n/g, '<br />')}</p>`;
  }).join('\n');
}

// --- Icons ---

function CopyIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></svg>
  )
}

function CheckIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4caf50" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>
  )
}

function XIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
  )
}

function FileIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#AFA9EC" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><polyline points="10 9 9 9 8 9" /></svg>
  )
}