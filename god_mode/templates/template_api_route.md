# API Route Template

Use this template when creating new API routes for the Grasshop project.

## Basic API Route

```tsx
// app/api/route-name/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { validateRequest } from '@/lib/validation';

/**
 * GET handler for route-name
 * 
 * Description of what this endpoint does and when to use it.
 */
export async function GET(request: NextRequest) {
  try {
    // Get query parameters
    const url = new URL(request.url);
    const someParam = url.searchParams.get('someParam');
    
    // Validate parameters
    if (!someParam) {
      return NextResponse.json(
        { error: 'Missing required parameter: someParam' },
        { status: 400 }
      );
    }
    
    // Fetch data from database
    const { data, error } = await supabase
      .from('some_table')
      .select('*')
      .eq('some_field', someParam);
    
    // Handle database errors
    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch data' },
        { status: 500 }
      );
    }
    
    // Return successful response
    return NextResponse.json({ data });
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}

/**
 * POST handler for route-name
 * 
 * Description of what this endpoint does and when to use it.
 */
export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json();
    
    // Validate request body
    const { valid, errors } = validateRequest(body, [
      'requiredField1',
      'requiredField2',
    ]);
    
    if (!valid) {
      return NextResponse.json(
        { error: 'Validation failed', details: errors },
        { status: 400 }
      );
    }
    
    // Process the request
    const { data, error } = await supabase
      .from('some_table')
      .insert({
        field1: body.requiredField1,
        field2: body.requiredField2,
        created_at: new Date().toISOString(),
      })
      .select()
      .single();
    
    // Handle database errors
    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to create record' },
        { status: 500 }
      );
    }
    
    // Return successful response
    return NextResponse.json(
      { data, message: 'Record created successfully' },
      { status: 201 }
    );
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
```

## Authenticated API Route

```tsx
// app/api/protected-route/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { validateRequest } from '@/lib/validation';
import { getAuthenticatedUser } from '@/lib/auth';

/**
 * GET handler for protected-route
 * 
 * Description of what this endpoint does and when to use it.
 * This endpoint requires authentication.
 */
export async function GET(request: NextRequest) {
  try {
    // Authenticate user
    const { user, error: authError } = await getAuthenticatedUser(request);
    
    if (authError || !user) {
      return NextResponse.json(
        { error: authError || 'Unauthorized' },
        { status: 401 }
      );
    }
    
    // Get query parameters
    const url = new URL(request.url);
    const someParam = url.searchParams.get('someParam');
    
    // Fetch data from database (with row-level security)
    const { data, error } = await supabase
      .from('some_table')
      .select('*')
      .eq('user_id', user.id)
      .eq('some_field', someParam);
    
    // Handle database errors
    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch data' },
        { status: 500 }
      );
    }
    
    // Return successful response
    return NextResponse.json({ data });
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}

/**
 * POST handler for protected-route
 * 
 * Description of what this endpoint does and when to use it.
 * This endpoint requires authentication.
 */
export async function POST(request: NextRequest) {
  try {
    // Authenticate user
    const { user, error: authError } = await getAuthenticatedUser(request);
    
    if (authError || !user) {
      return NextResponse.json(
        { error: authError || 'Unauthorized' },
        { status: 401 }
      );
    }
    
    // Parse request body
    const body = await request.json();
    
    // Validate request body
    const { valid, errors } = validateRequest(body, [
      'requiredField1',
      'requiredField2',
    ]);
    
    if (!valid) {
      return NextResponse.json(
        { error: 'Validation failed', details: errors },
        { status: 400 }
      );
    }
    
    // Process the request
    const { data, error } = await supabase
      .from('some_table')
      .insert({
        user_id: user.id,
        field1: body.requiredField1,
        field2: body.requiredField2,
        created_at: new Date().toISOString(),
      })
      .select()
      .single();
    
    // Handle database errors
    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to create record' },
        { status: 500 }
      );
    }
    
    // Return successful response
    return NextResponse.json(
      { data, message: 'Record created successfully' },
      { status: 201 }
    );
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
```

