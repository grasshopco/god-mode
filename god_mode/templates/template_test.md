# Test Template

Use this template when creating new test files for the Grasshop project.

## Component Test Template

```tsx
// ComponentName.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // Basic rendering test
  it('renders correctly with default props', () => {
    render(<ComponentName label="Test Label" />);
    
    expect(screen.getByText('Test Label')).toBeInTheDocument();
    // Add more assertions based on your component's expected output
  });
  
  // Interaction test
  it('handles user interactions correctly', async () => {
    const handleClick = jest.fn();
    render(<ComponentName label="Test Label" onClick={handleClick} />);
    
    // Click a button
    await userEvent.click(screen.getByRole('button', { name: /click me/i }));
    
    // Verify the handler was called
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  // Props test
  it('renders differently based on props', () => {
    const { rerender } = render(<ComponentName label="Initial Label" />);
    expect(screen.getByText('Initial Label')).toBeInTheDocument();
    
    // Re-render with different props
    rerender(<ComponentName label="Updated Label" />);
    expect(screen.getByText('Updated Label')).toBeInTheDocument();
  });
  
  // State test
  it('updates state correctly', async () => {
    render(<ComponentName label="Test Label" />);
    
    // Interact with component to change state
    await userEvent.click(screen.getByRole('button', { name: /increment/i }));
    
    // Verify state change is reflected in the UI
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
  
  // Conditional rendering test
  it('conditionally renders elements based on props', () => {
    const { rerender } = render(<ComponentName label="Test Label" showExtra={false} />);
    
    // Verify element is not present
    expect(screen.queryByTestId('extra-content')).not.toBeInTheDocument();
    
    // Re-render with showExtra=true
    rerender(<ComponentName label="Test Label" showExtra={true} />);
    
    // Verify element is now present
    expect(screen.getByTestId('extra-content')).toBeInTheDocument();
  });
  
  // Async test
  it('handles async operations correctly', async () => {
    render(<ComponentName label="Test Label" fetchData={true} />);
    
    // Initially shows loading state
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
    
    // Verify data is displayed
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
  
  // Error handling test
  it('handles errors correctly', async () => {
    // Mock a function that will throw an error
    const mockFetchWithError = jest.fn().mockRejectedValue(new Error('Failed to fetch'));
    
    render(<ComponentName label="Test Label" fetchData={mockFetchWithError} />);
    
    // Wait for error to be displayed
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
    });
  });
});
```

## Hook Test Template

```tsx
// useFeature.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useFeature } from './useFeature';

// Mock dependencies
jest.mock('@/lib/api', () => ({
  fetchData: jest.fn(),
}));

import { fetchData } from '@/lib/api';

describe('useFeature', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  // Basic initialization test
  it('initializes with default values', () => {
    const { result } = renderHook(() => useFeature());
    
    expect(result.current.value).toBe('');
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });
  
  // Test with custom initial values
  it('accepts and uses custom initial values', () => {
    const { result } = renderHook(() => useFeature({ initialValue: 'test' }));
    
    expect(result.current.value).toBe('test');
  });
  
  // Test state updates
  it('updates state correctly', () => {
    const { result } = renderHook(() => useFeature());
    
    act(() => {
      result.current.setValue('new value');
    });
    
    expect(result.current.value).toBe('new value');
  });
  
  // Test async operations
  it('handles async operations correctly', async () => {
    // Mock the API response
    (fetchData as jest.Mock).mockResolvedValue({ data: 'test data' });
    
    const { result, waitForNextUpdate } = renderHook(() => useFeature());
    
    // Trigger the async operation
    act(() => {
      result.current.fetchData();
    });
    
    // Verify loading state
    expect(result.current.isLoading).toBe(true);
    
    // Wait for the operation to complete
    await waitForNextUpdate();
    
    // Verify final state
    expect(result.current.isLoading).toBe(false);
    expect(result.current.value).toBe('test data');
    expect(result.current.error).toBeNull();
    expect(fetchData).toHaveBeenCalledTimes(1);
  });
  
  // Test error handling
  it('handles errors correctly', async () => {
    // Mock an API error
    const error = new Error('Failed to fetch data');
    (fetchData as jest.Mock).mockRejectedValue(error);
    
    const { result, waitForNextUpdate } = renderHook(() => useFeature());
    
    // Trigger the async operation
    act(() => {
      result.current.fetchData();
    });
    
    // Wait for the operation to complete
    await waitForNextUpdate();
    
    // Verify error state
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toEqual(error);
    expect(fetchData).toHaveBeenCalledTimes(1);
  });
  
  // Test cleanup
  it('performs cleanup on unmount', () => {
    const cleanup = jest.fn();
    const useHookWithCleanup = () => {
      const result = useFeature();
      result.cleanup = cleanup;
      return result;
    };
    
    const { unmount } = renderHook(() => useHookWithCleanup());
    
    unmount();
    
    expect(cleanup).toHaveBeenCalledTimes(1);
  });
});
```

