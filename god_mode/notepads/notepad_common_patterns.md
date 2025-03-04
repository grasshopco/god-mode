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
  // Options for the hook
  initialValue?: string;
  dependencyValue?: number;
}

interface UseFeatureResult {
  // Return values from the hook
  value: string;
  updateValue: (newValue: string) => void;
  isLoading: boolean;
  error: Error | null;
}

export function useFeature({
  initialValue = '',
  dependencyValue = 0,
}: UseFeatureOptions = {}): UseFeatureResult {
  const [value, setValue] = useState(initialValue);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Effect logic here
    
    return () => {
      // Cleanup logic here
    };
  }, [dependencyValue]);

  const updateValue = (newValue: string) => {
    setValue(newValue);
  };

  return {
    value,
    updateValue,
    isLoading,
    error,
  };
}
```

## Data Fetching

### Supabase Query Pattern

```tsx
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export function useSupabaseQuery<T>(
  tableName: string,
  queryBuilder: (query: any) => any,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        let query = supabase.from(tableName).select('*');
        query = queryBuilder(query);

        const { data, error } = await query;

        if (error) throw error;
        setData(data);
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [...dependencies]);

  return { data, error, isLoading };
}

// Usage example:
// const { data, error, isLoading } = useSupabaseQuery(
//   'users',
//   (query) => query.eq('role', 'admin').order('created_at', { ascending: false }),
//   [role]
// );
```

### Mutation Pattern

```tsx
import { useState } from 'react';
import { supabase } from '@/lib/supabase';

export function useSupabaseMutation<T, I>(
  tableName: string,
  options: {
    onSuccess?: (data: T) => void;
    onError?: (error: Error) => void;
  } = {}
) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const mutate = async (item: I) => {
    try {
      setIsLoading(true);
      setError(null);

      const { data, error } = await supabase
        .from(tableName)
        .insert(item)
        .select()
        .single();

      if (error) throw error;
      
      if (options.onSuccess) {
        options.onSuccess(data);
      }
      
      return data;
    } catch (error) {
      setError(error as Error);
      
      if (options.onError) {
        options.onError(error as Error);
      }
      
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    mutate,
    isLoading,
    error,
  };
}

// Usage example:
// const { mutate, isLoading } = useSupabaseMutation('todos', {
//   onSuccess: (data) => {
//     console.log('Todo created:', data);
//     router.push('/todos');
//   }
// });
// 
// const handleSubmit = (e) => {
//   e.preventDefault();
//   mutate({ title, description, user_id: currentUser.id });
// };
```

## Error Handling

### API Error Handling Pattern

```tsx
// api/someEndpoint.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { supabase } from '@/lib/supabase';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Validate request
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' });
    }

    const { id } = req.body;
    
    if (!id) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Process request
    const { data, error } = await supabase
      .from('some_table')
      .select('*')
      .eq('id', id)
      .single();

    if (error) {
      // Log detailed error for debugging
      console.error('Supabase error:', error);
      
      // Return appropriate status code based on error
      if (error.code === 'PGRST116') {
        return res.status(404).json({ error: 'Item not found' });
      }
      
      return res.status(500).json({ error: 'Database error occurred' });
    }

    // Return successful response
    return res.status(200).json({ data });
  } catch (error) {
    // Log uncaught errors
    console.error('Unexpected error:', error);
    
    // Return generic error to client
    return res.status(500).json({ error: 'An unexpected error occurred' });
  }
}
```

### Client-Side Error Handling

```tsx
import { useState } from 'react';
import { ErrorMessage } from '@/components/ErrorMessage';

export function MyComponent() {
  const [error, setError] = useState<string | null>(null);

  const handleAction = async () => {
    try {
      setError(null);
      // Perform action that might throw
      const response = await fetch('/api/someEndpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ /* data */ }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'An error occurred');
      }

      // Process successful response
      const data = await response.json();
      // Do something with data
    } catch (err) {
      // Set user-friendly error message
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    }
  };

  return (
    <div>
      {error && <ErrorMessage message={error} />}
      <button onClick={handleAction}>Perform Action</button>
    </div>
  );
}
```

## State Management

### Context Provider Pattern

```tsx
// contexts/FeatureContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface FeatureContextValue {
  // Context values
  featureData: any[];
  isLoading: boolean;
  error: Error | null;
  refreshData: () => Promise<void>;
}

const FeatureContext = createContext<FeatureContextValue | undefined>(undefined);

export function FeatureProvider({ children }: { children: React.ReactNode }) {
  const [featureData, setFeatureData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Fetch data logic
      const response = await fetch('/api/feature-data');
      
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      
      const data = await response.json();
      setFeatureData(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('An unknown error occurred'));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const refreshData = async () => {
    await fetchData();
  };

  const value = {
    featureData,
    isLoading,
    error,
    refreshData,
  };

  return (
    <FeatureContext.Provider value={value}>
      {children}
    </FeatureContext.Provider>
  );
}

export function useFeature() {
  const context = useContext(FeatureContext);
  
  if (context === undefined) {
    throw new Error('useFeature must be used within a FeatureProvider');
  }
  
  return context;
}

// Usage:
// In _app.tsx:
// <FeatureProvider>
//   <Component {...pageProps} />
// </FeatureProvider>
//
// In components:
// const { featureData, isLoading, refreshData } = useFeature();
```

## Form Handling

### Form Validation Pattern

```tsx
import { useState } from 'react';

interface FormValues {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

export function LoginForm() {
  const [values, setValues] = useState<FormValues>({
    email: '',
    password: '',
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    // Email validation
    if (!values.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(values.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    // Password validation
    if (!values.password) {
      newErrors.password = 'Password is required';
    } else if (values.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      setIsSubmitting(true);
      
      // Submit form logic here
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Login failed');
      }
      
      // Handle successful login
      // e.g., redirect, update auth state, etc.
    } catch (error) {
      // Handle error
      console.error('Login error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={values.email}
          onChange={handleChange}
        />
        {errors.email && <p className="error">{errors.email}</p>}
      </div>
      
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={values.password}
          onChange={handleChange}
        />
        {errors.password && <p className="error">{errors.password}</p>}
      </div>
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log in'}
      </button>
    </form>
  );
}
```

## Testing Patterns

### Component Testing Template

```tsx
// ComponentName.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders without crashing', () => {
    render(<ComponentName title="Test Title" />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('renders children correctly', () => {
    render(
      <ComponentName title="Test Title">
        <p>Test Content</p>
      </ComponentName>
    );
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('handles user interaction correctly', () => {
    const handleClick = jest.fn();
    render(
      <ComponentName title="Test Title">
        <button onClick={handleClick}>Click Me</button>
      </ComponentName>
    );
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Hook Testing Template

```tsx
// useFeature.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useFeature } from './useFeature';

describe('useFeature', () => {
  it('initializes with default values', () => {
    const { result } = renderHook(() => useFeature());
    
    expect(result.current.value).toBe('');
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('updates value when updateValue is called', () => {
    const { result } = renderHook(() => useFeature());
    
    act(() => {
      result.current.updateValue('new value');
    });
    
    expect(result.current.value).toBe('new value');
  });

  it('accepts and uses initialValue', () => {
    const { result } = renderHook(() => useFeature({ initialValue: 'initial' }));
    expect(result.current.value).toBe('initial');
  });
});
```

---

*This document provides common patterns used in the project codebase. Adapt them as needed for specific implementation requirements while maintaining consistency.* 