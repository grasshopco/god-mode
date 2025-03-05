# God Mode Web UI

A modern web interface for the God Mode system, allowing you to access it from any device including your phone.

## Features

- 📱 **Use from anywhere** - Access from your phone, tablet, or computer
- 🔄 **Seamless workflow** - Easily enhance prompts and process responses 
- 📋 **One-click copy/paste** - Copy enhanced prompts and paste AI responses with a click
- 📚 **Interaction history** - Keep track of your past prompts and responses
- 📊 **Mobile optimized** - Fully responsive design works perfectly on phones

## Getting Started

### Development Setup

```bash
# Navigate to the web-ui directory
cd web-ui

# Install dependencies
npm install

# Start the development server
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

### Using From Other Devices

To access the web UI from other devices on your network:

1. Find your computer's IP address:
   ```bash
   # On macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows
   ipconfig
   ```

2. Use that IP address with port 3000 in your phone's browser:
   ```
   http://YOUR_IP_ADDRESS:3000
   
   Example: http://192.168.1.100:3000
   ```

## Project Structure

```
web-ui/
├── app/                    # Next.js app directory
│   ├── api/                # API routes
│   │   ├── enhance/        # Enhance prompt endpoint
│   │   └── process/        # Process response endpoint
│   ├── history/            # History page
│   ├── page.tsx            # Main page
│   └── layout.tsx          # App layout
├── components/             # React components
│   ├── ui/                 # ShadCN UI components
│   ├── PromptForm.tsx      # Form for entering prompts
│   ├── ResponseForm.tsx    # Form for pasting responses
│   └── ...
├── lib/                    # Utility functions
│   ├── godmode.ts          # Functions for interacting with godmode scripts
│   └── ...
├── public/                 # Static assets
└── ...
```

## Tech Stack

- **Next.js**: For both frontend and API routes
- **TypeScript**: For type safety
- **ShadCN UI**: For rapid UI development
- **Tailwind CSS**: For styling
- **Vercel**: For optional deployment

## Usage

1. Enter your message in the text area
2. Click "Enhance with God Mode"
3. The enhanced prompt will appear below - click "Copy to Clipboard"
4. Paste the enhanced prompt into Cursor AI
5. Copy Cursor AI's response
6. Paste the response into the "AI Response" text area
7. Click "Process Response"

## Mobile Usage

The interface is optimized for mobile with:
- Large, easy-to-tap buttons
- Full-width text areas
- Bottom navigation bar
- Easy copy/paste functionality 