## API Route with File Upload

```tsx
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { getAuthenticatedUser } from '@/lib/auth';

/**
 * POST handler for file upload
 * 
 * Description of what this endpoint does and when to use it.
 * This endpoint handles file uploads.
 */
export async function POST(request: NextRequest) {
  try {
    // Authenticate user
    const { user, error: authError } = await getAuthenticatedUser(request);
    
    if (authError || !user) {
      return NextResponse.json(
        { error: authError || 'Unauthorized' },
        { status: 401 }
      );
    }
    
    // Get form data with file
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    // Validate file
    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }
    
    // Check file size (e.g., 5MB limit)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size exceeds the 5MB limit' },
        { status: 400 }
      );
    }
    
    // Check file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json(
        { error: 'File type not allowed. Please upload a JPEG, PNG, or GIF image.' },
        { status: 400 }
      );
    }
    
    // Generate a unique filename
    const fileName = `${user.id}/${Date.now()}-${file.name}`;
    
    // Convert file to buffer
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    
    // Upload to Supabase Storage
    const { data, error } = await supabase.storage
      .from('uploads')
      .upload(fileName, buffer, {
        contentType: file.type,
        upsert: false,
      });
    
    // Handle upload errors
    if (error) {
      console.error('Storage error:', error);
      return NextResponse.json(
        { error: 'Failed to upload file' },
        { status: 500 }
      );
    }
    
    // Get public URL
    const { data: publicUrlData } = supabase.storage
      .from('uploads')
      .getPublicUrl(fileName);
    
    // Save file metadata to database
    const { data: fileRecord, error: dbError } = await supabase
      .from('files')
      .insert({
        user_id: user.id,
        filename: file.name,
        storage_path: fileName,
        public_url: publicUrlData.publicUrl,
        file_type: file.type,
        file_size: file.size,
        created_at: new Date().toISOString(),
      })
      .select()
      .single();
    
    // Handle database errors
    if (dbError) {
      console.error('Database error:', dbError);
      return NextResponse.json(
        { error: 'Failed to save file metadata' },
        { status: 500 }
      );
    }
    
    // Return successful response
    return NextResponse.json(
      { 
        data: fileRecord, 
        message: 'File uploaded successfully',
        url: publicUrlData.publicUrl
      },
      { status: 201 }
    );
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
```

## API Route with Pagination

```tsx
// app/api/paginated-route/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

/**
 * GET handler for paginated-route
 * 
 * Description of what this endpoint does and when to use it.
 * This endpoint supports pagination.
 */
export async function GET(request: NextRequest) {
  try {
    // Get query parameters
    const url = new URL(request.url);
    
    // Pagination parameters
    const page = parseInt(url.searchParams.get('page') || '1');
    const pageSize = parseInt(url.searchParams.get('pageSize') || '10');
    
    // Validate pagination parameters
    if (page < 1 || pageSize < 1 || pageSize > 100) {
      return NextResponse.json(
        { error: 'Invalid pagination parameters' },
        { status: 400 }
      );
    }
    
    // Calculate offset
    const offset = (page - 1) * pageSize;
    
    // Sorting parameters
    const sortBy = url.searchParams.get('sortBy') || 'created_at';
    const sortOrder = url.searchParams.get('sortOrder') || 'desc';
    
    // Validate sort parameters
    const allowedSortFields = ['created_at', 'title', 'updated_at'];
    const allowedSortOrders = ['asc', 'desc'];
    
    if (!allowedSortFields.includes(sortBy) || !allowedSortOrders.includes(sortOrder)) {
      return NextResponse.json(
        { error: 'Invalid sort parameters' },
        { status: 400 }
      );
    }
    
    // Filtering parameters
    const filterField = url.searchParams.get('filterField');
    const filterValue = url.searchParams.get('filterValue');
    
    // Build query
    let query = supabase
      .from('some_table')
      .select('*', { count: 'exact' })
      .order(sortBy, { ascending: sortOrder === 'asc' })
      .range(offset, offset + pageSize - 1);
    
    // Apply filter if provided
    if (filterField && filterValue) {
      query = query.eq(filterField, filterValue);
    }
    
    // Execute query
    const { data, error, count } = await query;
    
    // Handle database errors
    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch data' },
        { status: 500 }
      );
    }
    
    // Calculate pagination metadata
    const totalPages = count ? Math.ceil(count / pageSize) : 0;
    const hasNextPage = page < totalPages;
    const hasPrevPage = page > 1;
    
    // Return successful response with pagination metadata
    return NextResponse.json({
      data,
      meta: {
        page,
        pageSize,
        totalItems: count,
        totalPages,
        hasNextPage,
        hasPrevPage,
      },
    });
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
```

