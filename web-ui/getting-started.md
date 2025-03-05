# Getting Started with God Mode Web UI

This guide will help you set up and run the God Mode Web UI, allowing you to access God Mode from any device including your phone.

## Prerequisites

- Node.js and npm installed on your computer
- God Mode scripts (`godmode.sh` and `godmode-process.sh`) already set up

## Step 1: Install Dependencies

```bash
# Navigate to the web-ui directory
cd GOD_MODE_PROJECT_STARTER_TEMPLATE/web-ui

# Install dependencies
npm install
```

## Step 2: Run the Development Server

```bash
# Start the Next.js development server
npm run dev
```

This will start the server on [http://localhost:3000](http://localhost:3000).

## Step 3: Access from Your Computer

Open your browser and go to [http://localhost:3000](http://localhost:3000) to use the God Mode Web UI.

## Step 4: Access from Your Phone or Other Devices

To access the web UI from your phone or other devices:

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

3. Make sure your phone and computer are on the same Wi-Fi network.

## Using the Web UI

1. **Enter your prompt**:
   - Type or paste your message in the text box
   - Click "Enhance with God Mode"

2. **Copy enhanced prompt**:
   - The enhanced prompt will appear
   - Click "Copy to Clipboard"
   - Paste it into Cursor AI

3. **Process AI response**:
   - Copy the entire AI response
   - Paste it into the "AI Response" text box
   - Click "Process Response"

## Troubleshooting

### Cannot Access from Phone

- Make sure your phone and computer are on the same network
- Check if your computer firewall is blocking connections
- Try using the computer's hostname instead of IP address

### Script Execution Errors

- Make sure the paths to `godmode.sh` and `godmode-process.sh` are correct
- Check that both scripts have execution permissions (`chmod +x`)
- Run the scripts manually to see if there are any errors

## Next Steps

- **Deploy to Vercel**: For access from anywhere (requires additional setup)
- **Add Authentication**: If deploying publicly, add user authentication
- **Create Progressive Web App**: For a more app-like experience on mobile

## Need Help?

If you encounter any issues or have questions, please open an issue on the GitHub repository. 