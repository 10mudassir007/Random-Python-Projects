import { useState } from 'react'
import type { Config } from '../App'

interface SidebarProps {
  config: Config
  onConfigChange: (c: Config) => void
}

export default function Sidebar({ config, onConfigChange }: SidebarProps) {
  const [tokenOpen, setTokenOpen] = useState(false)

  const set = (patch: Partial<Config>) =>
    onConfigChange({ ...config, ...patch })

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-name">
          readme<span className="brand-dot">.</span>gen
        </span>
        <span className="brand-sub">github readme generator</span>
      </div>

      <div className="token-section">
        <button
          className={`token-toggle ${tokenOpen ? 'open' : ''}`}
          onClick={() => setTokenOpen((v) => !v)}
          aria-expanded={tokenOpen}
          aria-controls="token-panel"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <span>github token</span>
          
          <svg
            className="chevron"
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>

        <div
          id="token-panel"
          className={`token-panel ${tokenOpen ? 'open' : ''}`}
        >
          <input
            className="sidebar-input"
            type="password"
            placeholder="ghp_xxxxxxxxxxxx"
            value={config.token}
            onChange={(e) => set({ token: e.target.value })}
            autoComplete="off"
            aria-label="GitHub personal access token"
          />
          <p className="token-hint">
            optional — for private repos or to avoid rate limits
          </p>
        </div>
      </div>

      <div className="sidebar-spacer" />

      <p className="sidebar-footer">
        calls <code>POST /generate</code>
        <br />
        with url + optional token
      </p>
    </aside>
  )
}
