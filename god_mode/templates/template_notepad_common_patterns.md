# Common Patterns and Best Practices

This document outlines the recurring code patterns and best practices used in the project codebase. Reference this document when implementing new features to maintain consistency.

## React Components

### Functional Component Template

```tsx
import React from 'react';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // Define props here
  title: string;
  children?: React.ReactNode;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  children,
}) => {
  // Component logic here
  
  return (
    <div className={styles.container}>
      <h2>{title}</h2>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
};
```

### Custom Hook Template

```tsx
import { useState, useEffect } from 'react';

interface UseFeatureOptions {
  initialValue: string;
  // Other options
}

interface UseFeatureResult {
  value: string;
  setValue: (newValue: string) => void;
  // Other return values
}

export function useFeature(options: UseFeatureOptions): UseFeatureResult {
  const { initialValue } = options;
  const [value, setValue] = useState(initialValue);
  
  useEffect(() => {
    // Effect logic here
    return () => {
      // Cleanup logic here
    };
  }, [/* dependencies */]);
  
  // Additional logic
  
  return {
    value,
    setValue,
    // Other return values
  };
}
```

### Context Provider Template

```tsx
import React, { createContext, useContext, useState } from 'react';

interface FeatureContextType {
  value: string;
  setValue: (newValue: string) => void;
}

const FeatureContext = createContext<FeatureContextType | undefined>(undefined);

interface FeatureProviderProps {
  initialValue?: string;
  children: React.ReactNode;
}

export const FeatureProvider: React.FC<FeatureProviderProps> = ({
  initialValue = '',
  children,
}) => {
  const [value, setValue] = useState(initialValue);
  
  return (
    <FeatureContext.Provider value={{ value, setValue }}>
      {children}
    </FeatureContext.Provider>
  );
};

export function useFeatureContext(): FeatureContextType {
  const context = useContext(FeatureContext);
  if (context === undefined) {
    throw new Error('useFeatureContext must be used within a FeatureProvider');
  }
  return context;
}
```

## API Patterns

### API Route Template

```ts
import type { NextApiRequest, NextApiResponse } from 'next';

type ResponseData = {
  message: string;
  data?: any;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  try {
    // Check HTTP method
    if (req.method !== 'POST') {
      return res.status(405).json({ message: 'Method not allowed' });
    }
    
    // Extract data from request
    const { param1, param2 } = req.body;
    
    // Validate input
    if (!param1 || !param2) {
      return res.status(400).json({ message: 'Missing required parameters' });
    }
    
    // Process the request
    const result = await processRequest(param1, param2);
    
    // Return success response
    return res.status(200).json({
      message: 'Success',
      data: result,
    });
  } catch (error) {
    console.error('API error:', error);
    return res.status(500).json({ message: 'Internal server error' });
  }
}

async function processRequest(param1: string, param2: string) {
  // Implementation here
  return { processed: true };
}
```

## Data Fetching Patterns

### React Query Template

```tsx
import { useQuery, useMutation, useQueryClient } from 'react-query';

// Fetch data
export function useGetData(id: string) {
  return useQuery(['data', id], async () => {
    const response = await fetch(`/api/data/${id}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  });
}

// Create data
export function useCreateData() {
  const queryClient = useQueryClient();
  
  return useMutation(
    async (newData: any) => {
      const response = await fetch('/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newData),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      return response.json();
    },
    {
      onSuccess: () => {
        // Invalidate and refetch
        queryClient.invalidateQueries('data');
      },
    }
  );
}
```

## Error Handling Patterns

### Try-Catch Pattern

```ts
async function fetchData() {
  try {
    // Attempt to fetch data
    const response = await fetch('/api/data');
    
    // Check if response is ok
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // Parse and return data
    const data = await response.json();
    return data;
  } catch (error) {
    // Log the error
    console.error('Error fetching data:', error);
    
    // Rethrow or handle appropriately
    throw new Error('Failed to fetch data. Please try again later.');
  }
}
```

### Error Boundary Component

```tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  fallback?: ReactNode;
  children: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log the error
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    
    // Call onError callback if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      // Render fallback UI if provided, otherwise render a default error message
      return this.props.fallback || (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <p>Please try again or contact support if the problem persists.</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Testing Patterns

### Component Test Template

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly with props', () => {
    render(<ComponentName title="Test Title" />);
    
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });
  
  it('handles user interactions', () => {
    const handleClick = jest.fn();
    render(<ComponentName title="Test Title" onClick={handleClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Hook Test Template

```tsx
import { renderHook, act } from '@testing-library/react-hooks';
import { useFeature } from './useFeature';

describe('useFeature', () => {
  it('initializes with the provided value', () => {
    const { result } = renderHook(() => useFeature({ initialValue: 'test' }));
    
    expect(result.current.value).toBe('test');
  });
  
  it('updates value when setValue is called', () => {
    const { result } = renderHook(() => useFeature({ initialValue: 'test' }));
    
    act(() => {
      result.current.setValue('updated');
    });
    
    expect(result.current.value).toBe('updated');
  });
});
```

---

*This document provides common patterns used in the project codebase. Adapt them as needed for specific implementation requirements while maintaining consistency.* 