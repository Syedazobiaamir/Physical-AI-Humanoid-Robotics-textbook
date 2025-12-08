import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from './AuthContext';

interface UserMenuProps {
  onSignInClick?: () => void;
}

export function UserMenu({ onSignInClick }: UserMenuProps) {
  const { user, isAuthenticated, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!isAuthenticated || !user) {
    return (
      <button className="signin-btn" onClick={onSignInClick}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
          <polyline points="10 17 15 12 10 7" />
          <line x1="15" y1="12" x2="3" y2="12" />
        </svg>
        <span>Sign In</span>

        <style>{`
          .signin-btn {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--ifm-color-primary, #2e8555);
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
          }

          .signin-btn:hover {
            background: var(--ifm-color-primary-dark, #257347);
            transform: translateY(-1px);
          }
        `}</style>
      </button>
    );
  }

  const initials = user.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="user-menu" ref={menuRef}>
      <button
        className="user-menu-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {user.avatar_url ? (
          <img src={user.avatar_url} alt={user.name} className="user-avatar" />
        ) : (
          <div className="user-avatar-fallback">{initials}</div>
        )}
        <svg
          className={`chevron ${isOpen ? 'open' : ''}`}
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {isOpen && (
        <div className="user-menu-dropdown">
          <div className="user-info">
            {user.avatar_url ? (
              <img src={user.avatar_url} alt={user.name} className="dropdown-avatar" />
            ) : (
              <div className="dropdown-avatar-fallback">{initials}</div>
            )}
            <div className="user-details">
              <span className="user-name">{user.name}</span>
              <span className="user-email">{user.email}</span>
              <span className={`user-role role-${user.role}`}>{user.role}</span>
            </div>
          </div>

          {(user.software_background || user.hardware_background) && (
            <div className="skill-badges">
              {user.software_background && (
                <span className="skill-badge">
                  <span className="badge-icon">💻</span>
                  SW: {user.software_background}
                </span>
              )}
              {user.hardware_background && (
                <span className="skill-badge">
                  <span className="badge-icon">🔧</span>
                  HW: {user.hardware_background}
                </span>
              )}
            </div>
          )}

          <div className="menu-divider" />

          <button className="menu-item" onClick={logout}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            <span>Sign Out</span>
          </button>
        </div>
      )}

      <style>{`
        .user-menu {
          position: relative;
        }

        .user-menu-trigger {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.25rem;
          background: transparent;
          border: none;
          cursor: pointer;
          border-radius: 24px;
          transition: background 0.2s;
        }

        .user-menu-trigger:hover {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
        }

        .user-avatar, .user-avatar-fallback {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          object-fit: cover;
        }

        .user-avatar-fallback {
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--ifm-color-primary, #2e8555), var(--ifm-color-primary-dark, #257347));
          color: white;
          font-size: 0.875rem;
          font-weight: 600;
        }

        .chevron {
          color: var(--ifm-color-emphasis-600, #666);
          transition: transform 0.2s;
        }

        .chevron.open {
          transform: rotate(180deg);
        }

        .user-menu-dropdown {
          position: absolute;
          top: calc(100% + 8px);
          right: 0;
          width: 280px;
          background: var(--ifm-background-color, #fff);
          border-radius: 12px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
          border: 1px solid var(--ifm-color-emphasis-200, #eee);
          z-index: 1000;
          animation: fadeIn 0.2s ease-out;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(-8px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .user-info {
          display: flex;
          align-items: center;
          gap: 0.875rem;
          padding: 1rem;
        }

        .dropdown-avatar, .dropdown-avatar-fallback {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          object-fit: cover;
          flex-shrink: 0;
        }

        .dropdown-avatar-fallback {
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--ifm-color-primary, #2e8555), var(--ifm-color-primary-dark, #257347));
          color: white;
          font-size: 1rem;
          font-weight: 600;
        }

        .user-details {
          display: flex;
          flex-direction: column;
          gap: 0.125rem;
          overflow: hidden;
        }

        .user-name {
          font-weight: 600;
          color: var(--ifm-font-color-base, #333);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .user-email {
          font-size: 0.8rem;
          color: var(--ifm-color-emphasis-600, #666);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .user-role {
          display: inline-block;
          font-size: 0.7rem;
          font-weight: 500;
          text-transform: uppercase;
          padding: 0.125rem 0.5rem;
          border-radius: 10px;
          width: fit-content;
          margin-top: 0.25rem;
        }

        .role-student {
          background: #dbeafe;
          color: #1e40af;
        }

        .role-author {
          background: #fef3c7;
          color: #92400e;
        }

        .role-admin {
          background: #fce7f3;
          color: #9d174d;
        }

        .skill-badges {
          display: flex;
          gap: 0.5rem;
          padding: 0 1rem 0.75rem;
          flex-wrap: wrap;
        }

        .skill-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          font-size: 0.75rem;
          padding: 0.25rem 0.5rem;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          border-radius: 6px;
          color: var(--ifm-color-emphasis-700, #555);
        }

        .badge-icon {
          font-size: 0.875rem;
        }

        .menu-divider {
          height: 1px;
          background: var(--ifm-color-emphasis-200, #eee);
          margin: 0;
        }

        .menu-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          width: 100%;
          padding: 0.875rem 1rem;
          background: transparent;
          border: none;
          cursor: pointer;
          color: var(--ifm-font-color-base, #333);
          font-size: 0.9rem;
          transition: background 0.2s;
          text-align: left;
        }

        .menu-item:hover {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
        }

        .menu-item:last-child {
          border-radius: 0 0 12px 12px;
        }

        .menu-item svg {
          color: var(--ifm-color-emphasis-600, #666);
        }
      `}</style>
    </div>
  );
}

export default UserMenu;