## API Route with Rate Limiting

```tsx
// app/api/rate-limited/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { getAuthenticatedUser } from '@/lib/auth';
import { rateLimit } from '@/lib/rate-limit';

/**
 * POST handler for rate-limited endpoint
 * 
 * Description of what this endpoint does and when to use it.
 * This endpoint implements rate limiting.
 */
export async function POST(request: NextRequest) {
  try {
    // Get client IP
    const ip = request.headers.get('x-forwarded-for') || 'unknown';
    
    // Apply rate limiting (e.g., 5 requests per minute)
    const rateLimitResult = await rateLimit({
      ip,
      limit: 5,
      duration: 60, // 1 minute
    });
    
    if (!rateLimitResult.success) {
      return NextResponse.json(
        { 
          error: 'Rate limit exceeded', 
          retryAfter: rateLimitResult.retryAfter 
        },
        { 
          status: 429,
          headers: {
            'Retry-After': String(rateLimitResult.retryAfter),
          },
        }
      );
    }
    
    // Authenticate user
    const { user, error: authError } = await getAuthenticatedUser(request);
    
    if (authError || !user) {
      return NextResponse.json(
        { error: authError || 'Unauthorized' },
        { status: 401 }
      );
    }
    
    // Parse request body
    const body = await request.json();
    
    // Process the request
    // ... (implementation specific to the endpoint)
    
    // Return successful response
    return NextResponse.json({ 
      message: 'Request processed successfully',
      remainingRequests: rateLimitResult.remaining,
    });
  } catch (error) {
    // Log unexpected errors
    console.error('Unexpected error:', error);
    
    // Return generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
```

## Usage Examples

### Calling the API from the Frontend

```tsx
// Example of calling the API from a React component
import { useState } from 'react';

export function ApiExample() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/route-name?someParam=value');
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch data');
      }
      
      const result = await response.json();
      setData(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button onClick={fetchData} disabled={loading}>
        {loading ? 'Loading...' : 'Fetch Data'}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {data && (
        <div>
          <h2>Results:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

### Submitting Data to the API

```tsx
// Example of submitting data to the API
import { useState } from 'react';

export function SubmitExample() {
  const [formData, setFormData] = useState({
    requiredField1: '',
    requiredField2: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      setSuccess(false);
      
      const response = await fetch('/api/route-name', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to submit data');
      }
      
      const result = await response.json();
      setSuccess(true);
      
      // Reset form
      setFormData({
        requiredField1: '',
        requiredField2: '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="requiredField1">Field 1:</label>
        <input
          type="text"
          id="requiredField1"
          name="requiredField1"
          value={formData.requiredField1}
          onChange={handleChange}
          required
        />
      </div>
      
      <div>
        <label htmlFor="requiredField2">Field 2:</label>
        <input
          type="text"
          id="requiredField2"
          name="requiredField2"
          value={formData.requiredField2}
          onChange={handleChange}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">Data submitted successfully!</div>}
    </form>
  );
}
```

---

*This template provides a starting point for creating API routes. Adapt it as needed for your specific requirements.* 