## API Route Test Template

```tsx
// route-name.test.ts
import { NextRequest } from 'next/server';
import { GET, POST } from './route';

// Mock dependencies
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn().mockReturnThis(),
    select: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    single: jest.fn(),
  },
}));

import { supabase } from '@/lib/supabase';

describe('route-name API', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  describe('GET handler', () => {
    it('returns data successfully', async () => {
      // Mock successful response
      const mockData = [{ id: 1, name: 'Test' }];
      (supabase.from as jest.Mock).mockReturnThis();
      (supabase.select as jest.Mock).mockReturnThis();
      (supabase.eq as jest.Mock).mockResolvedValue({
        data: mockData,
        error: null,
      });
      
      // Create mock request
      const request = new NextRequest(
        new URL('http://localhost:3000/api/route-name?someParam=test')
      );
      
      // Call the handler
      const response = await GET(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(200);
      expect(responseData).toEqual({ data: mockData });
      
      // Verify supabase was called correctly
      expect(supabase.from).toHaveBeenCalledWith('some_table');
      expect(supabase.select).toHaveBeenCalledWith('*');
      expect(supabase.eq).toHaveBeenCalledWith('some_field', 'test');
    });
    
    it('handles missing parameters', async () => {
      // Create mock request without required parameter
      const request = new NextRequest(
        new URL('http://localhost:3000/api/route-name')
      );
      
      // Call the handler
      const response = await GET(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(400);
      expect(responseData).toEqual({
        error: 'Missing required parameter: someParam',
      });
    });
    
    it('handles database errors', async () => {
      // Mock database error
      (supabase.from as jest.Mock).mockReturnThis();
      (supabase.select as jest.Mock).mockReturnThis();
      (supabase.eq as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'Database error' },
      });
      
      // Create mock request
      const request = new NextRequest(
        new URL('http://localhost:3000/api/route-name?someParam=test')
      );
      
      // Call the handler
      const response = await GET(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(500);
      expect(responseData).toEqual({ error: 'Failed to fetch data' });
    });
  });
  
  describe('POST handler', () => {
    it('creates a record successfully', async () => {
      // Mock successful response
      const mockData = { id: 1, field1: 'value1', field2: 'value2' };
      (supabase.from as jest.Mock).mockReturnThis();
      (supabase.insert as jest.Mock).mockReturnThis();
      (supabase.select as jest.Mock).mockReturnThis();
      (supabase.single as jest.Mock).mockResolvedValue({
        data: mockData,
        error: null,
      });
      
      // Create mock request
      const request = new NextRequest(
        'http://localhost:3000/api/route-name',
        {
          method: 'POST',
          body: JSON.stringify({
            requiredField1: 'value1',
            requiredField2: 'value2',
          }),
        }
      );
      
      // Call the handler
      const response = await POST(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(201);
      expect(responseData).toEqual({
        data: mockData,
        message: 'Record created successfully',
      });
      
      // Verify supabase was called correctly
      expect(supabase.from).toHaveBeenCalledWith('some_table');
      expect(supabase.insert).toHaveBeenCalledWith(expect.objectContaining({
        field1: 'value1',
        field2: 'value2',
      }));
    });
    
    it('handles validation errors', async () => {
      // Create mock request with missing fields
      const request = new NextRequest(
        'http://localhost:3000/api/route-name',
        {
          method: 'POST',
          body: JSON.stringify({}),
        }
      );
      
      // Call the handler
      const response = await POST(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(400);
      expect(responseData).toEqual(expect.objectContaining({
        error: 'Validation failed',
      }));
    });
    
    it('handles database errors', async () => {
      // Mock database error
      (supabase.from as jest.Mock).mockReturnThis();
      (supabase.insert as jest.Mock).mockReturnThis();
      (supabase.select as jest.Mock).mockReturnThis();
      (supabase.single as jest.Mock).mockResolvedValue({
        data: null,
        error: { message: 'Database error' },
      });
      
      // Create mock request
      const request = new NextRequest(
        'http://localhost:3000/api/route-name',
        {
          method: 'POST',
          body: JSON.stringify({
            requiredField1: 'value1',
            requiredField2: 'value2',
          }),
        }
      );
      
      // Call the handler
      const response = await POST(request);
      const responseData = await response.json();
      
      // Verify response
      expect(response.status).toBe(500);
      expect(responseData).toEqual({ error: 'Failed to create record' });
    });
  });
});
```

