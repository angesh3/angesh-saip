import React from 'react';

interface LogoProps {
  className?: string;
  size?: number;
}

export const Logo: React.FC<LogoProps> = ({ className = '', size = 40 }) => {
  return (
    <div className={`inline-flex items-center ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="flex-shrink-0"
      >
        {/* Shield Base */}
        <path
          d="M20 2L8 7V17C8 26.2843 13.1634 31 20 35C26.8366 31 32 26.2843 32 17V7L20 2Z"
          fill="#2563EB"
          className="transition-colors"
        />
        
        {/* Data Visualization Lines */}
        <path
          d="M16 20L19 17L22 22L25 15"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        
        {/* Lock Circle */}
        <circle
          cx="20"
          cy="19"
          r="6"
          stroke="white"
          strokeWidth="2"
          fill="none"
        />
      </svg>
      <span className="ml-2 text-xl font-semibold text-gray-900 dark:text-white">
        SAIP
      </span>
    </div>
  );
};

export default Logo; 