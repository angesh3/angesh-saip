import React from 'react';
import Logo from '../ui/logo';

export function TopNav() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <Logo className="mr-6" />
        <nav className="flex flex-1 items-center space-x-6 text-sm font-medium">
          <a href="/dashboard" className="transition-colors hover:text-foreground/80">Dashboard</a>
          <a href="/alerts" className="transition-colors hover:text-foreground/80">Alerts</a>
          <a href="/access-logs" className="transition-colors hover:text-foreground/80">Access Logs</a>
          <a href="/settings" className="transition-colors hover:text-foreground/80">Settings</a>
        </nav>
        <div className="flex items-center space-x-4">
          <button className="text-sm font-medium transition-colors hover:text-foreground/80">
            Profile
          </button>
        </div>
      </div>
    </header>
  );
}

export default TopNav; 