## Utility Function Test Template

```tsx
// utils.test.ts
import { formatDate, calculateTotal, validateEmail } from './utils';

describe('Utility Functions', () => {
  describe('formatDate', () => {
    it('formats date correctly', () => {
      const date = new Date('2023-01-15T12:30:45Z');
      expect(formatDate(date)).toBe('Jan 15, 2023');
    });
    
    it('handles invalid dates', () => {
      expect(formatDate(null)).toBe('');
      expect(formatDate(undefined)).toBe('');
      expect(formatDate(new Date('invalid'))).toBe('Invalid Date');
    });
    
    it('respects format options', () => {
      const date = new Date('2023-01-15T12:30:45Z');
      expect(formatDate(date, { month: 'long' })).toBe('January 15, 2023');
      expect(formatDate(date, { includeTime: true })).toBe('Jan 15, 2023, 12:30 PM');
    });
  });
  
  describe('calculateTotal', () => {
    it('calculates sum correctly', () => {
      const items = [
        { price: 10, quantity: 2 },
        { price: 15, quantity: 1 },
        { price: 5, quantity: 3 },
      ];
      
      expect(calculateTotal(items)).toBe(10 * 2 + 15 * 1 + 5 * 3);
    });
    
    it('handles empty array', () => {
      expect(calculateTotal([])).toBe(0);
    });
    
    it('handles invalid inputs', () => {
      expect(calculateTotal(null)).toBe(0);
      expect(calculateTotal(undefined)).toBe(0);
    });
    
    it('applies discount correctly', () => {
      const items = [
        { price: 100, quantity: 1 },
      ];
      
      expect(calculateTotal(items, 20)).toBe(80); // 20% discount
    });
  });
  
  describe('validateEmail', () => {
    it('validates correct email formats', () => {
      expect(validateEmail('user@example.com')).toBe(true);
      expect(validateEmail('user.name@example.co.uk')).toBe(true);
      expect(validateEmail('user+tag@example.com')).toBe(true);
    });
    
    it('rejects invalid email formats', () => {
      expect(validateEmail('user@')).toBe(false);
      expect(validateEmail('user@example')).toBe(false);
      expect(validateEmail('user.example.com')).toBe(false);
      expect(validateEmail('')).toBe(false);
      expect(validateEmail(null)).toBe(false);
      expect(validateEmail(undefined)).toBe(false);
    });
  });
});
```

## Context Provider Test Template

