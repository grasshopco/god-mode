# React Component Template

Use this template when creating new React components for the Grasshop project.

## Basic Component

```tsx
import React from 'react';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // Define props here
  label: string;
  onClick?: () => void;
  disabled?: boolean;
  children?: React.ReactNode;
}

/**
 * ComponentName - Brief description of the component
 * 
 * Detailed description of the component's purpose and usage.
 * Include any important notes or considerations.
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  label,
  onClick,
  disabled = false,
  children,
}) => {
  // Component logic here
  
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{label}</h2>
      <button 
        className={styles.button}
        onClick={onClick}
        disabled={disabled}
      >
        Click me
      </button>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
};
```

## Component with State

```tsx
import React, { useState, useEffect } from 'react';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // Define props here
  initialValue?: string;
  onChange?: (value: string) => void;
}

/**
 * ComponentName - Brief description of the component
 * 
 * Detailed description of the component's purpose and usage.
 * Include any important notes or considerations.
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  initialValue = '',
  onChange,
}) => {
  // State
  const [value, setValue] = useState(initialValue);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  // Effects
  useEffect(() => {
    // Effect logic here
    
    return () => {
      // Cleanup logic here
    };
  }, []);
  
  // Event handlers
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    
    if (onChange) {
      onChange(newValue);
    }
  };
  
  // Render
  return (
    <div className={styles.container}>
      {isLoading && <div className={styles.loader}>Loading...</div>}
      
      {error && (
        <div className={styles.error}>
          Error: {error.message}
        </div>
      )}
      
      <input
        type="text"
        value={value}
        onChange={handleChange}
        className={styles.input}
      />
    </div>
  );
};
```

## Component with Context

```tsx
import React, { useContext } from 'react';
import { SomeContext } from '@/contexts/SomeContext';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // Define props here
  label: string;
}

/**
 * ComponentName - Brief description of the component
 * 
 * Detailed description of the component's purpose and usage.
 * Include any important notes or considerations.
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  label,
}) => {
  // Use context
  const { someValue, someFunction } = useContext(SomeContext);
  
  // Event handlers
  const handleClick = () => {
    someFunction();
  };
  
  // Render
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{label}</h2>
      <div className={styles.value}>{someValue}</div>
      <button 
        className={styles.button}
        onClick={handleClick}
      >
        Update Value
      </button>
    </div>
  );
};
```

## Component with Data Fetching

```tsx
import React, { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import styles from './ComponentName.module.css';

interface DataItem {
  id: string;
  name: string;
  // Add other fields as needed
}

interface ComponentNameProps {
  // Define props here
  queryParam: string;
}

/**
 * ComponentName - Brief description of the component
 * 
 * Detailed description of the component's purpose and usage.
 * Include any important notes or considerations.
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  queryParam,
}) => {
  // State
  const [data, setData] = useState<DataItem[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  // Data fetching
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const { data, error } = await supabase
          .from('some_table')
          .select('*')
          .eq('some_field', queryParam);
        
        if (error) throw error;
        
        setData(data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err instanceof Error ? err : new Error('An unknown error occurred'));
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [queryParam]);
  
  // Render loading state
  if (isLoading) {
    return <div className={styles.loader}>Loading...</div>;
  }
  
  // Render error state
  if (error) {
    return (
      <div className={styles.error}>
        Error: {error.message}
      </div>
    );
  }
  
  // Render data
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Results</h2>
      
      {data && data.length > 0 ? (
        <ul className={styles.list}>
          {data.map((item) => (
            <li key={item.id} className={styles.item}>
              {item.name}
            </li>
          ))}
        </ul>
      ) : (
        <div className={styles.empty}>No results found</div>
      )}
    </div>
  );
};
```

## CSS Module Template

```css
/* ComponentName.module.css */

.container {
  /* Container styles */
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: var(--background-color);
}

.title {
  /* Title styles */
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.button {
  /* Button styles */
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.button:hover {
  background-color: var(--primary-color-dark);
}

.button:disabled {
  background-color: var(--disabled-color);
  cursor: not-allowed;
}

.content {
  /* Content styles */
  margin-top: 1rem;
}

.loader {
  /* Loader styles */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  color: var(--text-color-secondary);
}

.error {
  /* Error styles */
  padding: 1rem;
  border-radius: 0.25rem;
  background-color: var(--error-background);
  color: var(--error-color);
  margin-bottom: 1rem;
}

.list {
  /* List styles */
  list-style: none;
  padding: 0;
  margin: 0;
}

.item {
  /* List item styles */
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.item:last-child {
  border-bottom: none;
}

.empty {
  /* Empty state styles */
  padding: 1rem;
  text-align: center;
  color: var(--text-color-secondary);
}

/* Responsive styles */
@media (max-width: 768px) {
  .container {
    padding: 0.75rem;
  }
  
  .title {
    font-size: 1.25rem;
  }
}
```

## Test File Template

```tsx
// ComponentName.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly with default props', () => {
    render(<ComponentName label="Test Label" />);
    
    expect(screen.getByText('Test Label')).toBeInTheDocument();
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('calls onClick handler when button is clicked', () => {
    const handleClick = jest.fn();
    render(<ComponentName label="Test Label" onClick={handleClick} />);
    
    fireEvent.click(screen.getByText('Click me'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('renders children correctly', () => {
    render(
      <ComponentName label="Test Label">
        <div data-testid="child">Child Content</div>
      </ComponentName>
    );
    
    expect(screen.getByTestId('child')).toBeInTheDocument();
    expect(screen.getByText('Child Content')).toBeInTheDocument();
  });
  
  it('disables button when disabled prop is true', () => {
    render(<ComponentName label="Test Label" disabled />);
    
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

## Usage Example

```tsx
import { ComponentName } from '@/components/ComponentName';

export default function SomePage() {
  return (
    <div>
      <h1>Some Page</h1>
      
      <ComponentName 
        label="Example Component"
        onClick={() => console.log('Button clicked')}
      >
        <p>This is some content inside the component.</p>
      </ComponentName>
    </div>
  );
}
```

---

*This template provides a starting point for creating React components. Adapt it as needed for your specific requirements.* 