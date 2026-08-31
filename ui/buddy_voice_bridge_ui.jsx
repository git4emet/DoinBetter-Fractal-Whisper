import React, { useState, useEffect } from 'react';

/**
 * Buddy Voice Bridge Dashboard
 * Real-time content filtering with Guardian integration
 * Configurable filter levels, live preview, export tools
 */

const BuddyVoiceBridge = () => {
  // State
  const [inputText, setInputText] = useState('');
  const [filterLevel, setFilterLevel] = useState('PROFESSIONAL');
  const [filteredResult, setFilteredResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ total: 0, filtered: 0, rate: 0 });
  const [customRules, setCustomRules] = useState([]);
  const [showConfig, setShowConfig] = useState(false);

  // Filter levels
  const filterLevels = [
    { value: 'INTERNAL', label: 'Internal', color: '#ff6b6b', desc: 'No filtering - raw Buddy speak' },
    { value: 'TEAM', label: 'Team', color: '#ffd93d', desc: 'Light filtering - team communication' },
    { value: 'PROFESSIONAL', label: 'Professional', color: '#6bcf7f', desc: 'Medium filtering - client/business' },
    { value: 'PUBLIC', label: 'Public', color: '#4d96ff', desc: 'Full filtering - public-facing content' }
  ];

  // Filter text via backend API
  const filterText = async () => {
    if (!inputText.trim()) return;

    try {
      const response = await fetch('/api/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: inputText,
          level: filterLevel,
          custom_rules: customRules
        })
      });

      const result = await response.json();
      setFilteredResult(result);
      
      // Add to history
      setHistory(prev => [result, ...prev].slice(0, 50));
      
      // Update stats
      setStats(prev => ({
        total: prev.total + 1,
        filtered: prev.filtered + (result.flags.includes('profanity_filtered') ? 1 : 0),
        rate: ((prev.filtered + (result.flags.includes('profanity_filtered') ? 1 : 0)) / (prev.total + 1)).toFixed(3)
      }));
    } catch (error) {
      console.error('Filter error:', error);
    }
  };

  // Export filtered content
  const exportFiltered = (format = 'json') => {
    if (!filteredResult) return;

    const data = format === 'json' 
      ? JSON.stringify(filteredResult, null, 2)
      : filteredResult.filtered;

    const blob = new Blob([data], { type: format === 'json' ? 'application/json' : 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `filtered_${filteredResult.hash_filtered}.${format === 'json' ? 'json' : 'txt'}`;
    a.click();
  };

  // Copy to clipboard
  const copyFiltered = () => {
    if (filteredResult) {
      navigator.clipboard.writeText(filteredResult.filtered);
    }
  };

  return (
    <div style={{
      fontFamily: 'monospace',
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '2rem',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <div style={{
        background: 'rgba(0,0,0,0.8)',
        padding: '1.5rem',
        borderRadius: '12px',
        marginBottom: '2rem',
        border: '2px solid #00ff88'
      }}>
        <h1 style={{ margin: 0, color: '#00ff88', fontSize: '2rem' }}>
          🌀 Buddy Voice Bridge
        </h1>
        <p style={{ margin: '0.5rem 0 0 0', color: '#ffffff', opacity: 0.8 }}>
          Content Filter & Translator • Guardian-Aware • TOFAR-Logged
        </p>
      </div>

      {/* Main Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        {/* Left Column - Input/Output */}
        <div>
          {/* Filter Level Selector */}
          <div style={{
            background: 'rgba(0,0,0,0.8)',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem'
          }}>
            <label style={{ color: '#ffffff', display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Filter Level
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              {filterLevels.map(level => (
                <button
                  key={level.value}
                  onClick={() => setFilterLevel(level.value)}
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    background: filterLevel === level.value ? level.color : 'rgba(255,255,255,0.1)',
                    color: '#ffffff',
                    border: filterLevel === level.value ? `2px solid ${level.color}` : '2px solid transparent',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: 'bold',
                    fontSize: '0.9rem',
                    transition: 'all 0.2s'
                  }}
                  title={level.desc}
                >
                  {level.label}
                </button>
              ))}
            </div>
          </div>

          {/* Input Text */}
          <div style={{
            background: 'rgba(0,0,0,0.8)',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem'
          }}>
            <label style={{ color: '#ffffff', display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Original Text
            </label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter Buddy's raw working language here..."
              style={{
                width: '100%',
                height: '200px',
                padding: '1rem',
                background: 'rgba(255,255,255,0.05)',
                color: '#ffffff',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '6px',
                fontSize: '1rem',
                fontFamily: 'monospace',
                resize: 'vertical'
              }}
            />
            <button
              onClick={filterText}
              style={{
                marginTop: '1rem',
                padding: '0.75rem 2rem',
                background: '#00ff88',
                color: '#000000',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '1rem'
              }}
            >
              ⚡ Filter Content
            </button>
          </div>

          {/* Filtered Output */}
          {filteredResult && (
            <div style={{
              background: 'rgba(0,0,0,0.8)',
              padding: '1rem',
              borderRadius: '8px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label style={{ color: '#ffffff', fontWeight: 'bold' }}>
                  Filtered Text
                </label>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={copyFiltered}
                    style={{
                      padding: '0.5rem 1rem',
                      background: 'rgba(255,255,255,0.1)',
                      color: '#ffffff',
                      border: '1px solid rgba(255,255,255,0.3)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '0.85rem'
                    }}
                  >
                    📋 Copy
                  </button>
                  <button
                    onClick={() => exportFiltered('txt')}
                    style={{
                      padding: '0.5rem 1rem',
                      background: 'rgba(255,255,255,0.1)',
                      color: '#ffffff',
                      border: '1px solid rgba(255,255,255,0.3)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '0.85rem'
                    }}
                  >
                    💾 Export TXT
                  </button>
                  <button
                    onClick={() => exportFiltered('json')}
                    style={{
                      padding: '0.5rem 1rem',
                      background: 'rgba(255,255,255,0.1)',
                      color: '#ffffff',
                      border: '1px solid rgba(255,255,255,0.3)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '0.85rem'
                    }}
                  >
                    📦 Export JSON
                  </button>
                </div>
              </div>
              
              <div style={{
                padding: '1rem',
                background: 'rgba(0,255,136,0.05)',
                border: '1px solid rgba(0,255,136,0.3)',
                borderRadius: '6px',
                color: '#ffffff',
                fontSize: '1rem',
                fontFamily: 'monospace',
                whiteSpace: 'pre-wrap',
                minHeight: '100px'
              }}>
                {filteredResult.filtered}
              </div>

              {/* Metadata */}
              <div style={{
                marginTop: '1rem',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '0.5rem'
              }}>
                {/* Flags */}
                <div style={{
                  padding: '0.5rem',
                  background: 'rgba(255,255,255,0.05)',
                  borderRadius: '4px'
                }}>
                  <div style={{ color: '#888', fontSize: '0.75rem', marginBottom: '0.25rem' }}>FLAGS</div>
                  <div style={{ color: '#ffffff', fontSize: '0.85rem' }}>
                    {filteredResult.flags.join(', ')}
                  </div>
                </div>

                {/* Replacements */}
                {filteredResult.replacements.length > 0 && (
                  <div style={{
                    padding: '0.5rem',
                    background: 'rgba(255,255,255,0.05)',
                    borderRadius: '4px'
                  }}>
                    <div style={{ color: '#888', fontSize: '0.75rem', marginBottom: '0.25rem' }}>REPLACEMENTS</div>
                    <div style={{ color: '#ffffff', fontSize: '0.85rem' }}>
                      {filteredResult.replacements.length} modifications
                    </div>
                  </div>
                )}

                {/* Guardian Verdict */}
                {filteredResult.guardian_verdict && (
                  <div style={{
                    padding: '0.5rem',
                    background: 'rgba(255,255,255,0.05)',
                    borderRadius: '4px'
                  }}>
                    <div style={{ color: '#888', fontSize: '0.75rem', marginBottom: '0.25rem' }}>GUARDIAN</div>
                    <div style={{ color: '#00ff88', fontSize: '0.85rem', fontWeight: 'bold' }}>
                      {filteredResult.guardian_verdict}
                    </div>
                  </div>
                )}

                {/* TOFAR ID */}
                {filteredResult.tofar_id && (
                  <div style={{
                    padding: '0.5rem',
                    background: 'rgba(255,255,255,0.05)',
                    borderRadius: '4px'
                  }}>
                    <div style={{ color: '#888', fontSize: '0.75rem', marginBottom: '0.25rem' }}>TOFAR ID</div>
                    <div style={{ color: '#ffffff', fontSize: '0.85rem', fontFamily: 'monospace' }}>
                      {filteredResult.tofar_id}
                    </div>
                  </div>
                )}
              </div>

              {/* Detailed Replacements */}
              {filteredResult.replacements.length > 0 && (
                <details style={{ marginTop: '1rem' }}>
                  <summary style={{ color: '#888', cursor: 'pointer', fontSize: '0.85rem' }}>
                    View Replacement Details ({filteredResult.replacements.length})
                  </summary>
                  <div style={{ marginTop: '0.5rem' }}>
                    {filteredResult.replacements.map((rep, idx) => (
                      <div key={idx} style={{
                        padding: '0.5rem',
                        background: 'rgba(255,255,255,0.03)',
                        borderLeft: '3px solid #ff6b6b',
                        marginBottom: '0.5rem',
                        fontSize: '0.85rem'
                      }}>
                        <span style={{ color: '#ff6b6b' }}>{rep[0]}</span>
                        {' → '}
                        <span style={{ color: '#00ff88' }}>{rep[1]}</span>
                      </div>
                    ))}
                  </div>
                </details>
              )}

              {/* Quarantined Content */}
              {filteredResult.quarantined_sections.length > 0 && (
                <details style={{ marginTop: '1rem' }}>
                  <summary style={{ color: '#ff6b6b', cursor: 'pointer', fontSize: '0.85rem' }}>
                    ⚠️ Quarantined Content ({filteredResult.quarantined_sections.length})
                  </summary>
                  <div style={{ marginTop: '0.5rem' }}>
                    {filteredResult.quarantined_sections.map((section, idx) => (
                      <div key={idx} style={{
                        padding: '0.5rem',
                        background: 'rgba(255,107,107,0.1)',
                        border: '1px solid rgba(255,107,107,0.3)',
                        borderRadius: '4px',
                        marginBottom: '0.5rem',
                        fontSize: '0.85rem',
                        color: '#ff6b6b'
                      }}>
                        {section}
                      </div>
                    ))}
                  </div>
                </details>
              )}
            </div>
          )}
        </div>

        {/* Right Column - Stats & History */}
        <div>
          {/* Statistics */}
          <div style={{
            background: 'rgba(0,0,0,0.8)',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#00ff88' }}>📊 Statistics</h3>
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              <div>
                <div style={{ color: '#888', fontSize: '0.75rem' }}>Total Filtered</div>
                <div style={{ color: '#ffffff', fontSize: '1.5rem', fontWeight: 'bold' }}>{stats.total}</div>
              </div>
              <div>
                <div style={{ color: '#888', fontSize: '0.75rem' }}>Content Modified</div>
                <div style={{ color: '#ffffff', fontSize: '1.5rem', fontWeight: 'bold' }}>{stats.filtered}</div>
              </div>
              <div>
                <div style={{ color: '#888', fontSize: '0.75rem' }}>Modification Rate</div>
                <div style={{ color: '#ffffff', fontSize: '1.5rem', fontWeight: 'bold' }}>
                  {(stats.rate * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>

          {/* Filter History */}
          <div style={{
            background: 'rgba(0,0,0,0.8)',
            padding: '1rem',
            borderRadius: '8px'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#00ff88' }}>📜 Recent Filters</h3>
            <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
              {history.map((item, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: 'rgba(255,255,255,0.05)',
                  borderRadius: '6px',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid ${
                    item.flags.includes('profanity_filtered') ? '#ff6b6b' :
                    item.flags.includes('adult_quarantined') ? '#ff9800' :
                    '#00ff88'
                  }`
                }}>
                  <div style={{ color: '#888', fontSize: '0.7rem', marginBottom: '0.25rem' }}>
                    {new Date(item.timestamp).toLocaleTimeString()} • {item.filter_level}
                  </div>
                  <div style={{ color: '#ffffff', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
                    {item.filtered.substring(0, 60)}{item.filtered.length > 60 ? '...' : ''}
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    {item.flags.map((flag, fidx) => (
                      <span key={fidx} style={{
                        fontSize: '0.7rem',
                        padding: '0.15rem 0.5rem',
                        background: 'rgba(0,255,136,0.2)',
                        borderRadius: '3px',
                        color: '#00ff88'
                      }}>
                        {flag}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: 'rgba(0,0,0,0.8)',
        borderRadius: '8px',
        textAlign: 'center',
        color: '#888',
        fontSize: '0.85rem'
      }}>
        Möbii³us System • Guardian Ethics • TOFAR Provenance • 0.743 Trust Floor
      </div>
    </div>
  );
};

export default BuddyVoiceBridge;