```tsx
// FeatureContext.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FeatureProvider, useFeature } from './FeatureContext';

// Mock API calls
jest.mock('@/lib/api', () => ({
  fetchFeatureData: jest.fn(),
}));

import { fetchFeatureData } from '@/lib/api';

// Test component that uses the context
const TestComponent = () => {
  const { data, isLoading, error, refreshData } = useFeature();
  
  return (
    <div>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
      {data && (
        <div>
          <h1>Data Loaded</h1>
          <pre data-testid="data">{JSON.stringify(data)}</pre>
          <button onClick={refreshData}>Refresh</button>
        </div>
      )}
    </div>
  );
};

describe('FeatureContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('provides loading state initially', () => {
    // Mock API call that never resolves
    (fetchFeatureData as jest.Mock).mockImplementation(() => new Promise(() => {}));
    
    render(
      <FeatureProvider>
        <TestComponent />
      </FeatureProvider>
    );
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
  
  it('provides data when loaded successfully', async () => {
    // Mock successful API response
    const mockData = [{ id: 1, name: 'Test Item' }];
    (fetchFeatureData as jest.Mock).mockResolvedValue(mockData);
    
    render(
      <FeatureProvider>
        <TestComponent />
      </FeatureProvider>
    );
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
    
    // Verify data is displayed
    expect(screen.getByText('Data Loaded')).toBeInTheDocument();
    expect(screen.getByTestId('data').textContent).toBe(JSON.stringify(mockData));
  });
  
  it('provides error when API call fails', async () => {
    // Mock API error
    const error = new Error('Failed to fetch data');
    (fetchFeatureData as jest.Mock).mockRejectedValue(error);
    
    render(
      <FeatureProvider>
        <TestComponent />
      </FeatureProvider>
    );
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
    
    // Verify error is displayed
    expect(screen.getByText('Error: Failed to fetch data')).toBeInTheDocument();
  });
  
  it('refreshes data when refresh function is called', async () => {
    // Mock successful API response
    const mockData = [{ id: 1, name: 'Test Item' }];
    (fetchFeatureData as jest.Mock).mockResolvedValue(mockData);
    
    render(
      <FeatureProvider>
        <TestComponent />
      </FeatureProvider>
    );
    
    // Wait for initial data load
    await waitFor(() => {
      expect(screen.getByText('Data Loaded')).toBeInTheDocument();
    });
    
    // Clear mock and set up new response
    (fetchFeatureData as jest.Mock).mockClear();
    const updatedData = [{ id: 1, name: 'Updated Item' }];
    (fetchFeatureData as jest.Mock).mockResolvedValue(updatedData);
    
    // Click refresh button
    await userEvent.click(screen.getByText('Refresh'));
    
    // Verify API was called again
    expect(fetchFeatureData).toHaveBeenCalledTimes(1);
    
    // Wait for updated data
    await waitFor(() => {
      expect(screen.getByTestId('data').textContent).toBe(JSON.stringify(updatedData));
    });
  });
  
  it('throws error when useFeature is used outside provider', () => {
    // Mock console.error to prevent error output in tests
    const originalError = console.error;
    console.error = jest.fn();
    
    // Expect render to throw
    expect(() => {
      render(<TestComponent />);
    }).toThrow('useFeature must be used within a FeatureProvider');
    
    // Restore console.error
    console.error = originalError;
  });
});
```

## Jest Configuration

```js
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    // Handle module aliases
    '^@/(.*)$': '<rootDir>/src/$1',
    // Handle CSS imports (with CSS modules)
    '\\.module\\.(css|scss|sass)$': 'identity-obj-proxy',
    // Handle image imports
    '\\.(jpg|jpeg|png|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  transform: {
    // Use babel-jest to transpile tests with the next/babel preset
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
  transformIgnorePatterns: [
    '/node_modules/',
    '^.+\\.module\\.(css|sass|scss)$',
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/pages/_app.tsx',
    '!src/pages/_document.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};
```

## Jest Setup File

```js
// jest.setup.js
import '@testing-library/jest-dom';

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    back: jest.fn(),
    pathname: '/',
    query: {},
    asPath: '/',
    events: {
      on: jest.fn(),
      off: jest.fn(),
    },
  }),
}));

// Mock Supabase
jest.mock('@/lib/supabase', () => ({
  supabase: {
    auth: {
      getSession: jest.fn().mockResolvedValue({ data: { session: null }, error: null }),
      signIn: jest.fn(),
      signOut: jest.fn(),
    },
    from: jest.fn().mockReturnThis(),
    select: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    update: jest.fn().mockReturnThis(),
    delete: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    single: jest.fn(),
  },
}));

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() { return null; }
  unobserve() { return null; }
  disconnect() { return null; }
};

// Suppress console errors during tests
const originalConsoleError = console.error;
console.error = (...args) => {
  if (
    /Warning.*not wrapped in act/i.test(args[0]) ||
    /Warning.*ReactDOM.render is no longer supported/i.test(args[0])
  ) {
    return;
  }
  originalConsoleError(...args);
};
```

## Common Test Mocks

```js
// __mocks__/fileMock.js
module.exports = 'test-file-stub';
```

```js
// __mocks__/styleMock.js
module.exports = {};
```

---

*This template provides a starting point for creating test files. Adapt it as needed for your specific requirements.* 